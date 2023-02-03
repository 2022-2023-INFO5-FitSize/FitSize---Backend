import argparse
import time
from pathlib import Path
import numpy as np

import cv2
import torch
import torch.backends.cudnn as cudnn
from numpy import random
from tqdm import tqdm

from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages
from utils.general import check_img_size, check_imshow, non_max_suppression, scale_coords, xyxy2xywh, set_logging, increment_path
from utils.plots import plot_one_box
from utils.torch_utils import select_device, TracedModel

# import original modules
from utils.LM_utils.fashionai_key_points_detection_utils import draw_keypoints
from utils.LM_utils.utils import get_base_parser, update_parser  # noqa: E402
from utils.LM_utils.model_utils import check_and_download_models  # noqa: E402
# from utils.webcamera_utils import get_capture  # noqa: E402

import ailia
from utils.helper import preprocess_landmark_img, post_processing_landmarks, get_checkerboard_corners
from CONFIG import *

# logger
from logging import getLogger   # noqa: E402
logger = getLogger(__name__)

# ======================
# Arguemnt Parser Config
# ======================
parser = get_base_parser('FashionAI model')
args = update_parser(parser)



def detect(save_img=False):
    source, weights, view_img, save_txt, imgsz, trace = opt.source, opt.weights, opt.view_img, opt.save_txt, opt.img_size, not opt.no_trace
    save_img = not opt.nosave and not source.endswith('.txt')  # save inference images
    webcam = source.isnumeric() or source.endswith('.txt') or source.lower().startswith(('rtsp://', 'rtmp://', 'http://', 'https://'))

    # Directories
    save_dir = Path(increment_path(Path(opt.project) / opt.name, exist_ok=opt.exist_ok))  # increment run
    (save_dir / 'labels' if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir

    # Initialize
    set_logging()
    device = select_device(opt.device)
    half = device.type != 'cpu'  # half precision only supported on CUDA

    # Load detector model
    model = attempt_load(weights, map_location=device)  # load FP32 model
    stride = int(model.stride.max())  # model stride
    imgsz = check_img_size(imgsz, s=stride)  # check img_size

    if trace:
        model = TracedModel(model, device, opt.img_size)

    if half:
        model.half()  # to FP16

    # initialize Landmarks Detection Models
    for model_name, info in MODELS.items():
        weight_path, model_path = info['weights_path'], info['model_path']
        # model files check and download for Landmarks model
        check_and_download_models(weight_path, model_path, REMOTE_PATH_LANDMARKS)

        # initialize Landmarks model
        net = ailia.Net(model_path, weight_path, env_id=args.env_id)
        MODELS[model_name]['net'] = net

    # Set Dataloader
    vid_path, vid_writer = None, None
    if webcam:
        view_img = check_imshow()
        cudnn.benchmark = True  # set True to speed up constant image size inference
        dataset = LoadStreams(source, img_size=imgsz, stride=stride)
    else:
        dataset = LoadImages(source, img_size=imgsz, stride=stride)

    # Get names and colors
    names = model.module.names if hasattr(model, 'module') else model.names
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]

    # Run inference
    if device.type != 'cpu':
        model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once
    t0 = time.time()
    
    for path, img, im0s, vid_cap in tqdm(dataset, total=len(dataset)):
        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Inference and apply NMS
        pred = model(img, augment=opt.augment)[0]
        pred = non_max_suppression(pred, opt.conf_thres, opt.iou_thres, classes=opt.classes, agnostic=opt.agnostic_nms)

        # Process detections
        for i, det in enumerate(pred):  # detections per image
            if webcam:  # batch_size >= 1
                p, s, im0, frame = path[i], '%g: ' % i, im0s[i].copy(), dataset.count
            else:
                p, s, im0, frame = path, '', im0s, getattr(dataset, 'frame', 0)

            p = Path(p)  # to Path
            save_path = str(save_dir / p.name)  # img.jpg
            txt_path = str(save_dir / 'labels' / p.stem) + ('' if dataset.mode == 'image' else f'_{frame}')  # img.txt
            s += '%gx%g ' % img.shape[2:]  # print string
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            if len(det):
                h_orig, w_orig = im0.shape[:2]
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string
                
                # get checkboard image
                bboxs_cb = [xyxy for *xyxy, conf, cls in reversed(det) if names[int(cls)] == "checkerboard"]
                if len(bboxs_cb) > 0:
                    bbox_cb = bboxs_cb[0]   # get the first one

                    # get the pixelate distance between two consecutive corners of the checkerboard
                    im0, cb_box_distance = get_checkerboard_corners(im0, bbox_cb, cb_size=list(map(lambda x: x-1, CHECKBOARD_SIZE)))

                    # need to use the cb_box_distance accordingly
                    # ....
                else:
                    print("checkerboard not detected...")


                # iterate through the detections
                for *xyxy, conf, cls in reversed(det):
                    cls_str = names[int(cls)]

                    if cls_str == "checkerboard":
                        continue

                    x1, y1, x2, y2 = [int(v) for v in xyxy]
                    offset = 100
                    x1 = max(0, x1 - offset)
                    y1 = max(0, y1 - offset)
                    x2 = min(w_orig, x2 + offset)
                    y2 = min(h_orig, y2 + offset)
                    crop = im0[y1:y2, x1:x2].copy()
                    
                    model_ = MODELS[DETECTOR_MAPPING[cls_str]]['net']

                    imgl, imgl_flip, info = preprocess_landmark_img(crop)
                    # inference feedforward
                    output = model_.predict({'img': imgl})
                    output_flip = model_.predict({'img': imgl_flip})

                    _, hm_pred = output
                    _, hm_pred2 = output_flip

                    hm_pred, hm_pred2 = np.maximum(hm_pred, 0), np.maximum(hm_pred2, 0)
                    hm_pred, hm_pred2 = hm_pred[0], hm_pred2[0]
                    keypoints = post_processing_landmarks(hm_pred, hm_pred2, info, DETECTOR_MAPPING[cls_str])

                    # plot result
                    im0 = draw_keypoints(im0, keypoints, DETECTOR_MAPPING[cls_str], offset=(x1, y1))
                    
                    if save_txt:  # Write to file
                        xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                        line = (cls, *xywh, conf) if opt.save_conf else (cls, *xywh)  # label format
                        with open(txt_path + '.txt', 'a') as f:
                            f.write(('%g ' * len(line)).rstrip() % line + '\n')

                    if save_img or view_img:  # Add bbox to image
                        label = f'{cls_str} {conf:.2f}'
                        plot_one_box(xyxy, im0, label=label, color=colors[int(cls)], line_thickness=3)

        # Stream results
        if view_img:
            cv2.imshow("vis", im0)
            cv2.waitKey(0 if dataset.mode == 'image' else 1)  # 1 millisecond

        # Save results (image with detections)
        if save_img:
            if dataset.mode == 'image':
                cv2.imwrite(save_path, im0)
                print(f" The image with the result is saved in: {save_path}")
            else:  # 'video' or 'stream'
                if vid_path != save_path:  # new video
                    vid_path = save_path
                    if isinstance(vid_writer, cv2.VideoWriter):
                        vid_writer.release()  # release previous video writer
                    if vid_cap:  # video
                        fps = vid_cap.get(cv2.CAP_PROP_FPS)
                        w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                        h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    else:  # stream
                        fps, w, h = 30, im0.shape[1], im0.shape[0]
                        save_path += '.mp4'
                    vid_writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
                vid_writer.write(im0)

    if save_txt or save_img:
        s = f"\n{len(list(save_dir.glob('labels/*.txt')))} labels saved to {save_dir / 'labels'}" if save_txt else ''
        #print(f"Results saved to {save_dir}{s}")

    print(f'Done. ({time.time() - t0:.3f}s)')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str, default=WEIGHT_PATH_DETECTOR, help='model.pt path(s)')
    parser.add_argument('--source', type=str, default=SOURCE, help='source')  # file/folder, 0 for webcam
    parser.add_argument('--img-size', type=int, default=DETECTOR_IMAGE_SIZE, help='inference size (pixels)')
    parser.add_argument('--conf-thres', type=float, default=CONFIDENCE_THRESHOLD, help='object confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=IOU_THRESHOLD, help='IOU threshold for NMS')
    parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--view-img', default=VISUALIZE, help='display results')
    parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
    parser.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels')
    parser.add_argument('--nosave', action='store_true', help='do not save images/videos')
    parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --class 0, or --class 0 2 3')
    parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true', help='augmented inference')
    parser.add_argument('--update', action='store_true', help='update all models')
    parser.add_argument('--project', default=RESULTS_PATH, help='save results to project/name')
    parser.add_argument('--name', default='detections', help='save results to project/name')
    parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
    parser.add_argument('--no-trace', default=True, help='don`t trace model')
    opt = parser.parse_args()
    print(opt)

    with torch.no_grad():
        detect()
