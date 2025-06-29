import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QAction
from components.pull.screen import PullScreen

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sync WP")
        self.resize(800, 600)
        pull_menu = self.menuBar().addMenu("Pull")
        pull_action = QAction("Pull", self)
        pull_menu.addAction(pull_action)
        pull_action.triggered.connect(self.open_pull_screen)

    def open_pull_screen(self):
        pull_screen = PullScreen()
        self.setCentralWidget(pull_screen)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
