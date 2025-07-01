import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QAction
from components.pull.screen import PullScreen
from components.push.screen import PushScreen

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sync WP")
        self.resize(800, 600)
        
        # Pull menu
        pull_menu = self.menuBar().addMenu("Pull")
        pull_action = QAction("Pull", self)
        pull_menu.addAction(pull_action)
        pull_action.triggered.connect(self.open_pull_screen)
        
        # Push menu
        push_menu = self.menuBar().addMenu("Push")
        push_action = QAction("Push", self)
        push_menu.addAction(push_action)
        push_action.triggered.connect(self.open_push_screen)

    def open_pull_screen(self):
        pull_screen = PullScreen()
        self.setCentralWidget(pull_screen)
        
    def open_push_screen(self):
        push_screen = PushScreen()
        self.setCentralWidget(push_screen)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
