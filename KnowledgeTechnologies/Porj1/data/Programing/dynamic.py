import math
from shapely.geometry import Polygon
import numpy as np
from scipy.integrate import quad
import math
import matplotlib.pyplot as plt
fig, ax = plt.subplots()

show_animation = 1


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


class eta3_path(object):
    """
    eta3_path

    input
        segments: list of `eta3_path_segment` instances definining a continuous path
    """

    def __init__(self, segments):
        # ensure input has the correct form
        assert(isinstance(segments, list) and isinstance(
            segments[0], eta3_path_segment))
        # ensure that each segment begins from the previous segment's end (continuity)
        for r, s in zip(segments[:-1], segments[1:]):
            assert(np.array_equal(r.end_pose, s.start_pose))
        self.segments = segments

    def calc_path_point(self, u):
        """
        eta3_path::calc_path_point

        input
            normalized interpolation point along path object, 0 <= u <= len(self.segments)
        returns
            2d (x,y) position vector
        """

        assert(u >= 0 and u <= len(self.segments))
        if np.isclose(u, len(self.segments)):
            segment_idx = len(self.segments) - 1
            u = 1.
        else:
            segment_idx = int(np.floor(u))
            u -= segment_idx
        return self.segments[segment_idx].calc_point(u)


class eta3_path_segment(object):
    """
    eta3_path_segment - constructs an eta^3 path segment based on desired shaping, eta, and curvature vector, kappa.
                        If either, or both, of eta and kappa are not set during initialization, they will
                        default to zeros.

    input
        start_pose - starting pose array  (x, y, \theta)
        end_pose - ending pose array (x, y, \theta)
        eta - shaping parameters, default=None
        kappa - curvature parameters, default=None
    """

    def __init__(self, start_pose, end_pose, eta=None, kappa=None):
        # make sure inputs are of the correct size
        assert(len(start_pose) == 3 and len(start_pose) == len(end_pose))
        self.start_pose = start_pose
        self.end_pose = end_pose
        # if no eta is passed, initialize it to array of zeros
        if not eta:
            eta = np.zeros((6,))
        else:
            # make sure that eta has correct size
            assert(len(eta) == 6)
        # if no kappa is passed, initialize to array of zeros
        if not kappa:
            kappa = np.zeros((4,))
        else:
            assert(len(kappa) == 4)
        # set up angle cosines and sines for simpler computations below
        ca = np.cos(start_pose[2])
        sa = np.sin(start_pose[2])
        cb = np.cos(end_pose[2])
        sb = np.sin(end_pose[2])
        # 2 dimensions (x,y) x 8 coefficients per dimension
        self.coeffs = np.empty((2, 8))
        # constant terms (u^0)
        self.coeffs[0, 0] = start_pose[0]
        self.coeffs[1, 0] = start_pose[1]
        # linear (u^1)
        self.coeffs[0, 1] = eta[0] * ca
        self.coeffs[1, 1] = eta[0] * sa
        # quadratic (u^2)
        self.coeffs[0, 2] = 1. / 2 * eta[2] * \
            ca - 1. / 2 * eta[0]**2 * kappa[0] * sa
        self.coeffs[1, 2] = 1. / 2 * eta[2] * \
            sa + 1. / 2 * eta[0]**2 * kappa[0] * ca
        # cubic (u^3)
        self.coeffs[0, 3] = 1. / 6 * eta[4] * ca - 1. / 6 * \
            (eta[0]**3 * kappa[1] + 3. * eta[0] * eta[2] * kappa[0]) * sa
        self.coeffs[1, 3] = 1. / 6 * eta[4] * sa + 1. / 6 * \
            (eta[0]**3 * kappa[1] + 3. * eta[0] * eta[2] * kappa[0]) * ca
        # quartic (u^4)
        self.coeffs[0, 4] = 35. * (end_pose[0] - start_pose[0]) - (20. * eta[0] + 5 * eta[2] + 2. / 3 * eta[4]) * ca \
            + (5. * eta[0]**2 * kappa[0] + 2. / 3 * eta[0]**3 * kappa[1] + 2. * eta[0] * eta[2] * kappa[0]) * sa \
            - (15. * eta[1] - 5. / 2 * eta[3] + 1. / 6 * eta[5]) * cb \
            - (5. / 2 * eta[1]**2 * kappa[2] - 1. / 6 * eta[1] **
               3 * kappa[3] - 1. / 2 * eta[1] * eta[3] * kappa[2]) * sb
        self.coeffs[1, 4] = 35. * (end_pose[1] - start_pose[1]) - (20. * eta[0] + 5. * eta[2] + 2. / 3 * eta[4]) * sa \
            - (5. * eta[0]**2 * kappa[0] + 2. / 3 * eta[0]**3 * kappa[1] + 2. * eta[0] * eta[2] * kappa[0]) * ca \
            - (15. * eta[1] - 5. / 2 * eta[3] + 1. / 6 * eta[5]) * sb \
            + (5. / 2 * eta[1]**2 * kappa[2] - 1. / 6 * eta[1] **
               3 * kappa[3] - 1. / 2 * eta[1] * eta[3] * kappa[2]) * cb
        # quintic (u^5)
        self.coeffs[0, 5] = -84. * (end_pose[0] - start_pose[0]) + (45. * eta[0] + 10. * eta[2] + eta[4]) * ca \
            - (10. * eta[0]**2 * kappa[0] + eta[0]**3 * kappa[1] + 3. * eta[0] * eta[2] * kappa[0]) * sa \
            + (39. * eta[1] - 7. * eta[3] + 1. / 2 * eta[5]) * cb \
            + (7. * eta[1]**2 * kappa[2] - 1. / 2 * eta[1]**3 *
               kappa[3] - 3. / 2 * eta[1] * eta[3] * kappa[2]) * sb
        self.coeffs[1, 5] = -84. * (end_pose[1] - start_pose[1]) + (45. * eta[0] + 10. * eta[2] + eta[4]) * sa \
            + (10. * eta[0]**2 * kappa[0] + eta[0]**3 * kappa[1] + 3. * eta[0] * eta[2] * kappa[0]) * ca \
            + (39. * eta[1] - 7. * eta[3] + 1. / 2 * eta[5]) * sb \
            - (7. * eta[1]**2 * kappa[2] - 1. / 2 * eta[1]**3 *
               kappa[3] - 3. / 2 * eta[1] * eta[3] * kappa[2]) * cb
        # sextic (u^6)
        self.coeffs[0, 6] = 70. * (end_pose[0] - start_pose[0]) - (36. * eta[0] + 15. / 2 * eta[2] + 2. / 3 * eta[4]) * ca \
            + (15. / 2 * eta[0]**2 * kappa[0] + 2. / 3 * eta[0]**3 * kappa[1] + 2. * eta[0] * eta[2] * kappa[0]) * sa \
            - (34. * eta[1] - 13. / 2 * eta[3] + 1. / 2 * eta[5]) * cb \
            - (13. / 2 * eta[1]**2 * kappa[2] - 1. / 2 * eta[1] **
               3 * kappa[3] - 3. / 2 * eta[1] * eta[3] * kappa[2]) * sb
        self.coeffs[1, 6] = 70. * (end_pose[1] - start_pose[1]) - (36. * eta[0] + 15. / 2 * eta[2] + 2. / 3 * eta[4]) * sa \
            - (15. / 2 * eta[0]**2 * kappa[0] + 2. / 3 * eta[0]**3 * kappa[1] + 2. * eta[0] * eta[2] * kappa[0]) * ca \
            - (34. * eta[1] - 13. / 2 * eta[3] + 1. / 2 * eta[5]) * sb \
            + (13. / 2 * eta[1]**2 * kappa[2] - 1. / 2 * eta[1] **
               3 * kappa[3] - 3. / 2 * eta[1] * eta[3] * kappa[2]) * cb
        # septic (u^7)
        self.coeffs[0, 7] = -20. * (end_pose[0] - start_pose[0]) + (10. * eta[0] + 2. * eta[2] + 1. / 6 * eta[4]) * ca \
            - (2. * eta[0]**2 * kappa[0] + 1. / 6 * eta[0]**3 * kappa[1] + 1. / 2 * eta[0] * eta[2] * kappa[0]) * sa \
            + (10. * eta[1] - 2. * eta[3] + 1. / 6 * eta[5]) * cb \
            + (2. * eta[1]**2 * kappa[2] - 1. / 6 * eta[1]**3 *
               kappa[3] - 1. / 2 * eta[1] * eta[3] * kappa[2]) * sb
        self.coeffs[1, 7] = -20. * (end_pose[1] - start_pose[1]) + (10. * eta[0] + 2. * eta[2] + 1. / 6 * eta[4]) * sa \
            + (2. * eta[0]**2 * kappa[0] + 1. / 6 * eta[0]**3 * kappa[1] + 1. / 2 * eta[0] * eta[2] * kappa[0]) * ca \
            + (10. * eta[1] - 2. * eta[3] + 1. / 6 * eta[5]) * sb \
            - (2. * eta[1]**2 * kappa[2] - 1. / 6 * eta[1]**3 *
               kappa[3] - 1. / 2 * eta[1] * eta[3] * kappa[2]) * cb

        self.s_dot = lambda u: max(np.linalg.norm(self.coeffs[:, 1:].dot(np.array(
            [1, 2. * u, 3. * u**2, 4. * u**3, 5. * u**4, 6. * u**5, 7. * u**6]))), 1e-6)
        self.f_length = lambda ue: quad(lambda u: self.s_dot(u), 0, ue)
        self.segment_length = self.f_length(1)[0]

    def calc_point(self, u):
        """
        eta3_path_segment::calc_point

        input
            u - parametric representation of a point along the segment, 0 <= u <= 1
        returns
            (x,y) of point along the segment
        """
        assert(u >= 0 and u <= 1)
        return self.coeffs.dot(np.array([1, u, u**2, u**3, u**4, u**5, u**6, u**7]))

    def calc_deriv(self, u, order=1):
        """
        eta3_path_segment::calc_deriv

        input
            u - parametric representation of a point along the segment, 0 <= u <= 1
        returns
            (d^nx/du^n,d^ny/du^n) of point along the segment, for 0 < n <= 2
        """

        assert(u >= 0 and u <= 1)
        assert(order > 0 and order <= 2)
        if order == 1:
            return self.coeffs[:, 1:].dot(np.array([1, 2. * u, 3. * u**2, 4. * u**3, 5. * u**4, 6. * u**5, 7. * u**6]))

        return self.coeffs[:, 2:].dot(np.array([2, 6. * u, 12. * u**2, 20. * u**3, 30. * u**4, 42. * u**5]))


