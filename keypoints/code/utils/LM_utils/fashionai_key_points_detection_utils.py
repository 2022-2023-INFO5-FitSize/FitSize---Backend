import numpy as np
import cv2

from CONFIG import CONNECTIONS

color_palette = [(136, 112, 246),
                 (49, 136, 219),
                 (49, 156, 173),
                 (49, 170, 119),
                 (122, 176, 51),
                 (164, 172, 53),
                 (197, 168, 56),
                 (244, 154, 110),
                 (244, 121, 204),
                 (204, 101, 245)]  # husl


def decode_np(heatmap, scale, stride, default_pt, method='exp'):
    '''
    :param heatmap: [pt_num, h, w]
    :param scale:
    :return:
    '''
    kp_num, h, w = heatmap.shape
    dfx, dfy = np.array(default_pt) * scale / stride
    for k, hm in enumerate(heatmap):
        heatmap[k] = cv2.GaussianBlur(hm, (5, 5), 1)
    if method == 'exp':
        xx, yy = np.meshgrid(np.arange(w), np.arange(h))
        heatmap_th = np.copy(heatmap)
        heatmap_th[heatmap < np.amax(heatmap) / 2] = 0
        heat_sums_th = np.sum(heatmap_th, axis=(1, 2))
        x = np.sum(heatmap_th * xx, axis=(1, 2))
        y = np.sum(heatmap_th * yy, axis=(1, 2))
        x = x / heat_sums_th
        y = y / heat_sums_th
        x[heat_sums_th == 0] = dfx
        y[heat_sums_th == 0] = dfy
    else:
        if method == 'max':
            heatmap_th = heatmap.reshape(kp_num, -1)
            y, x = np.unravel_index(np.argmax(heatmap_th, axis=1), [h, w])
        elif method == 'maxoffset':
            heatmap_th = heatmap.reshape(kp_num, -1)
            si = np.argsort(heatmap_th, axis=1)
            y1, x1 = np.unravel_index(si[:, -1], [h, w])
            y2, x2 = np.unravel_index(si[:, -2], [h, w])
            x = (3 * x1 + x2) / 4.
            y = (3 * y1 + y2) / 4.
        var = np.var(heatmap_th, axis=1)
        x[var < 1] = dfx
        y[var < 1] = dfy
    x = x * stride / scale
    y = y * stride / scale
    return np.rint(x + 2), np.rint(y + 2)


def draw_keypoints(image, keypoints, cls, offset=None, draw_connections=False):
    '''
    :param image:
    :param keypoints: [[x, y, v], ...]
    :return:
    '''
    alpha = 1
    thick = 1
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.7
    overlay = image.copy()
    for i, (name, kpt) in enumerate(keypoints.items()):
        x, y, v = kpt

        if offset is not None:
            x += + offset[0]
            y += + offset[1]

        if v > 0:
            # color = color_palette[i % len(color_palette)]
            color = (0, 255, 0)
            overlay = cv2.circle(overlay, (x, y), 5, color, -1)
            overlay = cv2.putText(overlay, name, (x, y), font, font_scale, color, thick, cv2.LINE_AA)
            
    if draw_connections and cls in CONNECTIONS:
        for i, (name, connection) in enumerate(CONNECTIONS[cls].items()):
            color = color_palette[i % len(color_palette)]
            pnt1, pnt2 = keypoints[connection[0]], keypoints[connection[1]]
            if offset is not None:
                pnt1 = pnt1[0] + offset[0], pnt1[1] + offset[1]
                pnt2 = pnt2[0] + offset[0], pnt2[1] + offset[1]
            overlay = cv2.line(overlay, pnt1, pnt2, color, 2)

            pntc = [(c1 + c2) // 2 for c1, c2 in zip(pnt1, pnt2)]
            overlay = cv2.circle(overlay, pntc, 5, color, -1)

    image = cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)
    return image
