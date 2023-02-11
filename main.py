import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextBrowser, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView


class WebPageDisplay(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.input_area = QLineEdit()
        self.input_area.returnPressed.connect(self.load_url)
        
        self.browser = QWebEngineView()
        
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.go_back)
        self.forward_button = QPushButton("Forward")
        self.forward_button.clicked.connect(self.go_forward)
        
        layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button)
        button_layout.addWidget(self.forward_button)
        layout.addLayout(button_layout)
        layout.addWidget(self.input_area)
        layout.addWidget(self.browser)
        
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.resize(self.sizeHint())
        
        self.history = []
        self.history_index = 0
    
    def load_url(self):
        url = self.input_area.text()
        if not url.startswith(("http://", "https://")):
            url = "http://" + url
        self.browser.load(QUrl(url))
        self.history.append(url)
        self.history_index += 1
        if len(self.history) > 10:
            self.history.pop(0)
            self.history_index -= 1
    
    def go_back(self):
        if self.history_index > 0:
            self.history_index -= 1
            self.browser.load(QUrl(self.history[self.history_index]))
    
    def go_forward(self):
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.browser.load(QUrl(self.history[self.history_index]))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WebPageDisplay()
    window.show()
    sys.exit(app.exec_())
