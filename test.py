import cv2
import mediapipe as mp
import count
import pymysql
import sqldef
from collections import deque


conn = pymysql.connect(host='localhost', user='root', password='', db='mbt1', charset='utf8mb4')
cursor = conn.cursor()

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

reps = 0
side = 0
state = deque(["UP"])


# camera = cv2.VideoCapture(0)
camera = cv2.VideoCapture('./test_video/squat.mp4')
# camera = cv2.VideoCapture('./test_video/bete.mp4')
# camera = cv2.VideoCapture('./test_video/dete.mp4')


with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
  while True:
    success, frame = camera.read()
    if not success:
      continue

    frame.flags.writeable = False
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame)

    frame.flags.writeable = True
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # print(frame.shape) # 이미지 세로, 가로, channel
    height, width, _ = frame.shape

    # REPS
    cv2.rectangle(frame, (width-width//3,height-height//3), (width,height), (255,255,255), -1)
    cv2.putText(frame, 'REPS', (int(width-width//3.1),int(height-height//3.6)), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 2, cv2.LINE_AA)
    cv2.putText(frame, str(reps), (int(width-width//4),int(height-height//9)), cv2.FONT_HERSHEY_SIMPLEX, 5, (0,0,0), 4, cv2.LINE_AA)

    # state
    cv2.putText(frame, state[-1], (0,int(height//10)), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)

    # 1RM
    cv2.rectangle(frame, (width-width//3, 0), (width,height//3), (255,255,255), -1)
    cv2.putText(frame, '1RM', (int(width-width//4),int(height//10)), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 2, cv2.LINE_AA)
    cv2.putText(frame, str(count.onerm(100,reps)), (int(width-width//3),int(height//3.5)), cv2.FONT_HERSHEY_SIMPLEX, 5, (0,0,0), 4, cv2.LINE_AA)


    try:
        landmarks = results.pose_landmarks.landmark
        # print(landmarks)
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

        rightShoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        rightElbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
        rightWrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
        rightHip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        rightKnee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
        rightAnkle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
        rightToe = [landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].y]
        leftShoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        leftElbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        leftWrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        leftHip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        leftKnee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        leftAnkle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
        leftToe = [landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x,landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y]
        
        RkneeAngle = count.getAngle(rightHip, rightKnee, rightAnkle)
        RhipAngle = count.getAngle(rightShoulder, rightHip, rightKnee)
        RelbowAngle = count.getAngle(rightShoulder, rightElbow, rightWrist)
        # RankleAngle = count.getAngle(rightKnee, rightAnkle, rightToe)

        LkneeAngle = count.getAngle(leftHip, leftKnee, leftAnkle)
        LhipAngle = count.getAngle(leftShoulder, leftHip, leftKnee)
        LelbowAngle = count.getAngle(leftShoulder, leftElbow, leftWrist)
        # LankleAngle = count.getAngle(leftKnee, leftAnkle, leftToe)
        
        # #Squat

        reps, state = count.squat(RhipAngle, RkneeAngle, LhipAngle, LkneeAngle, reps, state)

        # #BenchPress
        # reps, state, side = count.benchpress(RelbowAngle, LelbowAngle, reps, state, side)

        # DeadLift
        # reps, state, side = count.deadlift(RhipAngle, RkneeAngle, LhipAngle, LkneeAngle, reps, state, side)
        
    except:
        pass

    cv2.imshow('MediaPipe Pose', frame)
    if cv2.waitKey(5) & 0xFF == 27:
      break
camera.release()


def classifyPose(landmarks, output_image, display=False): 
    # Initialize the label of the pose. It is not known at this stage.
    label = 'Unknown Pose'

    # Specify the color (Red) with which the label will be written on the image.
    color = (0, 0, 255)
    
    # Get the angle between the left shoulder, elbow and wrist points. 
    left_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                      landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                      landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value])
    
    # Get the angle between the right shoulder, elbow and wrist points. 
    right_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                       landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                                       landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value])   
    
    # Get the angle between the left elbow, shoulder and hip points. 
    left_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                         landmarks[mp_pose.PoseLandmark.LEFT_HIP.value])

    # Get the angle between the right hip, shoulder and elbow points. 
    right_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                          landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                          landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value])

    # Get the angle between the left hip, knee and ankle points. 
    left_knee_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                     landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value],
                                     landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value])

    # Get the angle between the right hip, knee and ankle points 
    right_knee_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                      landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value],
                                      landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value])
    
    #----------------------------------------------------------------------------------------------------------------
    
    # Check if it is the warrior II pose or the T pose.
    # As for both of them, both arms should be straight and shoulders should be at the specific angle.
    #----------------------------------------------------------------------------------------------------------------
    
    # Check if the both arms are straight.
    if left_elbow_angle > 165 and left_elbow_angle < 195 and right_elbow_angle > 165 and right_elbow_angle < 195:
        if left_shoulder_angle > 80 and left_shoulder_angle < 110 and right_shoulder_angle > 80 and right_shoulder_angle < 110:


            if left_knee_angle > 165 and left_knee_angle < 195 or right_knee_angle > 165 and right_knee_angle < 195:
                if left_knee_angle > 90 and left_knee_angle < 120 or right_knee_angle > 90 and right_knee_angle < 120:
                    label = 'Warrior II Pose' 
                        
    
            if left_knee_angle > 160 and left_knee_angle < 195 and right_knee_angle > 160 and right_knee_angle < 195:
                label = 'T Pose'


    if left_knee_angle > 165 and left_knee_angle < 195 or right_knee_angle > 165 and right_knee_angle < 195:
        if left_knee_angle > 315 and left_knee_angle < 335 or right_knee_angle > 25 and right_knee_angle < 45:
            label = 'Tree Pose'


    if label != 'Unknown Pose':
        color = (0, 255, 0)  
    
    return label