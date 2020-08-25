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

def drw(coord):
    coord.append(coord[0])
    polygon = Polygon(coord) #repeat the first point to create a 'closed loop'
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
    cover = 2*cover
    return round(cover*2)/2


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

def optimal(cord, ct, do):
    propotion = []
    disSeg = cordDist(cord)

    for i in range(len(disSeg)):
        propotion.append(round(disSeg[i]/ct))
    cnt = 0
    point = []
    print(propotion)
    for i in range(len(disSeg)):
        x2 = cord[i+1][0]
        x1 = cord[i][0]
        y2 = cord[i+1][1]
        y1 = cord[i][1]

        if propotion[i] <= 1:
            if y1 == y2:
                if x2 > x1:
                    ymid = y1
                    xmid = (x1+x2)*0.5

                    point.append([])
                    xp = xmid
                    yp = ymid - do
                    point[i].append(xp)
                    point[i].append(yp)

            if y1 == y2:
                if x2 < x1:
                    ymid = y1
                    xmid = (x1+x2)*0.5

                    point.append([])
                    xp = xmid
                    yp = ymid + do
                    point[i].append(xp)
                    point[i].append(yp)

            if x1 == x2:
                if y2 > y1:
                    ymid = (y1+y2)*0.5
                    xmid = x1

                    point.append([])
                    xp = xmid + do
                    yp = ymid
                    point[i].append(xp)
                    point[i].append(yp)

            if x1 == x2:
                if y2 < y1:
                    ymid = (y1+y2)*0.5
                    xmid = x1

                    point.append([])
                    xp = xmid - do
                    yp = ymid
                    point[i].append(xp)
                    point[i].append(yp)


        if propotion[i] > 1:
            #cnt = 0
            for j in range(propotion[i]):
                if y1 == y2:
                    if x2 > x1:
                        xw1 = x1 + (j+1)*ct
                        xw2 = x1 + j*ct
                  #      xw = xw1 - xw2

                        ymid = y1
                        xmid = (xw1+xw2)*0.5

                        point.append([])
                        xp = xmid
                        yp = ymid - do
                        point[cnt].append(xp)
                        point[cnt].append(yp)

                if y1 == y2:
                    if x2 < x1:
                        xw1 = x1 + (j+1)*ct
                        xw2 = x1 + j*ct
                      #  xw = xw1 - xw2

                        ymid = y1
                        xmid = (xw1+xw2)*0.5

                        point.append([])
                        xp = xmid
                        yp = ymid + do
                        point[cnt].append(xp)
                        point[cnt].append(yp)

                if x1 == x2:
                    if y2 > y1:
                        yw1 = y1 + (j+1)*ct
                        yw2 = y1 + j*ct
                      #  yw = yw1 - yw2

                        ymid = (yw1+yw2)*0.5
                        xmid = x1

                        point.append([])
                        xp = xmid - do
                        yp = ymid
                        point[cnt].append(xp)
                        point[cnt].append(yp)

                if x1 == x2:
                    if y2 < y1:
                        yw1 = y1 - (j+1)*ct
                        yw2 = y1 - j*ct
#                     #   yw = yw1 - yw2

                        ymid = (yw1+yw2)*0.5
                        xmid = x1

                        point.append([])
                        xp = xmid + do
                        yp = ymid
                        point[cnt].append(xp)
                        point[cnt].append(yp)
                cnt = cnt + 1
    return print('answer', point)


# ----MAIN--- #
heightOfobject = 5

distanceFromObject = pho_dist(heightOfobject)

if distanceFromObject < 5:
    distanceFromObject = 5  # to over come collision with the house.

coverT = w_t(distanceFromObject)

cord = [[0, 0],[10, 0], [10, 5], [5, 5], [5, 10],[0, 10]]

#cord = [[0, 0], [1, 0], [1, 1], [0, 1]]
cord.append(cord[0])
optimal(cord, coverT, distanceFromObject)

plt.plot([5, 15, 7.5, 10, 2.5, -5], [-5, 2.5, 10, 7.5, 15, 5], 'ro')
drw(cord)
plt.show()

# answer [[0.5, -5], [6, 0.5], [0.5, 6], [-5, 0.5]]
# answer [[5.0, -5], [15, 2.5], [7.5, 10], [10, 7.5], [2.5, 15], [-5, 5.0]]





