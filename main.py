import cv2
from process.main import FrameProcessing

frame_processing = FrameProcessing()
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

if __name__ == "__main__":

    while True:
        ret, frame = cap.read()
        process = frame_processing.process(frame)
        cv2.imshow('object tracking robot', frame)
        t = cv2.waitKey(5)
        if t == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
