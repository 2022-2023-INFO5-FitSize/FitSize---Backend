
import cv2
import numpy as np
from utils.LM_utils.fashionai_key_points_detection_utils import decode_np

from CONFIG import *

# ======================
# Main functions
# ======================

def post_processing_landmarks(hm_pred, hm_pred2, info, model_name):
    keypoint_names = KEYPOINTS[model_name]

    conjug = [
        [i, keypoint_names.index(key.replace('left', 'right'))] 
            for i, key in enumerate(keypoint_names) if 'left' in key
    ]

    a = np.zeros_like(hm_pred2)
    a[:, :, :info['img_w2'] // HM_STRIDE] = np.flip(hm_pred2[:, :, :info['img_w2'] // HM_STRIDE], 2)

    for conj in conjug:
        a[conj] = a[conj[::-1]]
    hm_pred2 = a

    x, y = decode_np(hm_pred + hm_pred2, info['scale'], HM_STRIDE, (info['img_w'] / 2, info['img_h'] / 2), method='maxoffset')
    keypoints_ = np.stack([x, y, np.ones(x.shape)], axis=1).astype(np.int16)

    keypoints = dict()
    for i in range(len(keypoints_)):
        keypoints[keypoint_names[i]] = keypoints_[i]
    return keypoints


def preprocess_landmarks(img, img_size):
    (img_w, img_h) = img_size
    img = cv2.resize(img, (img_w, img_h), interpolation=cv2.INTER_CUBIC)
    img = np.transpose(img, (2, 0, 1)).astype(np.float32)  # channel, height, width
    img[[0, 2]] = img[[2, 0]]  # BGR -> RGB
    img = img / 255.0
    img = (img - MU) / SIGMA
    pad_imgs = np.zeros([1, 3, IMAGE_SIZE, IMAGE_SIZE], dtype=np.float32)
    pad_imgs[0, :, :img_h, :img_w] = img
    return pad_imgs

def preprocess_landmark_img(img):
    img_flip = cv2.flip(img, 1) # flip horizontally

    # Padded resize
    img_h, img_w, _ = img.shape
    scale = IMAGE_SIZE / max(img_w, img_h)
    img_h2 = int(img_h * scale)
    img_w2 = int(img_w * scale)

    # initial preprocesses
    img = preprocess_landmarks(img, (img_w2, img_h2))
    img_flip = preprocess_landmarks(img_flip, (img_w2, img_h2))

    info = {
        'img_h': img_h,
        'img_w': img_w,
        'img_h2': img_h2,
        'img_w2': img_w2,
        'scale': scale,
    }
    return img, img_flip, info

def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))
    resized = cv2.resize(image, dim, interpolation=inter)
    return resized

import math
def l2_distance(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def get_checkerboard_corners(img, bbox_cb, cb_size=(4, 4), offset=5, t_size=150):
    x1, y1, x2, y2 = [int(v) - offset if i in [0, 1] else int(v) + offset for i, v in enumerate(bbox_cb)]
    cb_img = img[y1:y2, x1:x2].copy()                
    
    h, w = cb_img.shape[:2]
    l = h if h < w else w

    flags = cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE
    if l < 100:
        s = t_size / l
        nw, nh = int(w * s), int(h * s)
        cb_img = cv2.resize(cb_img, (nw, nh), interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(cb_img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, cb_size, flags=flags)
        if ret:
            corners = np.array([[int((x_/s) + x1), int((y_/s) + y1)] for corner in corners for x_, y_ in corner])
    else:
        gray = cv2.cvtColor(cb_img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, cb_size, flags=flags)
        if ret:
            corners = np.array([[int(x_ + x1), int(y_ + y1)] for corner in corners for x_, y_ in corner])
    
    if corners is not None:
        for i, corner in enumerate(corners):
            img = cv2.circle(img, corner, 2, (0, 255, 0), -1)
            # cv2.putText(img, str(i), corner, 0, 0.5, [255, 0, 255], thickness=1, lineType=cv2.LINE_AA)

        rows, cols = cb_size
        d = 0
        for i in range(0, len(corners), rows):
            d += l2_distance(corners[i], corners[i + 1])
            d += l2_distance(corners[i + 1], corners[i + 2])
            d += l2_distance(corners[i + 2], corners[i + 3])
        dv = d / (len(corners) - rows)
        print('average', dv)

    return img, dv

