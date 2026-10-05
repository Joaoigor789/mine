import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QComboBox, QLineEdit, QLabel, QProgressBar, QMessageBox
)
from PyQt6.QtCore import QThread, pyqtSignal

from launcher import versions, launcher_core
from launcher.executor import MinecraftExecutor
from launcher.console import ConsoleWidget


class InstallThread(QThread):
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    failed = pyqtSignal(str)

    def __init__(self, version):
        super().__init__()
        self.version = version

    def run(self):
        cb = {
            "setStatus": lambda s: self.status.emit(s),
            "setProgress": lambda p: self.progress.emit(p),
            "setMax": lambda m: None,
        }
        try:
            versions.install_version(self.version, cb)
            self.status.emit("Instalação concluída!")
        except Exception as e:
            self.failed.emit(str(e))


class LauncherWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Meu Launcher Minecraft")
        self.resize(640, 480)

        self.executor = MinecraftExecutor(
            on_log=self._on_log,
            on_exit=self._on_exit,
        )

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Nickname:"))
        self.username = QLineEdit("Player")
        layout.addWidget(self.username)

        layout.addWidget(QLabel("Versão:"))
        self.version_box = QComboBox()
        layout.addWidget(self.version_box)

        row = QHBoxLayout()
        self.btn_install = QPushButton("Instalar versão")
        self.btn_install.clicked.connect(self.install)
        row.addWidget(self.btn_install)

        self.btn_launch = QPushButton("Jogar")
        self.btn_launch.clicked.connect(self.play)
        row.addWidget(self.btn_launch)

        self.btn_stop = QPushButton("Parar")
        self.btn_stop.clicked.connect(self.stop)
        self.btn_stop.setEnabled(False)
        row.addWidget(self.btn_stop)

        layout.addLayout(row)

        self.progress = QProgressBar()
        layout.addWidget(self.progress)

        self.status = QLabel("Pronto.")
        layout.addWidget(self.status)

        layout.addWidget(QLabel("Console:"))
        self.console = ConsoleWidget()
        layout.addWidget(self.console)

        # input de comando pro servidor/console do MC
        input_row = QHBoxLayout()
        self.cmd_input = QLineEdit()
        self.cmd_input.setPlaceholderText("Comando pro Minecraft (ex: /help)")
        self.cmd_input.returnPressed.connect(self.send_command)
        input_row.addWidget(self.cmd_input)

        self.btn_send = QPushButton("Enviar")
        self.btn_send.clicked.connect(self.send_command)
        input_row.addWidget(self.btn_send)
        layout.addLayout(input_row)

        self.setLayout(layout)
        self.load_versions()

    def load_versions(self):
        try:
            for v in versions.get_available_versions(only_release=True):
                self.version_box.addItem(v["id"])
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao carregar versões: {e}")

    def install(self):
        version = self.version_box.currentText()
        self.status.setText(f"Instalando {version}...")
        self.thread = InstallThread(version)
        self.thread.status.connect(self.status.setText)
        self.thread.progress.connect(self.progress.setValue)
        self.thread.failed.connect(lambda m: QMessageBox.critical(self, "Erro", m))
        self.thread.start()

    def play(self):
        version = self.version_box.currentText()
        username = self.username.text().strip() or "Player"
        try:
            command = launcher_core.build_command(version, username)
            self.executor.start(command)
            self.status.setText("Minecraft rodando...")
            self.btn_launch.setEnabled(False)
            self.btn_stop.setEnabled(True)
            self.console.append_line(f"$ {' '.join(command[:3])} ...")
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))

    def stop(self):
        self.executor.stop()
        self.console.append_line("[launcher] encerrando processo...")

    def send_command(self):
        text = self.cmd_input.text().strip()
        if not text:
            return
        try:
            self.executor.send_command(text)
            self.console.append_line(f"> {text}")
            self.cmd_input.clear()
        except Exception as e:
            self.console.append_line(f"[erro] {e}")

    def _on_log(self, line: str):
        self.console.append_line(line)

    def _on_exit(self, code: int):
        self.console.append_line(f"[launcher] processo finalizado (código {code})")
        self.status.setText("Minecraft fechado.")
        self.btn_launch.setEnabled(True)
        self.btn_stop.setEnabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = LauncherWindow()
    w.show()
    sys.exit(app.exec())