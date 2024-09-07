import cv2 
import os 
from facefile_edit import facerec

sfr = facerec()
sfr.encodings_imgs(r"C:\Users\HP_Laptop\Downloads\imgs") # write the folder's name where the images exist 
cap = cv2.VideoCapture(0)
while True:
    _,frame = cap.read()
    locs, face_name = sfr.detect(frame)
    for(top, right, bottom, left),(name) in zip(locs, face_name):
            if name != "Unknown":
                cv2.rectangle(frame, (left, top), (right, bottom), (127,127,0), 3)
            else:
                cv2.rectangle(frame, (left, top), (right, bottom), (0,0,255), 3)
            cv2.putText(frame, name, (left, top-10), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
    cv2.imshow("Face Detection", frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
