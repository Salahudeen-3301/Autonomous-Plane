from ultralytics import YOLO
import cv2
import math
# start webcam
def Track(img,jump_frame, frame):

    if frame%jump_frame == 0:
        return None
    classNames = ["person"]
    
    results = model.track(img, stream=False, imgsz=(672,1056), classes=[0])

    # coordinates
    for r in results:
        boxes = r.boxes

        for box in boxes:
            # bounding box
            x1, y1, w, h = box.xywh[0]
            x1, y1, w, h = int(x1), int(y1), int(w), int(h) # convert to int values
            
        return x1,y1,w,h
