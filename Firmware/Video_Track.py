from ultralytics import YOLO
import cv2
import math
# start webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1056)
cap.set(4, 672)

# model
model = YOLO("yolo11n.pt")
frame_num = 0
frame_jump = 6

# object classes
classNames = ["person"]

while True:
    frame_num+=1
    success, img = cap.read()
    if frame_num%frame_jump !=0:
        continue

    results = model.track(img, stream=False, imgsz=(672,1056), classes=[0])

    # coordinates
    for r in results:
        boxes = r.boxes

        for box in boxes:
            cls = int(box.cls[0])
            # bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

            # put box in cam
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

            # confidence
            confidence = math.ceil((box.conf[0]*100))/100
            print("Confidence --->",confidence)

            # class name
            print("Class name -->", classNames[cls])

            # object details
            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2

            cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)

    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
