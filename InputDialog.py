from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class InputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('텍스트 입력')
        self.setFixedSize(300, 150)
        
        # 메인 레이아웃
        layout = QVBoxLayout()
        
        # 입력 필드
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText('텍스트를 입력하세요')
        self.input_field.setFont(QFont('맑은 고딕', 10))
        self.input_field.setStyleSheet(
            'padding: 5px; border: 2px solid #F5DA97; border-radius: 5px;'
        )
        
        # 버튼 레이아웃
        button_layout = QHBoxLayout()
        
        # 확인 버튼
        self.ok_button = QPushButton('확인')
        self.ok_button.setFont(QFont('맑은 고딕', 10))
        self.ok_button.setStyleSheet(
            'color: #66391A; background-color: #FFEFB3; border-style: solid;'
            'border-color: #F5DA97; border-radius: 5px; border-width: 2px;'
            'padding: 5px 15px;'
        )
        self.ok_button.clicked.connect(self.accept)
        
        # 취소 버튼
        self.cancel_button = QPushButton('취소')
        self.cancel_button.setFont(QFont('맑은 고딕', 10))
        self.cancel_button.setStyleSheet(
            'color: #66391A; background-color: #FFEFB3; border-style: solid;'
            'border-color: #F5DA97; border-radius: 5px; border-width: 2px;'
            'padding: 5px 15px;'
        )
        self.cancel_button.clicked.connect(self.reject)
        
        # 버튼을 레이아웃에 추가
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        
        # 메인 레이아웃에 위젯 추가
        layout.addWidget(self.input_field)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def get_text(self):
        return self.input_field.text()
    
    @staticmethod
    def getText(parent=None, title=''):
        dialog = InputDialog(parent)
        dialog.setWindowTitle(title)
        result = dialog.exec_()
        
        if result == QDialog.Accepted:
            return dialog.get_text(), True
        return '', False

# 사용 예시
if __name__ == '__main__':
    app = QApplication([])
    text, ok = InputDialog.getText(None, '이름 입력')
    if ok:
        print('입력된 텍스트:', text)
    app.quit() 