import cv2 as cv
import numpy as np
import math

class watermeter_machine_vision():
    def __init__(self, imgpath):
        self.SourceImg = cv.imread(imgpath)
        self.CordinateImg = cv.resize(self.SourceImg, (720, 720))
        self.GrayImg = cv.cvtColor(self.CordinateImg, cv.COLOR_BGR2GRAY)

    def _polar_coordiante_cal(self, x, y, r, theta):
        return int(x + r*np.cos(theta)), int(y + r*np.sin(theta))

    def _coordinate_quadrant(self, x, y, angle):
        if x<0:
            return angle + 90
        elif x>=0:
            return angle + 270

    def _angel2reading(self, angle):
        angle = angle - 90
        if angle <= 0:
            angle = angle + 360
        return 10 - angle / 36

    def _circle_ide(self, img):
        idecircles = cv.HoughCircles(img, cv.HOUGH_GRADIENT, 1, 60, param1=130, param2=38, minRadius=40,
                                     maxRadius=60)
        return sorted(np.uint16(np.around(idecircles))[0], key=lambda x: x[0], reverse=False)

    def _pointer_process(self, ROIimg, circle_radius):
        interlinecal = [[0 for i in range(2)] for i in range(80)]
        outerlinecal = [[0 for i in range(2)] for i in range(80)]
        j = 0
        k = 0

        HSVROI = cv.cvtColor(ROIimg, cv.COLOR_BGR2HSV)
        low_red_hsv = np.array([156, 43, 45])
        high_red_hsv = np.array([180, 255, 255])
        mask = cv.inRange(HSVROI, low_red_hsv, high_red_hsv)
        ColROI = cv.bitwise_and(ROIimg, ROIimg, mask=mask)
        ROIGrayImg = cv.cvtColor(ColROI, cv.COLOR_BGR2GRAY)
        ret, ROIbinary = cv.threshold(ROIGrayImg, 30, 255, cv.THRESH_BINARY)

        theta = np.arange(0, 2 * np.pi, np.pi / 180)
        inner_radius = 30
        outter_radius = 45

        for i in range(len(theta)):
            inner_x, inner_y = self._polar_coordiante_cal(0, 0, inner_radius, theta[i])
            outter_x, outter_y = self._polar_coordiante_cal(0, 0, outter_radius, theta[i])
            if ROIbinary[inner_x + circle_radius, inner_y + circle_radius] == 255:
                interlinecal[j][0], interlinecal[j][1] = inner_x + int(ROIbinary.shape[0] / 2), inner_y + int(
                    ROIbinary.shape[1] / 2)
                j = j + 1
            if ROIbinary[outter_x + circle_radius, outter_y + circle_radius] == 255:
                outerlinecal[k][0], outerlinecal[k][1] = outter_x + int(ROIbinary.shape[0] / 2), outter_y + int(
                    ROIbinary.shape[1] / 2)
                k = k + 1

        inter1, inter2, outer1, outer2 = 0, 0, 0, 0
        for l in range(j):
            inter1 = inter1 + interlinecal[l][0]
            inter2 = inter2 + interlinecal[l][1]
        for m in range(k):
            outer1 = outer1 + outerlinecal[m][0]
            outer2 = outer2 + outerlinecal[m][1]
        interlinestart = (int(ROIbinary.shape[0] / 2), int(ROIbinary.shape[1] / 2))
        inner_middle_point = int((int(inter1 / j) + int(outer1 / k)) / 2)
        outter_middle_point = int((int(inter2 / j) + int(outer2 / k)) / 2)
        finallineemd = (outter_middle_point, inner_middle_point)
        cv.line(ROIimg, interlinestart, finallineemd, (255, 255, 0), 4, 4)
        tanx = outter_middle_point - int(ROIbinary.shape[0] / 2)
        tany = inner_middle_point - int(ROIbinary.shape[1] / 2)
        trigonometric_angle = self._coordinate_quadrant(tany, tanx, (np.arctan(tanx / tany)) * (180 / np.pi))
        return self._angel2reading(trigonometric_angle)

    def _num_dect(self, circles):
        _final_reading = [0 for i in range(len(circles))]
        for cou in range(len(circles)):
            SourceImgROI = wm_ide_class.CordinateImg[
                           (circles[cou][1] - circles[cou][2]):(circles[cou][1] + circles[cou][2] + 2),
                           (circles[cou][0] - circles[cou][2]):(circles[cou][0] + circles[cou][2] + 2)]
            _final_reading[cou] = wm_ide_class._pointer_process(SourceImgROI, circles[cou][2])
        return _final_reading

    def _num_calibration(self, reading, circle):
        _calibration_num = []
        for i in range(len(reading) - 1):
            _calibration_num.append(reading[len(circle) - 1 - i] -
                                   (wm_ide_class._mathopeart(math.modf(reading[len(circle) - 1 - i])[0] -
                                                             reading[len(circle) - 2 - i] * 0.1)))
        _final_num_calibration = 0
        for i in range(len(_calibration_num)):
            _final_num_calibration = 10 ** (-(i + 1)) * int(_calibration_num[i]) + _final_num_calibration
        _final_num_calibration = final_reading[0] * 10 ** (-(len(_calibration_num) + 1)) + _final_num_calibration
        return _final_num_calibration

    def _draw_circle(self, img, ide_circle):
        for i in ide_circle:
            cv.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
            cv.circle(img, (i[0], i[1]), 2, (0, 0, 255), 2)
            for j in range(10):
                cv.line(img, (i[0] + int(i[2] * np.sin(np.pi / 5 * j) * 0.85),
                             i[1] + int(i[2] * np.cos(np.pi / 5 * j) * 0.85)),
                             (i[0] + int(i[2] * np.sin(np.pi / 5 * j)),
                             i[1] + int(i[2] * np.cos(np.pi / 5 * j))),
                            (0, 255, 0), 2)
                cv.line(img, (i[0] + int(i[2] * np.sin(np.pi / 5 * j + np.pi / 10) * 0.92),
                             i[1] + int(i[2] * np.cos(np.pi / 5 * j + np.pi / 10) * 0.92)),
                             (i[0] + int(i[2] * np.sin(np.pi / 5 * j + np.pi / 10)),
                             i[1] + int(i[2] * np.cos(np.pi / 5 * j + np.pi / 10))), (0, 255, 0), 2)

    def _mathopeart(self, num):
        if round(num) == -1:
            num = num +1
        elif round(num) == 1:
            num = num -1
        else:
            num = num
        return num

if __name__ == '__main__':
    imgpath = r'F:\Git\Python\watermeter\img\watermeter2.jpg'
    wm_ide_class = watermeter_machine_vision(imgpath)
    idecircles = wm_ide_class._circle_ide(wm_ide_class.GrayImg)
    wm_ide_class._draw_circle(wm_ide_class.CordinateImg, idecircles)
    final_reading = wm_ide_class._num_dect(idecircles)
    final_num_calibration = wm_ide_class._num_calibration(final_reading, idecircles)

    print('Calibration reading : %f' % final_num_calibration)

    cv.imshow('Source', wm_ide_class.CordinateImg)
    cv.waitKey(0)
    cv.destroyAllWindows()