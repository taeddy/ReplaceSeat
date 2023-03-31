import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import numpy as np

form_class_mainWindow = uic.loadUiType("uiInfo.ui")[0]

class Button(QPushButton):
    def __init__(self, title, parent):
        QPushButton.__init__(self, title, parent)
        self.offset = 0

    def mouseMoveEvent(self, e: QMouseEvent):
        if e.buttons() == Qt.RightButton:
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setData("application/hotspot", b"%d %d" % (e.x(), e.y()))
            drag.setMimeData(mime_data)

            pixmap = QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)

            drag.setHotSpot(e.pos() - self.rect().topLeft())
            drag.exec_(Qt.MoveAction)

class SeatChanger(QMainWindow, form_class_mainWindow):
    def __init__(self) :
        super().__init__()
        self.init_ui()
        self.set_param()
        self.init_action()

    def init_ui(self):
        self.setupUi(self)
        self.setWindowTitle('자리바꾸기')
        self.setAcceptDrops(True)
        self.statusBar().hide()
        self.setFixedHeight(541)
        self.setFixedWidth(800)

        self.btn_rand = QPushButton('섞기', self)
        self.btn_rand.lower()
        self.btn_rand.resize(65, 41)
        self.btn_rand.move(550, 430)
        # self.btn_rand.setStyleSheet(
        #     'border-image: url(refresh_icon.png);'
        # )

        self.btn_save = QPushButton('저장', self)
        self.btn_save.lower()
        self.btn_save.resize(45, 41)
        self.btn_save.move(630, 430)

        self.seat_btn_0 = Button('', self)
        self.seat_btn_1 = Button('', self)
        self.seat_btn_2 = Button('', self)
        self.seat_btn_3 = Button('', self)
        self.seat_btn_4 = Button('', self)
        self.seat_btn_5 = Button('', self)
        self.seat_btn_6 = Button('', self)
        self.seat_btn_7 = Button('', self)
        self.seat_btn_8 = Button('', self)
        self.seat_btn_9 = Button('', self)
        self.seat_btn_10 = Button('', self)
        self.seat_btn_11 = Button('', self)
        self.seat_btn_12 = Button('', self)
        self.seat_btn_13 = Button('', self)
        self.seat_btn_14 = Button('', self)
        self.seat_btn_15 = Button('', self)
        self.seat_btn_16 = Button('', self)
        self.seat_btn_17 = Button('', self)
        self.seat_btn_18 = Button('', self)
        self.seat_btn_19 = Button('', self)
        self.seat_btn_20 = Button('', self)
        self.seat_btn_21 = Button('', self)
        self.seat_btn_22 = Button('', self)
        self.seat_btn_23 = Button('', self)

        self.seat_btn_0.setGeometry(590,360,91,51)
        self.seat_btn_1.setGeometry(590,300,91,51)
        self.seat_btn_2.setGeometry(590,240,91,51)
        self.seat_btn_3.setGeometry(590,180,91,51)
        self.seat_btn_4.setGeometry(590,120,91,51)
        self.seat_btn_5.setGeometry(470,360,91,51)
        self.seat_btn_6.setGeometry(470,300,91,51)
        self.seat_btn_7.setGeometry(470,240,91,51)
        self.seat_btn_8.setGeometry(470,180,91,51)
        self.seat_btn_9.setGeometry(470,120,91,51)
        self.seat_btn_10.setGeometry(350,360,91,51)
        self.seat_btn_11.setGeometry(350,300,91,51)
        self.seat_btn_12.setGeometry(350,240,91,51)
        self.seat_btn_13.setGeometry(350,180,91,51)
        self.seat_btn_14.setGeometry(230,360,91,51)
        self.seat_btn_15.setGeometry(230,300,91,51)
        self.seat_btn_16.setGeometry(230,240,91,51)
        self.seat_btn_17.setGeometry(230,180,91,51)
        self.seat_btn_18.setGeometry(230,120,91,51)
        self.seat_btn_19.setGeometry(110,360,91,51)
        self.seat_btn_20.setGeometry(110,300,91,51)
        self.seat_btn_21.setGeometry(110,240,91,51)
        self.seat_btn_22.setGeometry(110,180,91,51)
        self.seat_btn_23.setGeometry(110,120,91,51)

        self.loading = QLabel('', self)
        self.loading.move(215, 110)
        self.loading.setFixedSize(370, 320)
        self.movie = QMovie('loading.gif', QByteArray(), self)
        self.movie.setSpeed(80)
        self.movie.setCacheMode(QMovie.CacheAll)
        self.loading.setMovie(self.movie)
        self.movie.frameChanged.connect(self.loading_finished)
        self.loading.hide()

        self.blind1 = QLabel('', self)
        self.blind1.setGeometry(90, 120, 621, 301)
        self.blind1.hide()

        self.blind2 = QLabel('', self)
        self.blind2.setGeometry(550,430,125,41)
        self.blind2.setStyleSheet(
            'background-color: rgb(255, 249, 235)'
        )
        self.blind2.hide()

    def loading_finished(self, frame):
        alpha = (1-1/self.movie.frameCount()*frame)*255
        self.blind1.setStyleSheet(
            'background-color: rgba(255, 249, 235, %d);' % alpha
        )
        if frame == self.movie.frameCount()-1:
            self.movie.stop()
            self.loading.hide()
            self.blind1.hide()
            self.btn_save.setEnabled(True)
            self.btn_rand.setEnabled(True)

    def set_param(self):
        self.stu_num = 24
        self.seat_arr = [0] * self.stu_num
        self.stu_name = ['None'] * self.stu_num
        self.load_data()
        self.seat_btn_arr = [
            self.seat_btn_0, self.seat_btn_1, self.seat_btn_2, self.seat_btn_3, self.seat_btn_4,
            self.seat_btn_5, self.seat_btn_6, self.seat_btn_7, self.seat_btn_8, self.seat_btn_9,
            self.seat_btn_10, self.seat_btn_11, self.seat_btn_12, self.seat_btn_13,
            self.seat_btn_14, self.seat_btn_15, self.seat_btn_16, self.seat_btn_17, self.seat_btn_18,
            self.seat_btn_19, self.seat_btn_20, self.seat_btn_21, self.seat_btn_22, self.seat_btn_23,
        ]
        self.fixed_seat_idx = []

        font = QFont()
        font.setFamily('맑은 고딕')
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        for i in range(self.stu_num):
            self.seat_btn_arr[i].setText(self.stu_name[i])
            self.seat_btn_arr[i].setFont(font)
            self.seat_btn_arr[i].setStyleSheet(
                'color: #66391A; background-color: #FFEFB3; border-style: solid;'
                'border-color: #F5DA97; border-radius: 7px; border-width: 3px'
            )
            self.seat_btn_arr[i].lower()
            # self.seat_label_arr[i].setDropEnable(True)

    def load_data(self):
        f = open('./명단.txt', 'r', encoding='UTF8')
        for i in range(self.stu_num):
            self.seat_arr[i] = i
            self.stu_name[i] = f.readline().strip()
        f.close()

    def init_action(self):
        self.btn_rand.clicked.connect(self.seat_shuffle)
        self.btn_save.clicked.connect(self.save_seat)
        self.intro_startbtn.clicked.connect(self.intro_start)
        self.seat_btn_arr[0].clicked.connect(lambda: self.fix_seat(0))
        self.seat_btn_arr[1].clicked.connect(lambda: self.fix_seat(1))
        self.seat_btn_arr[2].clicked.connect(lambda: self.fix_seat(2))
        self.seat_btn_arr[3].clicked.connect(lambda: self.fix_seat(3))
        self.seat_btn_arr[4].clicked.connect(lambda: self.fix_seat(4))
        self.seat_btn_arr[5].clicked.connect(lambda: self.fix_seat(5))
        self.seat_btn_arr[6].clicked.connect(lambda: self.fix_seat(6))
        self.seat_btn_arr[7].clicked.connect(lambda: self.fix_seat(7))
        self.seat_btn_arr[8].clicked.connect(lambda: self.fix_seat(8))
        self.seat_btn_arr[9].clicked.connect(lambda: self.fix_seat(9))
        self.seat_btn_arr[10].clicked.connect(lambda: self.fix_seat(10))
        self.seat_btn_arr[11].clicked.connect(lambda: self.fix_seat(11))
        self.seat_btn_arr[12].clicked.connect(lambda: self.fix_seat(12))
        self.seat_btn_arr[13].clicked.connect(lambda: self.fix_seat(13))
        self.seat_btn_arr[14].clicked.connect(lambda: self.fix_seat(14))
        self.seat_btn_arr[15].clicked.connect(lambda: self.fix_seat(15))
        self.seat_btn_arr[16].clicked.connect(lambda: self.fix_seat(16))
        self.seat_btn_arr[17].clicked.connect(lambda: self.fix_seat(17))
        self.seat_btn_arr[18].clicked.connect(lambda: self.fix_seat(18))
        self.seat_btn_arr[19].clicked.connect(lambda: self.fix_seat(19))
        self.seat_btn_arr[20].clicked.connect(lambda: self.fix_seat(20))
        self.seat_btn_arr[21].clicked.connect(lambda: self.fix_seat(21))
        self.seat_btn_arr[22].clicked.connect(lambda: self.fix_seat(22))
        self.seat_btn_arr[23].clicked.connect(lambda: self.fix_seat(23))

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        pos = e.pos()
        widget = e.source()
        new_seat = None
        old_seat = None

        # calculate drop location seat number
        for i in range(self.stu_num):
            x, y = self.seat_btn_arr[i].x(), self.seat_btn_arr[i].y()
            w, h = self.seat_btn_arr[i].size().width(), self.seat_btn_arr[i].size().height()
            if x <= pos.x() <= x+w and y <= pos.y() <= y + h:
                new_seat = i
                break

        # find old seat
        for i in range(self.stu_num):
            if self.seat_btn_arr[i].text() == widget.text():
                old_seat = i
                break

        # change text
        text = widget.text()
        widget.setText(self.seat_btn_arr[new_seat].text())
        self.seat_btn_arr[new_seat].setText(text)

        # change seat
        stu = self.seat_arr[old_seat]
        self.seat_arr[old_seat] = self.seat_arr[new_seat]
        self.seat_arr[new_seat] = stu

    def seat_shuffle(self):
        self.btn_rand.setDisabled(True)
        self.btn_save.setDisabled(True)
        self.blind1.raise_()
        self.blind1.show()
        self.loading.raise_()
        self.loading.show()
        self.movie.start()

        old_owner = []
        for i in self.fixed_seat_idx:
            old_owner.append(self.seat_arr[i])

        np.random.seed()
        np.random.shuffle(self.seat_arr)

        for i in range(len(self.fixed_seat_idx)):
            tmp1 = self.seat_arr.index(old_owner[i])  # 원래 자리 주인 ㅇㄷ
            tmp2 = self.seat_arr[self.fixed_seat_idx[i]]  # 원래 자리에 ㄴㄱ
            self.seat_arr[self.fixed_seat_idx[i]] = old_owner[i]
            self.seat_arr[tmp1] = tmp2

        for i in range(self.stu_num):
            self.seat_btn_arr[i].setText(self.stu_name[self.seat_arr[i]])

    def fix_seat(self, seat_idx=0):
        if seat_idx not in self.fixed_seat_idx:
            self.fixed_seat_idx.append(seat_idx)
            self.seat_btn_arr[seat_idx].setStyleSheet(
                'background-color: rgba(148, 148, 148, 150); border-radius: 7px;'
            )
        else:
            self.fixed_seat_idx.remove(seat_idx)
            self.seat_btn_arr[seat_idx].setStyleSheet(
                'color: #66391A; background-color: #FFEFB3; border-style: solid;'
                'border-color: #F5DA97; border-radius: 7px; border-width: 3px;'
            )

    def intro_start(self):
        self.intro_bg.hide()
        self.intro_startbtn.hide()
        self.btn_rand.raise_()
        self.btn_save.raise_()
        for i in range(self.stu_num):
            self.seat_btn_arr[i].raise_()

    def save_seat(self):
        f = open("명단.txt", 'w', encoding='UTF8')
        for i in range(self.stu_num):
            data = "%s\n" % self.seat_btn_arr[i].text()
            f.write(data)
        f.close()

        screen = QApplication.primaryScreen()
        screenshot = screen.grabWindow(self.winId())
        screenshot.save('자리배치표.png', 'png')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = SeatChanger()
    myWindow.show()
    app.exec_()