import cv2
import mediapipe as mp
from flask import Flask, jsonify, render_template, Response, request
import pymysql
import count
import sqldef
from collections import deque
import config

conn = pymysql.connect(host=config.DATABASE_CONFIG['host'],
                        user=config.DATABASE_CONFIG['user'], 
                        password=config.DATABASE_CONFIG['password'], 
                        db=config.DATABASE_CONFIG['dbname'], charset='utf8mb4')
cursor = conn.cursor()

app = Flask(__name__)
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

reps_s = 0
reps_b = 0
reps_d = 0
state = deque(["UP"])
data = []
result = []

def gen_frames(event):
    global reps_s, reps_b, reps_d, state, data, result
    state = deque(["Up"])
    data = []
    result = []

    if event == "Squat":
        reps_s = 0
        camera = cv2.VideoCapture('./test_video/squat.mp4')
        # camera = cv2.VideoCapture(0)
    elif event == "BenchPress":
        reps_b = 0
        camera = cv2.VideoCapture('./test_video/pushup.mp4')
    elif event == "Deadlift":
        reps_d
        camera = cv2.VideoCapture('./test_video/deadlift.mp4')


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

            cv2.rectangle(frame, (width-width//3,height-height//3), (width,height), (255,255,255), -1)
            cv2.putText(frame, 'REPS', (int(width-width//3.1),int(height-height//3.6)), cv2.FONT_HERSHEY_SIMPLEX, 1.6, (0,0,0), 2, cv2.LINE_AA)
            if event == "Squat":
                cv2.putText(frame, str(reps_s), (int(width-width//4),int(height-height//9)), cv2.FONT_HERSHEY_SIMPLEX, 4, (0,0,0), 4, cv2.LINE_AA)
            elif event == "BenchPress":
                cv2.putText(frame, str(reps_b), (int(width-width//4),int(height-height//9)), cv2.FONT_HERSHEY_SIMPLEX, 4, (0,0,0), 4, cv2.LINE_AA)
            elif event == "Deadlift":
                cv2.putText(frame, str(reps_d), (int(width-width//4),int(height-height//9)), cv2.FONT_HERSHEY_SIMPLEX, 4, (0,0,0), 4, cv2.LINE_AA)
            
            cv2.putText(frame, state[-1], (0,int(height//10)), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)

            try:
                landmarks = results.pose_landmarks.landmark
                # print(landmarks)
                mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())


                if event == "Squat":
                    rightShoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                    rightHip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                    rightKnee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                    rightAnkle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                    
                    leftShoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    leftHip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                    leftKnee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                    leftAnkle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

                    RkneeAngle = count.getAngle(rightHip, rightKnee, rightAnkle)
                    RhipAngle = count.getAngle(rightShoulder, rightHip, rightKnee)
                    
                    LkneeAngle = count.getAngle(leftHip, leftKnee, leftAnkle)
                    LhipAngle = count.getAngle(leftShoulder, leftHip, leftKnee)

                    Rh = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].visibility
                    Lh = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].visibility

                elif event == "Deadlift":
                    rightShoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                    rightHip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                    rightKnee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                    rightAnkle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                    
                    leftShoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    leftHip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                    leftKnee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                    leftAnkle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

                    RkneeAngle = count.getAngle(rightHip, rightKnee, rightAnkle)
                    RhipAngle = count.getAngle(rightShoulder, rightHip, rightKnee)
                    
                    LkneeAngle = count.getAngle(leftHip, leftKnee, leftAnkle)
                    LhipAngle = count.getAngle(leftShoulder, leftHip, leftKnee)

                    Rh = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].visibility
                    Lh = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].visibility
    
                elif event == "BenchPress":
                    rightShoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                    rightHip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                    rightElbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                    rightWrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                    
                    leftShoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    leftHip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                    leftElbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    leftWrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                    RelbowAngle = count.getAngle(rightShoulder, rightElbow, rightWrist)
                    LelbowAngle = count.getAngle(leftShoulder, leftElbow, leftWrist)

                    Re = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].visibility
                    Le = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].visibility


                if event == "Squat":
                    #Squat
                    reps_s, state, data, result = count.squat(RhipAngle, RkneeAngle, Rh, LhipAngle, LkneeAngle, Lh, reps_s, state, data, result)
                elif event == "BenchPress":
                    #BenchPress
                    reps_b, state, data, result= count.benchpress(RelbowAngle, Re, LelbowAngle, Le, reps_b, state, data, result)
                elif event == "Deadlift":
                    #DeadLift
                    reps_d, state, data, result = count.deadlift(RhipAngle, RkneeAngle, Rh, LhipAngle, LkneeAngle, Lh, reps_d, state, data, result)
                
            except:
                pass

            resize_frame = cv2.resize(frame, (390, 460), interpolation=cv2.INTER_CUBIC)
            _, buffer = cv2.imencode('.jpg', resize_frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

                




@app.route('/')
def index():
    return render_template('index.html')


# Video
@app.route('/Squat')
def video_feed_s():
    return Response(gen_frames("Squat"), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/BenchPress')
def video_feed_b():
    return Response(gen_frames("BenchPress"), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/Deadlift')
def video_feed_d():
    return Response(gen_frames("Deadlift"), mimetype='multipart/x-mixed-replace; boundary=frame')


# Measurement Page
@app.route('/reps/Squat', methods=['GET'])
def cnt_squat():
    return jsonify(data = reps_s)

@app.route('/reps/BenchPress', methods=['GET'])
def cnt_bench():
    return jsonify(data = reps_b)

@app.route('/reps/Deadlift', methods=['GET'])
def cnt_dead():
    return jsonify(data = reps_d)

# Result Page
@app.route('/result/<name>', methods=['POST'])
def result(name):
    params = request.get_json()
    sqldef.saveData(cursor, conn, params['event'], params['oneRM'], name)
    f = open('test.csv', 'w')

    for i in data:    
        f.write(str(i).replace(' ', '')[1:-1] + '\n')
    f.close()

    f = open('result.csv', 'w')
    for i in result:
        f.write(str(i) + '\n')
    f.close()
    
    return params


# Profile Page
@app.route('/profile/Squat/<name>', methods=['GET'])
def userData_S(name):
    squatt = sqldef.get_userData_s(cursor, conn, name)
    print(squatt)
    return jsonify(data = squatt)

@app.route('/profile/BenchPress/<name>', methods=['GET'])
def userData_B(name):
    Benchp = sqldef.get_userData_b(cursor, conn, name)
    print(Benchp)
    return jsonify(data = Benchp)

@app.route('/profile/Deadlift/<name>', methods=['GET'])
def userData_D(name):
    Deadl = sqldef.get_userData_d(cursor, conn, name)
    print(Deadl)
    return jsonify(data = Deadl)

@app.route('/profile/Total/<name>', methods=['GET'])
def userData_T(name):
    total = sqldef.get_userData_t(cursor, conn, name)
    print(total)
    return jsonify(data = total)
    
# Rank Page
@app.route('/rank', methods=['GET'])
def rank_data():
    ranking = sqldef.rank_sys(cursor, conn)
    print(ranking)
    return jsonify(data = ranking)

@app.route('/map')
def print_map():
    return render_template('map.html')

# Login Page
@app.route('/login', methods = ['GET', 'POST'])
def log_in():
    params_user = request.get_json()
    login = sqldef.log_in(cursor, conn, params_user['UID'], params_user['UPW'])
    return jsonify(loginStat = login)


if __name__ == "__main__":
    app.run(host='localhost', port=8000)

    # total= sqldef.get_userData_t(cursor, conn, 'kms')
    # print(total)
    # print(type(total))

    # squat = sqldef.get_userData_s(cursor, conn, 'kms')
    # print(squat)
    # print(type(squat))

    # bench = sqldef.get_userData_b(cursor, conn, 'kms')
    # print(bench)
    # print(type(bench))
    
    # dead = sqldef.get_userData_d(cursor, conn, 'kms')
    # print(dead)
    # print(type(dead))

    # print(sqldef.rank_sys(cursor, conn))
    # print(sqldef.login(cursor, conn, 'kms', '1234'))
    # print(sqldef.login(cursor, conn, 'psy', '2345'))


