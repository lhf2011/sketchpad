
import sys
import math
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class GeoMath():

    def __init__(self):
        self.dist=0

    # function: twoPointClose, to tell if 2 points are close( distancec less than 7 pixels)
    # input: point1: point1 position
    #        point2: point2 position
    def twoPointClose(self,point1, point2):
        dist2 = pow(point1.x() - point2.x(), 2) + pow(point1.y() - point2.y(), 2)
        if dist2 < 49:
            return True
        else:
            return False

    # function: distBetweenPoints, to calculate the distance between 2 points
    # input: point1: point1 position
    #        point2: point2 position
    def distBetweenPoints(self,point1, point2):
        return math.sqrt( pow(point1.x()-point2.x(),2) + pow(point1.y()-point2.y(),2) )


    # function: minDistOfPoint2RectEdge, to tell if the point(current cursor) close to a rectangle
    # input: point: point(current cursor) position
    #        rect: rectangle position
    def minDistOfPoint2RectEdge(self, point, rect):
        dist2Bottom = self.calcDist(point, QLine(rect.bottomLeft(), rect.bottomRight()))
        dist2Top = self.calcDist(point, QLine(rect.topLeft(), rect.topRight()))
        dist2Left = self.calcDist(point, QLine(rect.topLeft(), rect.bottomLeft()))
        dist2Right = self.calcDist(point, QLine(rect.topRight(), rect.bottomRight()))
        minDist = min(min(dist2Bottom, dist2Top), min(dist2Left, dist2Right))
        return minDist

    # function: minDistOfPoint2SquareEdge, to tell if the point(current cursor) close to a square
    # input: point: point(current cursor) position
    #        square: square position
    def minDistOfPoint2SquareEdge(self, point, square):
        dist2Bottom = self.calcDist(point, QLine(square[2], square[3]))
        dist2Top = self.calcDist(point, QLine(square[0], square[1]))
        dist2Left = self.calcDist(point, QLine(square[0], square[2]))
        dist2Right = self.calcDist(point, QLine(square[1], square[3]))
        minDist = min(min(dist2Bottom, dist2Top), min(dist2Left, dist2Right))
        return minDist

    # function: calcDist, to calculate the distance between a point and a line
    # input: point: point position
    #        line: line position
    def calcDist(self, point, line):
        if point.x() < 0:
            return
        baselineVector = [line.p2().x()-line.p1().x() , line.p2().y()-line.p1().y()]
        sidelineVector = [point.x()-line.p1().x() , point.y()-line.p1().y()]
        dotResult = baselineVector[0] * sidelineVector[0] + baselineVector[1] * sidelineVector[1]
        baselineNormDist = baselineVector[0] * baselineVector[0] + baselineVector[1] * baselineVector[1]
        if dotResult<0:
            return math.sqrt(pow(line.p1().x() - point.x(), 2) + pow(line.p1().y() - point.y(), 2))
        if dotResult >= baselineNormDist:
            return math.sqrt(pow(line.p2().x() - point.x(), 2) + pow(line.p2().y() - point.y(), 2))
        else:
            A = line.p2().y() - line.p1().y()
            B = line.p1().x() - line.p2().x()
            C = (line.p1().y() - line.p2().y()) * line.p1().x() + (line.p2().x() - line.p1().x()) * line.p1().y()
            distance = round(abs(A * point.x() + B * point.y() + C) / (math.sqrt(A ** 2 + B ** 2) + 1e-6))
            return distance