def calculatedistance(x1, y1, x2, y2):
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    dist = round(dist)
    return dist


def drw(cord):
    cord.append(cord[0])
    polygon = Polygon(cord) #repeat the first point to create a 'closed loop'
    plot_polys([polygon])
    plt.ylabel('Meter')
    plt.xlabel('Meter')
    plt.title('Optimal Path Points')


def WORK(cord, d):
    print('work')
    path_segments = []
    # segment 1: lane-change curve

    deg_1 = math.radians(90)
    deg_2 = math.radians(180)

    start_pose = [0.5, -5, deg_1]
    end_pose = [6, 0.5, deg_2]
    # NOTE: The ordering on kappa is [kappa_A, kappad_A, kappa_B, kappad_B], with kappad_* being the curvature derivative
    kappa = [0, 0, 0, 0]
    n = calculatedistance(start_pose[0], start_pose[1], end_pose[0], end_pose[1])
    eta = [n, n, 0, -100, -100, -100]
    path_segments.append(eta3_path_segment(
        start_pose=start_pose, end_pose=end_pose, eta=eta, kappa=kappa))

    deg_3 = deg_2
    deg_4 = math.radians(315)

    start_pose = [6, 0.5, deg_3]
    end_pose = [-3.03555, 4.0355, deg_4]
    # NOTE: The ordering on kappa is [kappa_A, kappad_A, kappa_B, kappad_B], with kappad_* being the curvature derivative
    kappa = [0, 0, 0, 0]
    n = calculatedistance(start_pose[0], start_pose[1], end_pose[0], end_pose[1])
    eta = [n, n, 0, -100, -100, -100]
    path_segments.append(eta3_path_segment(
        start_pose=start_pose, end_pose=end_pose, eta=eta, kappa=kappa))

    path = eta3_path(path_segments)

    deg_5 = deg_4
    deg_6 = math.radians(90)

    start_pose = [-3.03555, 4.0355, deg_5]
    end_pose = [0.5, -5, deg_6]
    # NOTE: The ordering on kappa is [kappa_A, kappad_A, kappa_B, kappad_B], with kappad_* being the curvature derivative
    kappa = [0, 0, 0, 0]
    n = calculatedistance(start_pose[0], start_pose[1], end_pose[0], end_pose[1])
    eta = [n, n, 0, -100, -100, -100]
    path_segments.append(eta3_path_segment(
        start_pose=start_pose, end_pose=end_pose, eta=eta, kappa=kappa))

    # interpolate at several points along the path
    ui = np.linspace(0, len(path_segments), 1001)
    pos = np.empty((2, ui.size))
    for j, u in enumerate(ui):
        pos[:, j] = path.calc_path_point(u)

    if show_animation:
        # plot the path
        plt.plot(pos[0, :], pos[1, :])
        #plt.show()
        print('test')


def main():

    #coord = [[0, 0],[0, 10], [5,10], [5, 5], [10, 5], [0, 10]]
    #plt.plot([2.5, 7.5, 20.5, 20.5, 2.5, 7.5, -10.5, -10.5], [-10.5, -10.5, 2.5, 7.5, 20.5, 20.5, 7.5, 2.5], 'ro')
    coord = [[0, 0], [1, 0], [1, 1]]
    drw(coord)

    WORK(coord, 5)
    plt.show()

if __name__ == '__main__':
    main()





