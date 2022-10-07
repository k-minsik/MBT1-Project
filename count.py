import numpy as np
# import sqldef
# import pymysql
from collections import deque


# conn = pymysql.connect(host='localhost', user='root', password='', db='mbt1', charset='utf8mb4')
# cursor = conn.cursor()



def getAngle(top, mid, bottom):
    top = np.array(top)
    mid = np.array(mid)
    bottom = np.array(bottom)
    
    radians = np.arctan2(bottom[1]-mid[1], bottom[0]-mid[0]) - np.arctan2(top[1]-mid[1], top[0]-mid[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle


def squat(RhipAngle, RkneeAngle, LhipAngle, LkneeAngle, reps, state):
    
    # print(state, RhipAngle, RkneeAngle, LhipAngle, LkneeAngle)
    if ((RhipAngle > 170)  and (RkneeAngle > 160)) or ((LhipAngle > 170)  and (LkneeAngle > 160)):
        if "Up" not in state and state[0] == "Squat":
            state.popleft()
            state.append("Up")
            reps += 1

    elif ((RkneeAngle < 80) and (RhipAngle < 80)) or ((LkneeAngle < 80) and (LhipAngle < 80)):
        if "Squat" not in state and state[0] == "Up":
            state.popleft()
            state.append("Squat")

    else:
        if "UNKNOWN" not in state:
            state.append("UNKNOWN")
        elif state[0] == "UNKNOWN":
            state.popleft()
            state.append("UNKNOWN")

    return reps, state


def benchpress(RelbowAngle, LelbowAngle, reps, state):
    
    # print(reps, state, RelbowAngle, LelbowAngle)
    if RelbowAngle > 170 or LelbowAngle > 170:
        if "Up" not in state and state[0] == "Down":
            state.popleft()
            state.append("Up")
            reps += 1

    elif RelbowAngle < 95 or LelbowAngle < 95:
        if "Down" not in state and state[0] == "Up":
            state.popleft()
            state.append("Down")

    else:
        if "UNKNOWN" not in state:
            state.append("UNKNOWN")
        elif state[0] == "UNKNOWN":
            state.popleft()
            state.append("UNKNOWN")

    return reps, state


def deadlift(RhipAngle, RkneeAngle, LhipAngle, LkneeAngle, reps, state):
    
    # print(reps, state, LhipAngle, LkneeAngle)

    if (RhipAngle < 60 and RkneeAngle < 150) or (LhipAngle < 60 and LkneeAngle < 150):
        if "Down" not in state and state[0] == "Up":
            state.popleft()
            state.append("Down")

    elif (RhipAngle > 160 and RkneeAngle > 160) or (LhipAngle > 160 and LkneeAngle > 160):
        if "Up" not in state and state[0] == "Down":
            state.popleft()
            state.append("Up")
            reps += 1

    else:
        if "UNKNOWN" not in state:
            state.append("UNKNOWN")
        elif state[0] == "UNKNOWN":
            state.popleft()
            state.append("UNKNOWN")

    return reps, state

def onerm(weight, reps):
    best = 0
    # NCSA 계산상수 활용
    if reps >= 12:  # 12회 이상은 12회로 계산
        best = weight / (0.7)
    elif reps == 11:
        best = weight / (0.73)
    elif reps == 10:
        best = weight / (0.75)
    elif reps == 9:
        best = weight / (0.77)
    elif reps == 8:
        best = weight / (0.80)
    elif reps == 7:
        best = weight / (0.83)
    elif reps == 6:
        best = weight / (0.85)
    elif reps == 5:
        best = weight / (0.87)
    elif reps == 4:
        best = weight / (0.90)
    elif reps == 3:
        best = weight / (0.93)
    elif reps == 2:
        best = weight / (0.95)
    elif reps == 1:
        best = weight

    return round(best, 1)


if __name__ == '__main__':
    pass