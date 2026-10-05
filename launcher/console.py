from PyQt6.QtWidgets import QPlainTextEdit
from PyQt6.QtGui import QFont


class ConsoleWidget(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setFont(QFont("Monospace", 9))
        self.setStyleSheet("background-color: #111; color: #0f0;")

    def append_line(self, line: str):
        self.appendPlainText(line)
        # auto-scroll
        sb = self.verticalScrollBar()
        sb.setValue(sb.maximum())