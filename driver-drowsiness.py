import numpy as numpy
import dlib
import cv2
import math

cap = cv2.VideoCapture(0) 

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

def get_mid(p1,p2):
	return (int((p1.x+p2.x)/2), int((p1.y+p2.y)/2))

count=0
eye_closed=0
while True:

	_,frame = cap.read()
	frame = cv2.flip(frame,1)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	ratio_le=0
	ratio_re=0
	ratio_mo=0;
	faces = detector(gray)
	for face in faces:

		landmarks = predictor(gray, face)

		#LEFT EYE
		left_point_le = (landmarks.part(36).x, landmarks.part(36).y)
		right_point_le = (landmarks.part(39).x, landmarks.part(39).y)
		top_mid_le = get_mid(landmarks.part(37), landmarks.part(38))
		bottom_mid_le = get_mid(landmarks.part(41), landmarks.part(40))
		lenv_le = math.sqrt((top_mid_le[0] - bottom_mid_le[0])**2 + (top_mid_le[1] - bottom_mid_le[1])**2)
		lenh_le = math.sqrt((left_point_le[0]-right_point_le[0])**2 + (left_point_le[1] - right_point_le[1])**2)
		cv2.rectangle(frame,(landmarks.part(36).x-5, landmarks.part(37).y-5), (landmarks.part(39).x+5, landmarks.part(40).y+5), (255,0,0), 2)
		if lenv_le!=0:
			ratio_le = lenh_le/lenv_le
		out_le=str(ratio_le)


		#RIGHT EYE
		left_point_re = (landmarks.part(42).x, landmarks.part(42).y)
		right_point_re = (landmarks.part(45).x, landmarks.part(45).y)
		top_mid_re = get_mid(landmarks.part(43), landmarks.part(44))
		bottom_mid_re = get_mid(landmarks.part(47), landmarks.part(48))
		lenv_re = math.sqrt((top_mid_le[0] - bottom_mid_le[0])**2 + (top_mid_le[1] - bottom_mid_le[1])**2)
		lenh_re = math.sqrt((left_point_le[0]-right_point_le[0])**2 + (left_point_le[1] - right_point_le[1])**2)
		cv2.rectangle(frame,(landmarks.part(42).x-5, landmarks.part(43).y-5), (landmarks.part(45).x+5, landmarks.part(46).y+5), (255,0,0), 2)
		if lenv_re!=0:
			ratio_re = lenh_re/lenv_re
		out_re=str(ratio_re)


		cv2.putText(frame,"Left Eye Ratio : ",(1,15),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,255,0),2,cv2.LINE_AA)
		cv2.putText(frame,"Right Eye Ratio : ",(1,35),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,255,0),2,cv2.LINE_AA)
		cv2.putText(frame,out_le[:5],(130,15), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,255,0),2,cv2.LINE_AA)
		cv2.putText(frame,out_re[:5],(140,35), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,255,0),2,cv2.LINE_AA)


		#MOUTH 
		left_point_mo = (landmarks.part(48).x, landmarks.part(48).y)
		right_point_mo = (landmarks.part(64).x, landmarks.part(64).y)
		top_mid_mo = get_mid(landmarks.part(50), landmarks.part(52))
		bottom_mid_mo = (landmarks.part(57).x, landmarks.part(57).y)
		lenv_mo = math.sqrt((top_mid_mo[0] - bottom_mid_mo[0])**2 + (top_mid_mo[1] - bottom_mid_mo[1])**2)
		lenh_mo = math.sqrt((left_point_mo[0]-right_point_mo[0])**2 + (left_point_mo[1] - right_point_mo[1])**2)
		cv2.rectangle(frame,(landmarks.part(48).x-5, landmarks.part(51).y-10), (landmarks.part(54).x+5, landmarks.part(57).y+5), (255,0,0), 2)
		if lenv_mo!=0:
			ratio_mo = lenh_mo/lenv_mo
		out_mo=str(ratio_mo)
		cv2.putText(frame,"Mouth Ratio : ",(1,55),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,255,0),2,cv2.LINE_AA)
		cv2.putText(frame,out_mo[:5],(115,55), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,255,0),2,cv2.LINE_AA)

	if ratio_mo!=0 and ratio_le!=0 and ratio_re!=0 and ratio_mo<1.5 and ratio_le>4.5 and ratio_re>4.5:
		count+=1
	else:
		count=0

	if ratio_le!=0 and ratio_re!=0 and ratio_le>5 and ratio_re>5:
		eye_closed+=1
	else:
		eye_closed=0

	#cv2.putText(frame,"Count : ",(1,75),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,255,0),2,cv2.LINE_AA)
	#cv2.putText(frame,str(count),(60,75),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,255,0),2,cv2.LINE_AA)
	#cv2.putText(frame,"Count eyes : ",(1,95),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,255,0),2,cv2.LINE_AA)
	#cv2.putText(frame,str(eye_closed),(100,75),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,255,0),2,cv2.LINE_AA)

	if count>40:
		cv2.putText(frame,"DRIVER IS SLEEPY!",(1,115),cv2.FONT_HERSHEY_SIMPLEX, 0.7,(0,0,255),2,cv2.LINE_AA)

	if eye_closed>30:
		cv2.putText(frame,"DRIVER IS ASLEEP!",(1,135),cv2.FONT_HERSHEY_SIMPLEX, 0.7,(0,0,255),2,cv2.LINE_AA)		

	cv2.imshow("Frame",frame)

	key = cv2.waitKey(1)
	if key == 27:
		break;

cap.release()
cv2.destroyAllWindows()

