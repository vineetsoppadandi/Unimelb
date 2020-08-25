from shapely.geometry import Polygon
import math
import matplotlib.pyplot as plt
fig, ax = plt.subplots()

vAngular = 1.33
hAngular = 0.16
vFOV = 10.67

def drw(cord, d):

    cord.append(cord[0])
    polygon = Polygon(cord) #repeat the first point to create a 'closed loop'
    polygon_b = polygon.buffer(d)
    plot_polys([polygon_b, polygon])
    plt.ylabel('Meter')
    plt.xlabel('Meter')
    plt.title('LIDAR Optimal Path - Concave structure')


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


def reso(B_height):

    v_laser = vFOV/vAngular
    H = B_height-1.5
    reso_v = v_laser/H

    dh = H*math.tan(math.radians(vFOV))
    dh = round(dh)

    thetaV = math.atan(0.5/dh)
    thetaV = 2*math.degrees(thetaV)

    h_laser = thetaV/hAngular
    reso_h = h_laser

    reso = reso_v*reso_h

    if reso > 250:
        print('Resolution ok = ', reso)
        return dh

    elif reso < 250:
        print('Manual override, please enter yes or no?')
        uI = input()
        if uI == 'yes':
            print('All yours')
        if uI == 'no':
            return dh


building_height = 5

d = reso(building_height)

coord = [[0, 0], [0, 5], [5, 5], [5, 0]]

drw(coord, d)

plt.show()
