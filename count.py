import numpy as np
import sqldef
import pymysql
from collections import deque


conn = pymysql.connect(host='localhost', user='root', password='', db='mbt1', charset='utf8mb4')
cursor = conn.cursor()




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
    if ((RhipAngle > 170)  and (RkneeAngle > 160)):
        if "UP" not in state and state[0] == "SQUAT":
            state.popleft()
            state.append("UP")
            reps += 1
    elif ((LhipAngle > 170)  and (LkneeAngle > 160)):
        if "UP" not in state and state[0] == "SQUAT":
            state.popleft()
            state.append("UP")
            reps += 1

    elif ((RkneeAngle < 80) and (RhipAngle < 80)):
        if "SQUAT" not in state and state[0] == "UP":
            state.popleft()
            state.append("SQUAT")

    elif((LkneeAngle < 80) and (LhipAngle < 80)):
        if "SQUAT" not in state and state[0] == "UP":
            state.popleft()
            state.append("SQUAT")

    else:
        if "UNKNOWN" not in state:
            state.append("UNKNOWN")
        elif state[0] == "UNKNOWN":
            state.popleft()
            state.append("UNKNOWN")

    return reps, state


def benchpress(RelbowAngle, LelbowAngle, reps, status, side):
    
    if RelbowAngle < 100:
        side = 1
        status = "Down"
    elif LelbowAngle < 100:
        side = 2
        status = "Down"


    if RelbowAngle > 160 and status == 'Down' and side == 1:
        status = "UP"
        reps += 1
    elif LelbowAngle > 160 and status == 'Down' and side == 2:
        status = "UP"
        reps += 1
    
    # print(elbowAngle)
    return reps, status, side


def deadlift(RhipAngle, RkneeAngle, LhipAngle, LkneeAngle, reps, status, side):
    
    if (RhipAngle < 100 and RkneeAngle < 150):
        side = 1
        status = "Down"
    elif (LhipAngle < 100 and LkneeAngle < 150):
        side = 2
        status = "Down"


    if (RhipAngle > 170 and RkneeAngle > 170) and status == 'Down' and side == 1:
        status = "UP"
        reps += 1
    elif (LhipAngle > 170 and LkneeAngle > 170) and status == 'Down' and side == 2:
        status = "UP"
        reps += 1
    
    # print(hipAngle, kneeAngle)
    return reps, status, side

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
    
    print(int(2.9))