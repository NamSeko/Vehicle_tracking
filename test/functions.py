import cv2
import numpy as np
import os
import re

CONFUSIONS_TO_NUMBER = {
    'B': '8',
    'G': '6',
    'Z': '2',
    'S': '5',
    'O': '0',
    'I': '1',
    'D': '0',
    'A': '4',
    'C': '0',
    'L': '4'
}

CONFUSIONS_TO_LETTER = {
    '8': 'B',
    '6': 'G',
    '9': 'B',
    '2': 'Z',
    '5': 'S',
    '0': 'B',
    '1': 'I',
}

def correct_char(char, must_be_letter=False):
    if must_be_letter:
        return CONFUSIONS_TO_LETTER.get(char, char)
    else:
        return CONFUSIONS_TO_NUMBER.get(char, char)

def post_process_license_plate(raw_text, cls):
    clean_text = re.sub(r'[^A-Z0-9]', '', str(raw_text).upper())
    if len(clean_text) <= 7:
        return "OCR ERROR" 

    corrected_chars = []
    
    if len(clean_text) == 9:
        if cls == 0:
            template = "NNLLNNNNNNNN"
        elif cls == 1:
            template = "NNLNNNNNNNN" 
    else:
        template = "NNLNNNNNNNN"

    for i, char in enumerate(clean_text):
        must_be_letter = (template[i] == 'L')
        corrected_chars.append(correct_char(char, must_be_letter))

    return "".join(corrected_chars)

def process_img(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(2,2))
    enh = clahe.apply(img)
    blur = cv2.GaussianBlur(enh, (0,0), 3)
    sharp = cv2.addWeighted(enh, 1.5, blur, -0.5, 0)
    lap = cv2.Laplacian(sharp, cv2.CV_8U, ksize=3)
    final = cv2.addWeighted(sharp, 1, lap, -0.4, 0)
    return final

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

class SelectAreaDetect:
    def __init__(self, video_path="demo/demo.mp4", scale=0.5):
        cap = cv2.VideoCapture(video_path)
        self.data_path = video_path.split("/")[-1].split(".")[0]
        os.makedirs(self.data_path, exist_ok=True)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imwrite(f"{self.data_path}/{self.data_path}.png", frame)
            self.img = frame
            break
        cap.release()
        self.scale = scale
        self.points = []
    def plot_point(self, image):
        if len(self.points) == 1:
            x, y = self.points[0]
            cv2.circle(image, (x, y), 3, (0, 0, 255), -3)
        else:
            for i in range(len(self.points)-1):
                x1, y1 = self.points[i]
                x2, y2 = self.points[i+1]
                cv2.circle(image, (x1, y1), 3, (0, 0, 255), -3)
                cv2.circle(image, (x2, y2), 3, (0, 0, 255), -3)
                cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.imshow("Image", image)

    def create_txt(self):
        def click_event(event, x, y, flags, params):
            if event == cv2.EVENT_LBUTTONDOWN:
                print(f'Point coordinates: ({x}, {y})')
                self.points.append((x, y))        
                self.plot_point(self.img)
        h, w = self.img.shape[:2]
        self.img = cv2.resize(self.img, (int(w*self.scale), int(h*self.scale)))
        cv2.imshow('Image', self.img)

        cv2.setMouseCallback('Image', click_event)
        while True:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        cv2.destroyAllWindows()

        with open(f"{self.data_path}/{self.data_path}.txt", "w") as f:
            for x, y in self.points:
                x, y = x/self.scale, y/self.scale
                f.write(f"{int(x)} {int(y)}\n")