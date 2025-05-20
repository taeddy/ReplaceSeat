import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import numpy as np
from InputDialog import InputDialog

form_class_mainWindow = uic.loadUiType("uiInfo.ui")[0]

class seat_button(QPushButton):
    # 새로운 시그널 추가
    rightClicked = pyqtSignal()
    doubleClicked = pyqtSignal()

    def __init__(self, title, parent):
        QPushButton.__init__(self, title, parent)
        self.drag_start_position = None  # 드래그 시작 위치 저장

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.RightButton:
            self.rightClicked.emit()  # 우클릭 시그널
        elif e.button() == Qt.LeftButton:
            self.drag_start_position = e.pos()
        super().mousePressEvent(e)

    def mouseMoveEvent(self, e: QMouseEvent):
        if not self.drag_start_position:
            return

        # 드래그 시작 위치로부터의 거리가 10픽셀 이상일 때만 드래그 시작
        if (e.pos() - self.drag_start_position).manhattanLength() < 10:
            return

        # 드래그 데이터 생성
        drag = QDrag(self)

        # mime_data가 있어야 pixmap 설정 가능
        mime_data = QMimeData()
        drag.setMimeData(mime_data)

        # 드래그 중 띄울 이미지 생성
        pixmap = QPixmap(self.size())
        self.render(pixmap)
        drag.setPixmap(pixmap)

        # 드래그 핫스팟 설정 (마우스 커서 위치)
        # 아래와 같이 핫스팟 설정을 하면 잡은 위치 그대로 움직임
        drag.setHotSpot(e.pos() - self.rect().topLeft())

        # 드래그 시작
        drag.exec_(Qt.MoveAction)
        super().mouseMoveEvent(e)

    def mouseReleaseEvent(self, e: QMouseEvent):
        self.drag_start_position = None
        super().mouseReleaseEvent(e)

    def mouseDoubleClickEvent(self, e: QMouseEvent):
        self.doubleClicked.emit()  # 더블클릭 시그널
        super().mouseDoubleClickEvent(e)

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

        # 좌석 버튼 생성
        self.seat_btn_arr = []
        for i in range(24):
            self.seat_btn_arr.append(seat_button('', self))

        # 좌석 위치 설정
        # 차후 좌석 위치를 드래그앤드롭으로 변경 가능해지면 수정 예정
        for i in range(5):  # 1열
            self.seat_btn_arr[i].setGeometry(590, 360-60*i, 91, 51)
        for i in range(5):  # 2열
            self.seat_btn_arr[i+5].setGeometry(470, 360-60*i, 91, 51)
        for i in range(4):  # 3열
            self.seat_btn_arr[i+10].setGeometry(350, 360-60*i, 91, 51)
        for i in range(5):  # 4열
            self.seat_btn_arr[i+14].setGeometry(230, 360-60*i, 91, 51)
        for i in range(5):  # 5열
            self.seat_btn_arr[i+19].setGeometry(110, 360-60*i, 91, 51)

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
        self.seat_btn_arr = self.seat_btn_arr
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
        self.btn_rand.clicked.connect(self.shuffle_seats)
        self.btn_save.clicked.connect(self.save_seat)
        self.intro_startbtn.clicked.connect(self.intro_start)
        
        # 우클릭으로 자리고정
        # 좌클릭-드래그앤드롭으로 자리 이동
        # 더블클릭으로 이름 변경
        for i in range(self.stu_num):
            self.seat_btn_arr[i].rightClicked.connect(lambda idx=i: self.fix_seat(idx))
            self.seat_btn_arr[i].doubleClicked.connect(lambda idx=i: self.change_seat_name(idx))
            self.seat_btn_arr[i].setAcceptDrops(True)

    def shuffle_seats(self):
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
        self.intro_bg.deleteLater()
        self.intro_startbtn.deleteLater()
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

        # 현재 윈도우만 스크린샷 저장
        # 기존 코드는 전체화면 스크린샷이 캡쳐되는 오류가 있었음
        # 메뉴바를 제외하고 캡쳐할 수 있게 수정 필요
        screen = QApplication.primaryScreen()
        window_geometry = self.geometry()
        screenshot = screen.grabWindow(
            self.winId(),
            self.x(), self.y(),  # 시작 위치 (0,0)
            window_geometry.width(),
            window_geometry.height()
        )
        screenshot.save('자리배치표.png', 'png')

        # 저장 완료 메시지 표시
        msg = QMessageBox()
        msg.setWindowTitle('알림')
        msg.setText('저장되었습니다')
        msg.setIcon(QMessageBox.Information)
        msg.setStyleSheet(
            'QMessageBox { background-color: #FFF9EB; }'
            'QMessageBox QLabel { color: #66391A; font-family: 맑은 고딕; font-size: 12px; padding: 10px; }'
            'QPushButton { color: #66391A; background-color: #FFEFB3; border-style: solid; '
            'border-color: #F5DA97; border-radius: 5px; border-width: 2px; '
            'min-width: 60px; padding: 5px; font-family: 맑은 고딕; }'
        )
        msg.exec_()

    def change_seat_name(self, seat_idx):
        text, ok = InputDialog.getText(self, f'이름 변경 - 좌석 {seat_idx + 1}')
        
        if ok and text:
            # 현재 자리에 있는 학생의 인덱스 찾기
            student_idx = self.seat_arr[seat_idx]
            # 이름 변경
            self.stu_name[student_idx] = text
            self.seat_btn_arr[seat_idx].setText(text)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = SeatChanger()
    mainWindow.show()
    app.exec_()