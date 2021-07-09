import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import uuid
import pdfplumber
import xlwings as xw




class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.all_saved = []
        self.all_rect = []
        self.lab_rect = {}
        self.buttons_present = []
        
        self.excelText = []
        
        self.initUI()
        self.flag = False

        self.setGeometry(30, 30, 500, 300)
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()

        self.show()
            
        
    def initUI(self):
        self.setFixedSize(900, 500)
        self.setWindowTitle('Document Viewer ')
        self.btn = QPushButton("Draw polygon", self)
        self.btn.move(10, 10)
        self.btn.clicked.connect(self.onClicked)
        
        self.save = QPushButton('Save', self)
        self.save.move (150, 10)
        self.save.clicked.connect(self.onSave)
        
        self.updateButton = QPushButton('Update', self)
        self.updateButton.move (250, 10)
        self.updateButton.clicked.connect(self.onUpdate)


        #self.show()

        

        
    def onSave(self):  

        self.all_saved += [f for f in self.all_rect if f not in self.all_saved]
        

        for i, v in self.lab_rect.items():
            if len(v) > 0 and i not in self.buttons_present:


                button = QPushButton("X", self)
                button.setStyleSheet("background-color: red")
                button.resize(20, 20)
                button.clicked.connect(lambda ch, i=i: self.handle_clicked(i) ) 
                
                button.move(v[0], v[1])
                self.buttons_present.append(i)
                button.show()


            
    def handle_clicked(self, i):
        
        
        button = self.sender()
        button.deleteLater()
        print('clicked ', i) 
        self.lab_rect[i] = []
        
    
    def get_text(self, filename, coordinates):
        # (100, 378, 418, 37+378)

        with pdfplumber.open(filename) as pdf:
            first_page = pdf.pages[0]
            page = first_page
            # left , top, width ,height
            bottom = page.crop(coordinates)
            im = bottom.extract_text(x_tolerance=3, y_tolerance=3)
            return(im)

    def add_text(self, text, column):
        app = xw.apps.active
        # Active book
        wb = xw.books.active  # in active app
        # Active sheet
        sht = xw.sheets.active  # in active book
        # Range on active sheet
        alphas = ['A','B','C','D','E','F','G','H']
        names = xw.Range('A1:H1').value
        print(names)

        for i in range(0, len(names)):
            if names[i] == column:
                start = alphas[i]+'2'

                xw.Range(start).value = text

   
    def onUpdate(self):  
        
        ids = []
        coordinates = []
        text_string = []
        
        
        for k, v in self.lab_rect.items():
            if len(v) > 0:

                text_string.append(self.get_text('test.pdf',(v[0], v[1], v[2], v[3]+v[1])))
               
                coordinates.append(str(v))
                ids.append(k)
                
                
        all_sents = [[f] for f in text_string ]

        self.add_text(all_sents,'Text')
        
        all_cords = [[f] for f in coordinates ]
        
        self.add_text(all_cords,'Coordinates')
        print(all_cords)
        
        all_poly = [[f] for f in ids ]
        
        self.add_text(all_poly,'Polygon')
        

        



    def onClicked(self):
        if self.flag:
            self.flag = False
        else:
            self.flag = True
        self.update()
        self.adjustSize()

    def paintEvent(self, event):
        
        
        
        
        
        painter = QPainter(self)
        pixmap = QPixmap("bottom.png")

        
        self.setFixedSize(pixmap.width(),pixmap.height())
        self.resize(pixmap.width(),pixmap.height())
        self.adjustSize()
        self.show()
        
        painter.drawPixmap(self.rect(), pixmap)
        pen = QPen(Qt.red, 3)
        
        painter.setPen(pen)
        rect = QtCore.QRect(self.begin, self.end)
        painter.drawRect(rect)
        
        if self.flag:

            self.x = rect.x()
            self.y = rect.y()
            self.w = rect.width()
            self.h = rect.height()


            if len(self.all_rect) > 0:
                
                for k, v in self.lab_rect.items():
                    if len(v) > 0:
                        painter.drawRect(v[0],v[1],v[2],v[3])

        
    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = event.pos()
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.begin = event.pos()
        self.end = event.pos()
        
        if self.flag and int(self.w) > 1:
            
            
            self.lab_rect[str(uuid.uuid1())] = [self.x, self.y, self.w, self.h] 
            
            print(" SAVING FROM MOUSE EVENT ")
            print(self.lab_rect)
            self.all_rect.append([self.x, self.y, self.w, self.h])

        
       

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())
