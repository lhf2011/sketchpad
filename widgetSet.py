import main
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class StockDialog(QWidget):
    def __init__(self, parent=None):
        super(StockDialog, self).__init__(parent)
        self.setWindowTitle("SketchPad")
        mainSplitter = QSplitter(Qt.Horizontal)
        mainSplitter.setOpaqueResize(True)
        frame = QFrame(mainSplitter)
        mainLayout = QGridLayout(frame)
        mainLayout.setSpacing(6)

        label1 = QLabel("Object Shape：")
        label2 = QLabel("Pen Width：")
        label3 = QLabel("Pen Color：")
        label4 = QLabel("Pen Style：")
        label5 = QLabel("Undo/Redo：")


        self.shapeComboBox = QComboBox()
        self.shapeComboBox.addItem("FreeHandLine", "FreeHandLine")
        self.shapeComboBox.addItem("Line", "Line")
        self.shapeComboBox.addItem("Rectangle", "Rectangle")
        self.shapeComboBox.addItem('Ellipse', 'Ellipse')
        self.shapeComboBox.addItem('Square', 'Square')
        self.shapeComboBox.addItem('Circle', 'Circle')
        self.shapeComboBox.addItem('Polygon', 'Polygon')
        self.shapeComboBox.addItem('Group', 'Group')
        self.shapeComboBox.addItem('Choose', 'Choose')

        self.widthSpinBox = QSpinBox()
        self.widthSpinBox.setRange(0, 20)

        self.penColorFrame = QFrame()
        self.penColorFrame.setAutoFillBackground(True)
        self.penColorFrame.setPalette(QPalette(Qt.blue))
        self.penColorPushButton = QPushButton("choose color")

        self.penStyleComboBox = QComboBox()
        self.penStyleComboBox.addItem("Solid", Qt.SolidLine)
        self.penStyleComboBox.addItem('Dash', Qt.DashLine)
        self.penStyleComboBox.addItem('Dot', Qt.DotLine)
        self.penStyleComboBox.addItem('Dash Dot', Qt.DashDotLine)
        self.penStyleComboBox.addItem('Dash Dot Dot', Qt.DashDotDotLine)
        self.penStyleComboBox.addItem('None', Qt.NoPen)

        self.redoPushButton = QPushButton("Undo")
        self.undoPushButton = QPushButton("Redo")

        labelCol = 0
        contentCol = 1

        # 建立布局
        mainLayout.addWidget(label1, 1, labelCol)
        mainLayout.addWidget(self.shapeComboBox, 1, contentCol)
        mainLayout.addWidget(label2, 2, labelCol)
        mainLayout.addWidget(self.widthSpinBox, 2, contentCol)
        mainLayout.addWidget(label3, 4, labelCol)
        mainLayout.addWidget(self.penColorFrame, 4, contentCol)
        mainLayout.addWidget(self.penColorPushButton, 4, 3)
        mainLayout.addWidget(label4, 6, labelCol)
        mainLayout.addWidget(self.penStyleComboBox, 6, contentCol)
        mainLayout.addWidget(label5, 8, labelCol)
        mainLayout.addWidget(self.redoPushButton, 8, contentCol)
        mainLayout.addWidget(self.undoPushButton, 8, 3)

        mainSplitter1 = QSplitter(Qt.Horizontal)
        mainSplitter1.setOpaqueResize(True)

        stack1 = QStackedWidget()
        stack1.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.area = main.PaintArea()
        stack1.addWidget(self.area)
        frame1 = QFrame(mainSplitter1)
        mainLayout1 = QVBoxLayout(frame1)
        mainLayout1.setSpacing(6)
        mainLayout1.addWidget(stack1)

        layout = QGridLayout(self)
        layout.addWidget(mainSplitter1, 0, 0)
        layout.addWidget(mainSplitter, 0, 1)
        self.setLayout(layout)

        # signal and slot
        self.shapeComboBox.activated.connect(self.slotShape)
        self.widthSpinBox.valueChanged.connect(self.slotPenWidth)
        self.penColorPushButton.clicked.connect(self.slotPenColor)
        self.penStyleComboBox.activated.connect(self.slotPenStyle)

        # setting signals
        self.areaPen = QPen(Qt.black, 2, Qt.SolidLine)
        self.slotShape(self.shapeComboBox.currentIndex())
        self.slotPenWidth(self.widthSpinBox.value())

    def slotShape(self, value):
        shape = self.area.ShapeList[value]
        self.area.setShape(shape)

    def slotPenWidth(self, value):
        self.areaPen.setWidth(value)
        self.area.setPen(self.areaPen)

    def slotPenStyle(self, value):
        self.areaPen.setStyle(value)
        self.area.setPen(self.areaPen)

    def slotPenColor(self):
        color = QColorDialog.getColor()
        self.penColorFrame.setPalette(QPalette(color))
        self.areaPen.setColor(self.penColorFrame.palette().color(QPalette.Window))
        self.area.setPen(self.areaPen)