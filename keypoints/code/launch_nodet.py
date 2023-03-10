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
from utils.general import check_img_size, check_imshow, non_max_suppression, scale_coords, set_logging, increment_path
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
from logging import getLogger  # noqa: E402

logger = getLogger(__name__)

# ======================
# Arguemnt Parser Config
# ======================
parser = get_base_parser('FashionAI model')
args = update_parser(parser)


def detect(save_img=False):
    source = "data/images/trouser"
    weights = "weights/yolov7_deepfashion2_best.pt"
    view_img = False
    save_txt = True
    imgsz = 416
    no_trace = True
    nosave = False
    save_txt = True

    print("DBG001000:::")
    save_img = not nosave and not source.endswith('.txt')  # save inference images
    print("DBG002000:::")
    webcam = source.isnumeric() or source.endswith('.txt') or source.lower().startswith(
        ('rtsp://', 'rtmp://', 'http://', 'https://'))
    print("DBG003000:::")

    # Directories
    project = "runs"
    name = "detections"
    exist_ok = False

    save_dir = Path(increment_path(Path(project) / name, exist_ok))  # increment run
    (save_dir / 'labels' if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir
    print("DBG004000:::")
    # exit(1)
    # Initialize
    set_logging()
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    half = device.type != 'cpu'  # half precision only supported on CUDA
    print("DBG5000:::")
    print(device)
    # Load detector model
    model = attempt_load(weights, map_location=device)  # load FP32 model
    print("DBG6000:::")
    stride = int(model.stride.max())  # model stride
    print("DBG7000:::")
    imgsz = check_img_size(imgsz, s=stride)  # check img_size
    print("DBG8000:::")
    img_size = 512
    trace = False
    if trace:
        model = TracedModel(model, device, img_size)
        print("DBG9000:::")

    if half:
        model.half()  # to FP16
        print("DBG10000:::")

    # initialize Landmarks Detection Models
    weight_path, model_path = MODELS[CLOTHING_TYPE]['weights_path'], MODELS[CLOTHING_TYPE]['model_path']
    print("DBG11000:::")
    check_and_download_models(weight_path, model_path, REMOTE_PATH_LANDMARKS)
    print("DBG12000:::")
    net = ailia.Net(model_path, weight_path, env_id=args.env_id)
    print("DBG13000:::")
    # Set Dataloader
    vid_path, vid_writer = None, None
    if webcam:
        print("DBG14100:::")
        view_img = check_imshow()
        cudnn.benchmark = True  # set True to speed up constant image size inference
        dataset = LoadStreams(source, img_size=imgsz, stride=stride)
    else:
        print("DBG14200:::")
        dataset = LoadImages(source, img_size=imgsz, stride=stride)

    # Get names and colors
    print("DBG15000:::")
    names = model.module.names if hasattr(model, 'module') else model.names
    print("DBG16000:::")
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]

    # Run inference
    if device.type != 'cpu':
        model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once
    t0 = time.time()

    for path, img, im0s, vid_cap in tqdm(dataset, total=len(dataset)):
        print("DBG17000:::")
        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        ## Inference and apply NMS
        augment = False
        pred = model(img, augment)[0]
        conf_thres = 0.4
        iou_thres = 0.45
        classes = None
        agnostic = False
        pred = non_max_suppression(pred, conf_thres,iou_thres ,classes,agnostic)


        # Process detections
        for i, det in enumerate(pred):  # detections per image
            print("DBG18000:::")
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

                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                # Print results
                for c in det[:, -1].unique():
                    print("DBG19000:::")
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string
                print("DBG200000:::")
                # get checkboard image
                bboxs_cb = [xyxy for *xyxy, conf, cls in reversed(det) if names[int(cls)] == "checkerboard"]
                if len(bboxs_cb) > 0:
                    bbox_cb = bboxs_cb[0]  # get the first one

                    # get the pixelate distance between two consecutive corners of the checkerboard
                    im0, cb_box_distance = get_checkerboard_corners(im0, bbox_cb,
                                                                    cb_size=list(map(lambda x: x - 1, CHECKBOARD_SIZE)))

                    # need to use the cb_box_distance accordingly
                    # ....
                else:
                    print("checkerboard not detected...")
                print("DBG210000:::")
                imgl, imgl_flip, info = preprocess_landmark_img(im0)
                # inference feedforward
                print("DBG220000:::")
                output = net.predict({'img': imgl})
                print("DBG230000:::")
                output_flip = net.predict({'img': imgl_flip})
                print("DBG240000:::")

                _, hm_pred = output
                print("DBG250000:::")
                _, hm_pred2 = output_flip
                print("DBG260000:::")

                hm_pred, hm_pred2 = np.maximum(hm_pred, 0), np.maximum(hm_pred2, 0)
                print("DBG270000:::")
                hm_pred, hm_pred2 = hm_pred[0], hm_pred2[0]
                print("DBG280000:::")
                keypoints = post_processing_landmarks(hm_pred, hm_pred2, info, CLOTHING_TYPE)
                print("DBG290000:::")

                # plot result
                im0 = draw_keypoints(im0, keypoints, CLOTHING_TYPE)
                print("DBG300000:::")

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
        with open(save_dir / 'labels' / 'keypoints.txt', 'w') as kps:
            kps.write(str(keypoints))
            kps.write('\n')
            kps.write(str(cb_box_distance))

        s = f"\n{len(list(save_dir.glob('labels/*.txt')))} labels saved to {save_dir / 'labels'}" if save_txt else ''
        # print(f"Results saved to {save_dir}{s}")

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
