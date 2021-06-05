import cv2
import numpy
from rubik_solver import utils
# from MagicCube.code.cube_interactive import Cube
# import matplotlib.pyplot as plt
# from matplotlib import widgets


def getPoints(lado, x, y, i, j):
    top = {
        'pt1': (y+(lado*i), x+(j*lado)),
        'pt2': (y+lado+(lado*i), x+(j*lado))
    }
    left = {
        'pt1': (y+(lado*i), x+(j*lado)),
        'pt2': (y+(lado*i), x+lado+(j*lado))
    }
    right = {
        'pt1': (y+lado+(lado*i), x+(j*lado)),
        'pt2': (y+lado+(lado*i), x+lado+(j*lado))
    }
    down = {
        'pt1': (y+(lado*i), x+lado+(j*lado)),
        'pt2': (y+lado+(lado*i), x+lado+(j*lado))
    }
    return {'top': top, 'down': down, 'left': left, 'right': right}


def drawCube(frame, lado, x, y):
    for j in range(3):
        for i in range(3):
            points = getPoints(lado, x, y, i, j)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            color = getColor(
                hsv, points['top']['pt1'][1]+(offset*2), points['top']['pt1'][0]+(offset*2))
            cv2.line(img=frame,
                     pt1=(points['top']['pt1']),
                     pt2=(points['top']['pt2']),
                     color=(0, 0, 0), thickness=calibre, lineType=8, shift=0)
            cv2.line(img=frame,
                     pt1=(points['left']['pt1']),
                     pt2=(points['left']['pt2']),
                     color=(0, 0, 0), thickness=calibre, lineType=8, shift=0)
            cv2.line(img=frame,
                     pt1=(points['right']['pt1']),
                     pt2=(points['right']['pt2']),
                     color=(0, 0, 0), thickness=calibre, lineType=8, shift=0)
            cv2.line(img=frame,
                     pt1=(points['down']['pt1']),
                     pt2=(points['down']['pt2']),
                     color=(0, 0, 0), thickness=calibre, lineType=8, shift=0)

            cv2.line(img=frame,
                     pt1=(points['top']['pt1'][0]+(offset*2),
                          points['top']['pt1'][1]+(offset*2)),
                     pt2=(points['top']['pt1'][0]+(offset*2),
                          points['top']['pt1'][1]+(offset*2)),
                     color=(0, 0, 0), thickness=calibre, lineType=8, shift=0)

            cv2.putText(frame, color, (points['top']['pt1'][0]+(offset*2),
                                                  points['top']['pt1'][1]+(offset*2)),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, 0, thickness=3)


def extratHSV(frame, x, y): #HSV
    colorH = frame[x, y, 0]
    colorS = frame[x, y, 1]
    colorV = frame[x, y, 2]
    return colorH, colorS

def getColor(frame, x, y):
    hue, sat = extratHSV(frame, x, y)
    if(sat <= 100):
        # print("BRANCO", hue, sat)
        return 'w'
    elif (hue >= 0 and hue < 8) or (hue > 160):
        # print('VERMELHO', hue, sat)
        return 'r'
    elif hue >= 8 and hue < 20:
        # print('LARANJA', hue, sat)
        return 'o'
    elif hue >= 20 and hue < 60:
        # print('AMARELO', hue, sat)
        return 'y'
    elif hue >= 60 and hue < 90:
        # print('VERDE', hue, sat)
        return 'g'
    elif hue >= 90 and hue < 160:
        # print('AZUL', hue, sat)
        return 'b'
    else:
        # print("BRANCO D", hue, sat)
        return 'w'

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)
lado = 100
x = 100
y = 170
calibre = 5
offset = int(lado/4)
cube = ''
solved = False

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else: 
    rval = False

while rval:
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)

    if key == 27: # exit on ESC
        break
    elif key == 114 or key == 82:
        solved = True
        # print(cube)
        try:
            formula = utils.solve(cube, 'Kociemba')
        except:
            print("Não foi possível RESOLVER o cubo")
        print("MOVES:")
        print(formula)
        # formula.reverse()
        # c = Cube(3)
        # for form in formula:
        #     f = str(form)
        #     if len(f) == 1:
        #         c.rotate_face(f, -1)
        #     else:
        #         if f[1] == "2":
        #             c.rotate_face(f[0], 1)
        #             c.rotate_face(f[0], 1)
        #         else:
        #             c.rotate_face(f[0], 1)
        # c.draw_interactive()
        # plt.show()
    elif key == 32: # exit on SPACE
        ret, frame = vc.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        print('SIDE SCANNED')
        for j in range(3):
            for i in range(3):
                points = getPoints(lado, x, y, i, j)
                cube += getColor(hsv, points['top']['pt1'][1]+(offset*2),
                              points['top']['pt1'][0]+(offset*2))
    elif not solved:
        drawCube(frame, lado, x, y)

vc.release()
cv2.destroyAllWindows()   
