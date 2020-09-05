# https://www.cnblogs.com/hhh5460/p/4273799.html

import sys
import math
import geoMath
import widgetSet
import objectCharacter

from copy import deepcopy

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class PaintArea(QWidget):
    def __init__(self):
        super(PaintArea, self).__init__()
        self.ShapeList = ["FreeHandLine", "Line", "Rectangle", "Ellipse", "Square", "Circle","Polygon", "Group", "Choose"]
        self.setPalette(QPalette(Qt.white))
        self.setAutoFillBackground(True)
        self.setMinimumSize(800, 600)
        self.grabKeyboard() # 只有控件开始捕获键盘，控件的键盘事件才能收到消息

        self.straightLines = []
        self.freeHandLines = []
        self.freeHandLine = []
        self.rects = []
        self.squares = []
        self.ellipses = []
        self.circles = []
        self.polygons = []
        self.polygon = []
        self.groups = []

        # general parameter
        self.startQPoint = QPoint(-1, -1)
        self.endQPoint = QPoint(-1, -1)
        self.objectIndex=0
        self.chooseObjectIndex=[]
        self.copyObjectIndex = []

    def moveObjectMembers(self,groupedObjectIndex,moveX,moveY):
        if len(groupedObjectIndex) == 0:
            return
        # move group
        for group in self.groups:
            group.moveObject(groupedObjectIndex,moveX,moveY)
        # move ellipse
        for ellipse in self.ellipses:
            ellipse.moveObject(groupedObjectIndex,moveX,moveY)
        # move circle
        for circle in self.circles:
            circle.moveObject(groupedObjectIndex,moveX,moveY)
        # move rectangular
        for rect in self.rects:
            rect.moveObject(groupedObjectIndex,moveX,moveY)
        # move square
        for square in self.squares:
            square.moveObject(groupedObjectIndex,moveX,moveY)
        # move straight line
        for straightLine in self.straightLines:
            straightLine.moveObject(groupedObjectIndex,moveX,moveY)
        # move freehand line
        for freehandLine in self.freeHandLines:
            freehandLine.moveObject(groupedObjectIndex,moveX,moveY)
        # move polygon
        for polygon in self.polygons:
            polygon.moveObject(groupedObjectIndex,moveX,moveY)

    def chooseAnObject(self, cursorPos):
        minDist= 100

        # choose ellipse
        for elps in self.ellipses:
            dist=elps.point2ObjectDistance(point=cursorPos)
            if dist < minDist:
                minDist=dist
                self.chooseObjectIndex = [elps.objIndex]
        # choose circle
        for circle in self.circles:
            dist = circle.point2ObjectDistance(point=cursorPos)
            if dist < minDist:
                minDist = dist
                self.chooseObjectIndex = [circle.objIndex]
        # choose rectangular
        for rect in self.rects:
            dist=rect.point2ObjectDistance(point=cursorPos)
            if dist < minDist:
                minDist=dist
                self.chooseObjectIndex = [rect.objIndex]
        # choose square
        for square in self.squares:
            dist=square.point2ObjectDistance(point=cursorPos)
            if dist < minDist:
                minDist = dist
                self.chooseObjectIndex = [square.objIndex]
        # choose straight line
        for sl in self.straightLines:
            dist=sl.point2ObjectDistance(point=cursorPos)
            if dist < minDist:
                minDist=dist
                self.chooseObjectIndex = [sl.objIndex]
        # choose freehand line
        for fhl in self.freeHandLines:
            dist=fhl.point2ObjectDistance(point=cursorPos)
            if dist < minDist:
                minDist=dist
                self.chooseObjectIndex = [fhl.objIndex]
        # choose polygon
        for plg in self.polygons:
            dist=plg.point2ObjectDistance(point=cursorPos)
            if dist < minDist:
                minDist=dist
                self.chooseObjectIndex= [plg.objIndex]
        # choose group
        for gp in self.groups:
            dist=gp.point2ObjectDistance(point=cursorPos)
            if dist < minDist:
                minDist = dist
                self.chooseObjectIndex = gp.memberIndexes

    def copyObjectChosen(self, copyObjectIndex):
        if len(copyObjectIndex) == 0:
            return
        self.copyObjectIndex = copyObjectIndex

    def deleteObjectChosen(self, delObjectIndex):
        if len(delObjectIndex) == 0:
            return
        # delete ellipse
        ellipsesList= self.ellipses[:]
        for elps in ellipsesList:
            if elps.objIndex in delObjectIndex:
                self.ellipses.remove(elps)
                self.chooseObjectIndex.remove(elps.objIndex)
        # delete circle
        circlesList= self.circles[:]
        for circle in circlesList:
            if circle.objIndex in delObjectIndex:
                self.circles.remove(circle)
                self.chooseObjectIndex.remove(circle.objIndex)
        # delete rectangular
        rectsList = self.rects[:]
        for rect in rectsList:
            if rect.objIndex in delObjectIndex:
                self.rects.remove(rect)
                self.chooseObjectIndex.remove(rect.objIndex)
        # delete square
        squaresList = self.squares[:]
        for square in squaresList:
            if square.objIndex in delObjectIndex:
                self.squares.remove(square)
                self.chooseObjectIndex.remove(square.objIndex)
        # delete straight line
        LinesList = self.straightLines[:]
        for sl in LinesList:
            if sl.objIndex in delObjectIndex:
                self.straightLines.remove(sl)
                self.chooseObjectIndex.remove(sl.objIndex)
        # delete freehand line
        freeHandLinesList = self.freeHandLines[:]
        for fhl in freeHandLinesList:
            if fhl.objIndex in delObjectIndex:
                self.freeHandLines.remove(fhl)
                self.chooseObjectIndex.remove(fhl.objIndex)
        # delete polygon
        polygonsList = self.polygons[:]
        for plg in polygonsList:
            if plg.objIndex in delObjectIndex:
                self.polygons.remove(plg)
                self.chooseObjectIndex.remove(plg.objIndex)
        # delete group
        groupsList = self.groups[:]
        for gp in groupsList:
            if gp.objIndex in delObjectIndex:
                self.groups.remove(gp)
                self.chooseObjectIndex.remove(gp.objIndex)

    def pasteObjectChosen(self, pasteObjectIndex, moveX, moveY):
        if len(pasteObjectIndex) == 0:
            return
        newIndexInGroup=[]
        # paste ellipse
        for elps in self.ellipses:
            if elps.objIndex in pasteObjectIndex:
                newEllipse = deepcopy(elps)
                self.objectIndex = self.objectIndex + 1
                newEllipse.objIndex = self.objectIndex
                newEllipse.moveObject([newEllipse.objIndex], moveX, moveY)
                self.ellipses.append(newEllipse)
                newIndexInGroup.append(self.objectIndex)

        # paste circle
        for circle in self.circles:
            if circle.objIndex in pasteObjectIndex:
                newCircle = deepcopy(circle)
                self.objectIndex = self.objectIndex + 1
                newCircle.objIndex = self.objectIndex
                newCircle.moveObject([newCircle.objIndex], moveX, moveY)
                self.circles.append(newCircle)
                newIndexInGroup.append(self.objectIndex)

        # paste rectangular
        for rect in self.rects:
            if rect.objIndex in pasteObjectIndex:
                newRect = deepcopy(rect)
                self.objectIndex = self.objectIndex + 1
                newRect.objIndex = self.objectIndex
                newRect.moveObject([newRect.objIndex], moveX, moveY)
                self.rects.append(newRect)
                newIndexInGroup.append(self.objectIndex)

        # paste square
        for square in self.squares:
            if square.objIndex in pasteObjectIndex:
                newSquare = deepcopy(square)
                self.objectIndex = self.objectIndex + 1
                newSquare.objIndex = self.objectIndex
                newSquare.moveObject([newSquare.objIndex], moveX, moveY)
                self.squares.append(newSquare)
                newIndexInGroup.append(self.objectIndex)

        # paste straight line
        for sl in self.straightLines:
            if sl.objIndex in pasteObjectIndex:
                newSl = deepcopy(sl)
                self.objectIndex = self.objectIndex + 1
                newSl.objIndex = self.objectIndex
                newSl.moveObject([newSl.objIndex], moveX, moveY)
                self.straightLines.append(newSl)
                newIndexInGroup.append(self.objectIndex)

        # paste freehand line
        for fhl in self.freeHandLines:
            if fhl.objIndex in pasteObjectIndex:
                newFHL = deepcopy(fhl)
                self.objectIndex = self.objectIndex + 1
                newFHL.objIndex = self.objectIndex
                newFHL.moveObject([newFHL.objIndex], moveX, moveY)
                self.freeHandLines.append(newFHL)
                newIndexInGroup.append(self.objectIndex)

        # paste polygon
        for plg in self.polygons:
            if plg.objIndex in pasteObjectIndex:
                newPolygon = deepcopy(plg)
                self.objectIndex = self.objectIndex + 1
                newPolygon.objIndex = self.objectIndex
                newPolygon.moveObject([newPolygon.objIndex], moveX, moveY)
                self.polygons.append(newPolygon)
                newIndexInGroup.append(self.objectIndex)

        # paste group
        for gp in self.groups:
            if gp.objIndex in pasteObjectIndex:
                newGroup = deepcopy(gp)
                self.objectIndex = self.objectIndex + 1
                newGroup.objIndex = self.objectIndex
                newIndexInGroup.append(self.objectIndex)
                newGroup.moveObject([newGroup.objIndex], moveX, moveY)
                newGroup.memberIndexes = newIndexInGroup  # all new paste object index in group are updated here!!
                self.groups.append(newGroup)

    def setShape(self, s):
        self.shape = s
        self.update()

    def setPen(self, p):
        self.pen = p
        self.update()

    def paintEvent(self, QPaintEvent):
        # draw free hand line
        for freeHandLine in self.freeHandLines:
            freeHandLinePainter = QPainter()
            freeHandLinePainter.begin(self)
            freeHandLinePainter.setPen(QPen(freeHandLine.penColor, freeHandLine.penWidth, freeHandLine.penStyle))
            for i in range(len(freeHandLine.freeHandLine) - 1):
                freeHandLinePainter.drawLine(freeHandLine.freeHandLine[i], freeHandLine.freeHandLine[i + 1])
            freeHandLinePainter.end()
        # draw straight line
        for straightLine in self.straightLines:
            straightLinePainter = QPainter()
            straightLinePainter.begin(self)
            straightLinePainter.setPen(QPen(straightLine.penColor, straightLine.penWidth, straightLine.penStyle))
            straightLinePainter.drawLine(straightLine.straightLine)
            straightLinePainter.end()
        # draw rectangular
        for rect in self.rects:
            rectangularPainter = QPainter()
            rectangularPainter.begin(self)
            rectangularPainter.setPen(QPen(rect.penColor, rect.penWidth, rect.penStyle))
            rectangularPainter.drawRect(rect.rectangle)
            rectangularPainter.end()
        # draw square
        for square in self.squares:
            squarePainter = QPainter()
            squarePainter.begin(self)
            squarePainter.setPen(QPen(square.penColor, square.penWidth, square.penStyle))
            # squarePainter.drawPolygon(square.square)
            for pointIndex in range(4):
                squarePainter.drawLine(square.square[pointIndex],square.square[(pointIndex + 1) % 4])
            squarePainter.end()
        # draw ellipses
        for ellipse in self.ellipses:
            ellipsePainter = QPainter()
            ellipsePainter.begin(self)
            ellipsePainter.setPen(QPen(ellipse.penColor, ellipse.penWidth, ellipse.penStyle))
            ellipsePainter.drawEllipse(ellipse.ellipse)
            ellipsePainter.end()
        # draw circle
        for circle in self.circles:
            circlePainter = QPainter()
            circlePainter.begin(self)
            circlePainter.setPen(QPen(circle.penColor, circle.penWidth, circle.penStyle))
            circlePainter.drawEllipse(circle.circle)
            circlePainter.end()
        # draw polygons
        for polygon in self.polygons:
            polygonPainter = QPainter()
            polygonPainter.begin(self)
            polygonPainter.setPen(QPen(polygon.penColor, polygon.penWidth, polygon.penStyle))
            for pointIndex in range(len(polygon.polygon)):
                polygonPainter.drawLine(polygon.polygon[pointIndex], polygon.polygon[(pointIndex + 1) % len(polygon.polygon)])
            polygonPainter.end()
        for pointIndex in range(len(self.polygon) - 1):
            painter = QPainter()
            painter.begin(self)
            painter.setPen(self.pen)
            painter.drawLine(self.polygon[pointIndex], self.polygon[(pointIndex + 1) % len(self.polygon)])
            painter.end()
        # draw group
        for group in self.groups:
            groupPainter = QPainter()
            groupPainter.begin(self)
            groupPainter.setPen(QPen(group.penColor, group.penWidth, group.penStyle))
            groupPainter.drawRect(group.area)
            groupPainter.end()
        self.update()

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.modifiers() == Qt.ControlModifier and QKeyEvent.key() == Qt.Key_C:  # 两键组合
            self.copyObjectChosen(self.chooseObjectIndex)
        if QKeyEvent.modifiers() == Qt.ControlModifier and QKeyEvent.key() == Qt.Key_V:  # 两键组合
            self.pasteObjectChosen(self.copyObjectIndex, 10, 10)
        if (QKeyEvent.key() == Qt.Key_Delete):
            self.deleteObjectChosen(self.chooseObjectIndex)

    def mousePressEvent(self, event):
        # single click to choose a object
        if self.shape == "Choose":
            pos = QPoint(event.pos().x(), event.pos().y())
            if self.startQPoint.x() < 0:
                self.startQPoint = pos
            self.endQPoint = pos


    def mouseDoubleClickEvent(self, event):
        # double click to cancel choose a group
        if self.shape == "Choose":
            pos = QPoint(event.pos().x(), event.pos().y())
            if self.startQPoint.x() < 0:
                self.startQPoint = pos
            self.endQPoint = pos

            if self.startQPoint.x() < 0:
                return
            for gp in self.groups:
                geoCalc = geoMath.GeoMath()
                dist = geoCalc.minDistOfPoint2RectEdge(self.startQPoint, gp.area)
                if dist < 49:
                    self.groups.remove(gp)
            self.startQPoint = QPoint(-1, -1)
            self.endQPoint = QPoint(-1, -1)


    def mouseMoveEvent(self, event):
        if (self.shape == "Line") or (self.shape == "Rectangle") or (self.shape == "Square") or (self.shape == "Ellipse") \
                or (self.shape == "Circle") or (self.shape == "Polygon" ) or (self.shape == "Group") or(self.shape == "Choose"):
            pos=QPoint(event.pos().x(), event.pos().y())
            if self.startQPoint.x() < 0:
                self.startQPoint=pos
            self.endQPoint=pos
        if self.shape == "FreeHandLine":
            pos=QPoint(event.pos().x(), event.pos().y())
            self.freeHandLine.append(pos)
        self.update()

    def mouseReleaseEvent(self, event):
        if self.shape == "Line":
            self.objectIndex=self.objectIndex+1
            self.straightLines.append(
                objectCharacter.StraightLineCha(objIndex=self.objectIndex, objShape="Line", penColor=self.pen.color(),
                                                penWidth=self.pen.width(), penStyle=self.pen.style(),
                                                straightLine=QLine(self.startQPoint, self.endQPoint)))
            self.startQPoint = QPoint(-1, -1)
            self.endQPoint = QPoint(-1, -1)
        if self.shape == "FreeHandLine":
            self.objectIndex = self.objectIndex + 1
            self.freeHandLines.append(
                objectCharacter.FreeHandLineCha(objIndex=self.objectIndex, objShape="FreeHandLine",
                                                penColor=self.pen.color(), penWidth=self.pen.width(),
                                                penStyle=self.pen.style(), freeHandLine=self.freeHandLine))
            self.freeHandLine=[]
        if self.shape == "Rectangle":
            self.objectIndex = self.objectIndex + 1
            self.rects.append(
                objectCharacter.RectangleCha(objIndex=self.objectIndex, objShape="Rectangle", penColor=self.pen.color(),
                                             penWidth=self.pen.width(), penStyle=self.pen.style(),
                                             rectangle=QRect(self.startQPoint, self.endQPoint)))
            self.startQPoint = QPoint(-1, -1)
            self.endQPoint = QPoint(-1, -1)
        if self.shape == "Square":
            self.objectIndex = self.objectIndex + 1
            point1 = self.startQPoint
            point3 = self.endQPoint
            point2 = QPoint(round(((point1.x()+point3.x())+(point3.y()-point1.y()))/2), round(((point1.y()+point3.y())+(point1.x()-point3.x()))/2))
            point4 = QPoint(round(((point1.x()+point3.x())-(point3.y()-point1.y()))/2), round(((point1.y()+point3.y())-(point1.x()-point3.x()))/2))
            self.squares.append(
                objectCharacter.SquareCha(objIndex=self.objectIndex, objShape="Square", penColor=self.pen.color(),
                                          penWidth=self.pen.width(),
                                          penStyle=self.pen.style(), square=[point1, point2, point3, point4]))
            self.startQPoint = QPoint(-1, -1)
            self.endQPoint = QPoint(-1, -1)
        if self.shape == "Ellipse":
            self.objectIndex = self.objectIndex + 1
            self.ellipses.append(
                objectCharacter.EllipseCha(objIndex=self.objectIndex, objShape="Ellipse", penColor=self.pen.color(),
                                           penWidth=self.pen.width(), penStyle=self.pen.style(),
                                           ellipse=QRect(self.startQPoint, self.endQPoint)))
            self.startQPoint = QPoint(-1, -1)
            self.endQPoint = QPoint(-1, -1)
        if self.shape == "Circle":
            self.objectIndex = self.objectIndex + 1
            center=QPoint( round((self.startQPoint.x() + self.endQPoint.x()) / 2), round((self.startQPoint.y() + self.endQPoint.y()) / 2) )
            geoCalc=geoMath.GeoMath()
            squareRadius = round(geoCalc.distBetweenPoints(self.startQPoint, self.endQPoint) / 2)
            topLeftPoint = QPoint( center.x()-squareRadius , center.y()-squareRadius)
            bottomRightPoint = QPoint(center.x() + squareRadius, center.y() + squareRadius)
            boundingRect = QRect(topLeftPoint,bottomRightPoint)
            self.circles.append(
                objectCharacter.CircleCha(objIndex=self.objectIndex, objShape="Circle", penColor=self.pen.color(),
                                          penWidth=self.pen.width(),
                                          penStyle=self.pen.style(), circle=boundingRect,radius=squareRadius))
            self.startQPoint = QPoint(-1, -1)
            self.endQPoint = QPoint(-1, -1)
        if self.shape == "Polygon":
            if len(self.polygon)==0:
                if self.startQPoint.x() < 0 or self.endQPoint.x()<0:
                    return
                self.polygon.append(self.startQPoint)
                self.polygon.append(self.endQPoint)
                self.startQPoint = QPoint(-1, -1)
                self.endQPoint = QPoint(-1, -1)
            else:
                if self.startQPoint.x() < 0 or self.endQPoint.x() < 0:
                    return
                startPointOverlap= False
                endPointOverlap= False
                for polygonPoints in self.polygon:
                    geoCalc= geoMath.GeoMath()
                    startPointOverlap = startPointOverlap or geoCalc.twoPointClose(polygonPoints, self.startQPoint)
                    endPointOverlap = endPointOverlap or geoCalc.twoPointClose(polygonPoints, self.endQPoint)
                if startPointOverlap and endPointOverlap:
                    self.objectIndex = self.objectIndex + 1
                    self.polygons.append(objectCharacter.PolygonCha(objIndex=self.objectIndex, objShape="Polygon",
                                                                    penColor=self.pen.color(),
                                                                    penWidth=self.pen.width(),
                                                                    penStyle=self.pen.style(), polygon=self.polygon))
                    self.polygon = []
                    self.startQPoint = QPoint(-1, -1)
                    self.endQPoint = QPoint(-1, -1)
                elif startPointOverlap:
                    self.polygon.append(self.endQPoint)
                    self.startQPoint = QPoint(-1, -1)
                    self.endQPoint = QPoint(-1, -1)
                else:
                    self.polygon.append(self.startQPoint)
                    self.polygon.append(self.endQPoint)
                    self.startQPoint = QPoint(-1, -1)
                    self.endQPoint = QPoint(-1, -1)
        if self.shape == "Group":
            if self.startQPoint.x() < 0:
                return
            self.objectIndex = self.objectIndex + 1
            chooseArea = QRect(self.startQPoint, self.endQPoint)
            containIndex = [self.objectIndex]
            # loop ellipse
            for elps in self.ellipses:
                if chooseArea.contains(elps.ellipse.center()):
                    containIndex.append(elps.objIndex)
            # loop circle
            for circle in self.circles:
                if chooseArea.contains(circle.circle.center()):
                    containIndex.append(circle.objIndex)
            # loop rectangular
            for rect in self.rects:
                if chooseArea.contains(rect.rectangle.center()):
                    containIndex.append(rect.objIndex)
            # loop square
            for square in self.squares:
                if chooseArea.contains(square.square[0]) and chooseArea.contains(square.square[1]) and chooseArea.contains(square.square[2]) and chooseArea.contains(square.square[3]):
                    containIndex.append(square.objIndex)
            # loop straight line
            for sl in self.straightLines:
                if chooseArea.contains(sl.straightLine.p1()) or chooseArea.contains(sl.straightLine.p2()):
                    containIndex.append(sl.objIndex)
            # loop freehand line
            for fhl in self.freeHandLines:
                if chooseArea.contains(fhl.freeHandLine[0]) or chooseArea.contains(fhl.freeHandLine[-1]):
                    containIndex.append(fhl.objIndex)
            # loop freehand line
            for plg in self.polygons:
                allPointsIncluded = True
                for point in plg.polygon:
                    if not chooseArea.contains(point):
                        allPointsIncluded = False
                        break
                if allPointsIncluded:
                    containIndex.append(plg.objIndex)
            # build group
            self.groups.append(
                objectCharacter.GroupCha(objIndex=self.objectIndex, objShape="Group", penColor=self.pen.color(), penWidth=self.pen.width(),
                         penStyle=Qt.DashDotLine, area=chooseArea, memberIndexes=containIndex))
            self.startQPoint = QPoint(-1, -1)
            self.endQPoint = QPoint(-1, -1)
        if self.shape == "Choose":
            if self.startQPoint.x() < 0:
                return
            self.chooseAnObject(self.startQPoint)
            moveX = self.endQPoint.x() - self.startQPoint.x()
            moveY = self.endQPoint.y() - self.startQPoint.y()
            self.moveObjectMembers(self.chooseObjectIndex, moveX, moveY)
            self.startQPoint = QPoint(-1, -1)
            self.endQPoint = QPoint(-1, -1)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = widgetSet.StockDialog()
    window.show()
    app.exec_()