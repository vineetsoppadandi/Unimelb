
import math
from shapely.geometry import Polygon, Point
import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

focalLen = 2.5
sensorHeight = 4.89
sensorWidth = 5.79
pixelHeight = 488
pixelWidth = 648
vFOV = 81
hFOV = 97


def slope(cord1, cord2):
    x1 = cord1[0]
    y1 = cord1[1]
    x2 = cord2[0]
    y2 = cord2[1]
    m = (y2-y1)/(x2-x1)

    return m

def drw(cord, d):
    d = 0.5
    #box1 = box(x1, y1, x2, y2)
    cord.append(cord[0])
    polygon = Polygon(cord) #repeat the first point to create a 'closed loop'
    polygon_b = polygon.buffer(d)
    plot_polys([polygon])
    plt.ylabel('m')
    plt.xlabel('m')
    plt.title('Optimal Path')


def plot_coords(coords):
    pts = list(coords)
    x, y = zip(*pts)
    plt.plot(x, y)


def plot_polys(polys):
    for poly in polys:
        if (not getattr(poly, "exterior", None)):
            print("got line?")

        plot_coords(poly.exterior.coords)

        for hole in poly.interiors:
            plot_coords(hole.coords)


# DISTANCE FORM THE OBJECT
def pho_dist(oh):
    cam_h = 1.2
    h = oh - cam_h
    deg = math.radians(vFOV/2)
    do = h/math.tan(deg)

    return do


# HORIZONTAL DIST COVER
def w_t(do):

    deg = math.radians(hFOV/2)
    cover = do*math.tan(deg)

    return cover


# CALCULATE THE PIXEL DENSITY
def pixel_den(do, oh, owt):

    ohp = (focalLen * oh * pixelHeight)/(do*sensorHeight)
    owp = (focalLen * owt * pixelWidth)/(do*sensorWidth)

    return ohp*owp


# DIST BETWEEN EACH COORD
def calculate_distance(cord1, cord2):

    x1 = cord1[0]
    y1 = cord1[1]
    x2 = cord2[0]
    y2 = cord2[1]
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    return dist


# RETURNS THE DIST OF EVER SEGMENT
def cordDist(cord):
    dist = []
    for i in range(len(cord)-1):
        cd = calculate_distance(cord[i], cord[i+1])
        dist.append(cd)

    return dist


def optimalP(segDist, w_t, do, cord, polygon):
    point = []
    for i in range(len(segDist)):
        if segDist[i]/w_t <= 1:
            x2 = cord[i+1][0]
            x1 = cord[i][0]
            y2 = cord[i+1][1]
            y1 = cord[i][1]

            xd = x2 - x1
            midX = xd/2 + x1

            yd = y2 - y1
            midY = yd/2 + y1

            if y1 == y2:
                p1 = Point(midX, y1 - (0.1*segDist[i]))   # THIS ONLY TAKES INTO ACCOUNT A POLYGON FROM 0,0 CORD !
                p2 = Point(midX, y1 + (0.1*segDist[i]))

                if polygon.contains(p1):
                    yp = y1 + do
                    xp = midX
                    point.append([])
                    point[i].append(xp)
                    point[i].append(yp)

                if polygon.contains(p2):
                    yp = y1 - do
                    xp = midX
                    point.append([])
                    point[i].append(xp)
                    point[i].append(yp)

            elif x1 == x2:
                p1 = Point(x1-(0.1*segDist[i]), midY)   # THIS ONLY TAKES INTO ACCOUNT A POLYGON FROM 0,0 CORD !
                p2 = Point(x1+(0.1*segDist[i]), midY)

                if polygon.contains(p1):
                    yp = midY
                    xp = x1 + do
                    point.append([])
                    point[i].append(xp)
                    point[i].append(yp)

                if polygon.contains(p2):
                    yp = midY
                    xp = x1 - do
                    point.append([])
                    point[i].append(xp)
                    point[i].append(yp)

            else:
                m = slope(cord[i], cord[i+1])
                c = midY - (-1/m)*midX

                #print('m,c', m, c)

                yT1 = -(1/m)*(midX-(0.1*segDist[i])) + c
                yT2 = -(1/m)*(midX+(0.1*segDist[i])) + c

                #print('test y coordinates', yT1, yT2)

                x1p = midX + math.sqrt(do**2/(1 + (1/m**2)))
                x2p = midX - math.sqrt(do**2/(1 + (1/m**2)))

                #print('2 x cordinates', x1p, x2p)

                p1 = Point((midX-(0.1*segDist[i])), yT1)
                p2 = Point((midX+(0.1*segDist[i])), yT2)

                if polygon.contains(p1):
                    if math.fabs((midX*1.1 - x1p)) > math.fabs((midX*1.1 - x2p)):
                        yp = -(1/m)*x2p + c
                        point.append([])
                        point[i].append(x2p)
                        point[i].append(yp)
                        #print(10)
                    else:
                        yp = -(1/m)*x1p + c
                        point.append([])
                        point[i].append(x1p)
                        point[i].append(yp)
                        #print(20)

                if polygon.contains(p2):
                    if math.fabs((midX*0.1 - x1p)) > math.fabs((midX*0.1 - x2p)):
                        yp = -(1/m)*x2p + c
                        point.append([])
                        point[i].append(x2p)
                        point[i].append(yp)
                        #print(30)
                    else:
                        yp = -(1/m)*x1p + c
                        point.append([])
                        point[i].append(x1p)
                        point[i].append(yp)
                        #print(40)

    return print('list', point)


# -----------MAIN----------------- #

# ----EXAMPLE TRIANGULAR HOUSE---- #

oh = 5  # SUBJECT HEIGHT
cord = [[0, 0], [1, 0], [1, 1], [0,1]]

cord.append(cord[0])

do = math.ceil(pho_dist(oh))  # MINIMUM DISTANCE TO MAINTAIN FROM THE OBJECT, GIVEN THE HEIGHT OF OBJECT
if do < 5:
    do = 5  # to over come collision with the house.
w_t = math.ceil(w_t(do))  # RETURNS THE HORIZONTAL COVERAGE GIVEN THE DISTANCE FROM THE SUBJECT
segDist = cordDist(cord)  # CALCULATE THE DIST OF EVER SEGMENT

polygon = Polygon(cord)
optimalP(segDist, w_t, do, cord, polygon)
