import cv2
import numpy as np

def gen_mask(point_path, image_path, scale):
    image = cv2.imread(image_path)
    h, w = image.shape[:2]
    h, w = int(h*scale), int(w*scale)
    all_points = np.loadtxt(point_path)
    all_points *= scale
    polygon_points = all_points.astype(np.int32).reshape((-1, 1, 2))
    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.fillPoly(mask, [polygon_points], (255))
    return mask

def process_image(img, mask, scale):
    h, w = img.shape[:2]
    img = cv2.resize(img, (int(w*scale), int(h*scale)))
    new_img = cv2.bitwise_and(img, img, mask=mask)
    return img, new_img