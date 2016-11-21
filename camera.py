import numpy as np
import cv2

class Camera:

    def __init__(self, scale=1):
        self.cap = cv2.VideoCapture(0)
        self.scale = scale

    def show_video(self):

        while(True):
            # Capture frame-by-frame
            ret, frame = self.cap.read()

            # Our operations on the frame come here
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            res = cv2.resize(gray,None,fx=self.scale, fy=self.scale, interpolation = cv2.INTER_CUBIC)
            print(res)
            # Display the resulting frame
            cv2.imshow('frame',res)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything done, release the capture
        self.cap.release()
        cv2.destroyAllWindows()


