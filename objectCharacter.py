import geoMath
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class ObjectCha:
    def __init__(self, objIndex, objShape,penColor, penWidth, penStyle):
        self.objIndex = objIndex
        self.objShape = objShape
        self.penColor = penColor
        self.penWidth = penWidth
        self.penStyle = penStyle

class FreeHandLineCha(ObjectCha):
    def __init__(self,objIndex, objShape, penColor, penWidth, penStyle, freeHandLine):
        ObjectCha.__init__(self,objIndex, objShape, penColor, penWidth, penStyle)
        self.freeHandLine=freeHandLine
    def moveObject(self, chosenObjectIndex, moveX, moveY):
        if len(chosenObjectIndex)==0:
            return
        if self.objIndex in chosenObjectIndex:
            for point in self.freeHandLine:
                point.setX(point.x() + moveX)
                point.setY(point.y() + moveY)
    def point2ObjectDistance(self, point):
        dist = 100
        geoCalc = geoMath.GeoMath()
        for pointOnLine in self.freeHandLine:
            pointDist = geoCalc.distBetweenPoints(point, pointOnLine)
            dist = min(dist, pointDist)
        return dist

class StraightLineCha(ObjectCha):
    def __init__(self,objIndex, objShape, penColor, penWidth, penStyle, straightLine):
        ObjectCha.__init__(self,objIndex, objShape, penColor, penWidth, penStyle)
        self.straightLine = straightLine
    def moveObject(self, chosenObjectIndex, moveX, moveY):
        if len(chosenObjectIndex)==0:
            return
        if self.objIndex in chosenObjectIndex:
            self.straightLine.setLine(self.straightLine.p1().x() + moveX, self.straightLine.p1().y() + moveY,
                                    self.straightLine.p2().x() + moveX, self.straightLine.p2().y() + moveY)
    def point2ObjectDistance(self, point):
        geoCalc = geoMath.GeoMath()
        dist = geoCalc.calcDist( point=point, line=self.straightLine)
        return dist

class RectangleCha(ObjectCha):
    def __init__(self,objIndex, objShape, penColor, penWidth, penStyle, rectangle):
        ObjectCha.__init__(self,objIndex, objShape, penColor, penWidth, penStyle)
        self.rectangle = rectangle
    def moveObject(self, chosenObjectIndex, moveX, moveY):
        if len(chosenObjectIndex)==0:
            return
        if self.objIndex in chosenObjectIndex:
            newRectCenter = QPoint(self.rectangle.center().x() + moveX,
                                   self.rectangle.center().y() + moveY)
            self.rectangle.moveCenter(newRectCenter)
    def point2ObjectDistance(self, point):
        geoCalc = geoMath.GeoMath()
        dist= geoCalc.minDistOfPoint2RectEdge(point,self.rectangle)
        return dist

class SquareCha(ObjectCha):
    def __init__(self,objIndex, objShape, penColor, penWidth, penStyle, square):
        ObjectCha.__init__(self,objIndex, objShape, penColor, penWidth, penStyle)
        self.square = square
    def moveObject(self, chosenObjectIndex, moveX, moveY):
        if len(chosenObjectIndex)==0:
            return
        if self.objIndex in chosenObjectIndex:
            for vertex in self.square:
                vertex.setX(vertex.x() + moveX)
                vertex.setY(vertex.y() + moveY)
    def point2ObjectDistance(self, point):
        geoCalc = geoMath.GeoMath()
        dist = geoCalc.minDistOfPoint2SquareEdge(point, self.square)
        return dist

class EllipseCha(ObjectCha):
    def __init__(self,objIndex, objShape, penColor, penWidth, penStyle, ellipse):
        ObjectCha.__init__(self,objIndex, objShape, penColor, penWidth, penStyle)
        self.ellipse = ellipse
    def moveObject(self, chosenObjectIndex, moveX, moveY):
        if len(chosenObjectIndex)==0:
            return
        if self.objIndex in chosenObjectIndex:
            newEllipseCenter = QPoint(self.ellipse.center().x() + moveX, self.ellipse.center().y() + moveY)
            self.ellipse.moveCenter(newEllipseCenter)
    def point2ObjectDistance(self, point):
        geoCalc = geoMath.GeoMath()
        dist= geoCalc.distBetweenPoints(point, self.ellipse.center())
        return dist

class CircleCha(ObjectCha):
    def __init__(self,objIndex, objShape, penColor, penWidth, penStyle, circle, radius):
        ObjectCha.__init__(self,objIndex, objShape, penColor, penWidth, penStyle)
        self.circle = circle
        self.radius = radius
    def moveObject(self, chosenObjectIndex, moveX, moveY):
        if len(chosenObjectIndex)==0:
            return
        if self.objIndex in chosenObjectIndex:
            newCircleCenter = QPoint(self.circle.center().x() + moveX, self.circle.center().y() + moveY)
            self.circle.moveCenter(newCircleCenter)
    def point2ObjectDistance(self, point):
        geoCalc = geoMath.GeoMath()
        dist = abs(round(geoCalc.distBetweenPoints(self.circle.center(), point))-self.radius)
        return dist

class PolygonCha(ObjectCha):
    def __init__(self,objIndex, objShape, penColor, penWidth, penStyle, polygon):
        ObjectCha.__init__(self,objIndex, objShape, penColor, penWidth, penStyle)
        self.polygon = polygon
    def moveObject(self, chosenObjectIndex, moveX, moveY):
        if len(chosenObjectIndex)==0:
            return
        if self.objIndex in chosenObjectIndex:
            for vertex in self.polygon:
                vertex.setX(vertex.x() + moveX)
                vertex.setY(vertex.y() + moveY)
    def point2ObjectDistance(self, point):
        dist=100
        geoCalc = geoMath.GeoMath()
        for vertex in range(len(self.polygon)):
            dist2AnEdge = geoCalc.calcDist(point,QLine(self.polygon[vertex], self.polygon[(vertex + 1) % len(self.polygon)]))
            dist = min(dist, dist2AnEdge)
        return dist

class GroupCha(ObjectCha):
    def __init__(self,objIndex, objShape, penColor, penWidth, penStyle, area,memberIndexes):
        ObjectCha.__init__(self, objIndex, objShape, penColor, penWidth, penStyle)
        self.area=area
        self.memberIndexes=memberIndexes
    def moveObject(self, chosenObjectIndex, moveX, moveY):
        if len(chosenObjectIndex)==0:
            return
        if self.objIndex in chosenObjectIndex:
            newGroupCenter = QPoint(self.area.center().x() + moveX, self.area.center().y() + moveY)
            self.area.moveCenter(newGroupCenter)
    def point2ObjectDistance(self, point):
        geoCalc = geoMath.GeoMath()
        dist = geoCalc.minDistOfPoint2RectEdge(point, self.area)
        return dist