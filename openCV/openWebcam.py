import cv2
from signal import signal, SIGINT
import sys

cap = cv2.VideoCapture(0)
print(cap.isOpened())
exitFlag=0

def handler(signal_received, frame):
    print('Signal received')
    cap.release()
    cv2.destroyAllWindows()
    exitFlag=1
    print('cap released')
    sys.exit()

signal(SIGINT, handler)

while (exitFlag==0):
    ret, frame = cap.read()
    if frame is not None:
        print('Got frame')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # equalize the histogram of the Y channel
        histEq = cv2.equalizeHist(gray)

        cv2.imshow('frame', histEq)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

print('Break for while loop')



