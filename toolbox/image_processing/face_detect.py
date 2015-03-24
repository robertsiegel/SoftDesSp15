""" Experiment with face detection and image filtering using OpenCV.
	Author: Robbie Siegel
"""

import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier('/home/rsiegel/Downloads/haarcascade_frontalface_alt.xml')
kernel = np.ones((21,21),'uint8')
cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
	ret, frame = cap.read()
	#Use face detection to find  locations of faces in frame
	faces = face_cascade.detectMultiScale(frame, scaleFactor=1.2, minSize=(20,20))
	for (x,y,w,h) in faces:
		frame[y:y+h,x:x+w,:] = cv2.dilate(frame[y:y+h,x:x+w,:], kernel) #blurs face
		#draw weird looking face over blurred face
		cv2.circle(frame, (x+w/3, y+h/3), h/12, (255,255,255), -1, 8)
		cv2.circle(frame, (x+2*w/3, y+h/3), h/12, (255,255,255), -1, 8)
		cv2.circle(frame, (x+w/3, y+h/3), h/24, (255,150,0), -1, 8)
		cv2.circle(frame, (x+2*w/3, y+h/3), (h/24), (255,150,0), -1, 8)
		cv2.ellipse(frame, (x+w/2, y+3*h/4),(w/6,h/12),0,0,180,(0,0,255), 8)

	# Display the resulting frame
	cv2.imshow('frame',frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
	    break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()