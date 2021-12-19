 # import os
import time

import cv2 as cv
import numpy as np
import datetime as dts
from matplotlib import pyplot as plt

def motionDetection():
    # 0 - for windows, -1 - for linux
    cap = cv.VideoCapture(-1)
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()
    
    fourcc = cv.VideoWriter_fourcc(*'DIVX')
    output = cv.VideoWriter()

    start_image_time = time.time() * 1000
    start_video_time = time.time() * 1000
    last_detection_time = 0
    write_video = False

    while cap.isOpened():
        
        diff = cv.absdiff(frame1, frame2)
        diff_gray = cv.cvtColor(diff, cv.COLOR_BGR2GRAY)
        blur = cv.GaussianBlur(diff_gray, (5, 5), 0)
        _, thresh = cv.threshold(blur, 20, 255, cv.THRESH_BINARY)
        dilated = cv.dilate(thresh, None, iterations=3)
        contours = cv.findContours(
            dilated, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        # print("test")
        process_video_time = time.time() * 1000
        
        if (write_video == True):
            output.write(frame1)
            
        if (write_video == True and last_detection_time > 0 and (process_video_time - last_detection_time) > 20000):
            # print("stop video")
            output.release()
            write_video = False
        
        for contour in contours[1]:
            (x, y, w, h) = cv.boundingRect(contour)
            if cv.contourArea(contour) < 900:
                continue
                     
            # print("write")
            process_time = time.time() * 1000
            last_detection_time = time.time() * 1000
            
            if (write_video == False):
                start_video_time = time.time() * 1000
                output.release()
                now = dts.datetime.utcnow()
                videoFileName = "video_{}{}".format(now.strftime("%d-%m-%Y_%H-%M-%S"), ".avi")
                output = cv.VideoWriter(videoFileName, fourcc, 25.0, (640,480))
                write_video = True

            if (write_video == True):
                output.write(frame1)

            if ((process_time - start_image_time) > 1000):
                now = dts.datetime.utcnow()
                fileName = "image_{}{}".format(now.strftime("%d-%m-%Y_%H-%M-%S"), ".jpg")
                cv.imwrite(fileName, frame1)
                start_image_time = time.time() * 1000

            #cv.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
            #cv.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv.FONT_HERSHEY_SIMPLEX,
            #           1, (255, 0, 0), 3)

        #cv.drawContours(frame1, contours[1], -1, (0, 255, 0), 2)

        cv.imshow("Video", frame1)
        frame1 = frame2
        ret, frame2 = cap.read()

        if cv.waitKey(20) == ord('q'):
            break

    output.release()
    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    motionDetection()