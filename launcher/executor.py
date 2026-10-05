"""
Executor do processo do Minecraft (versão melhorada).
- Captura stdout e stderr
- Salva log em arquivo
- Detecta saída prematura
"""

import subprocess
import threading
import os
from datetime import datetime
from typing import Callable, Optional

LOG_DIR = os.path.expanduser("~/.minecraft/logs")


class MinecraftExecutor:
    def __init__(
        self,
        on_log: Optional[Callable[[str], None]] = None,
        on_exit: Optional[Callable[[int], None]] = None,
        log_file: Optional[str] = None,
    ):
        self.process: Optional[subprocess.Popen] = None
        self.on_log = on_log or (lambda line: print(line))
        self.on_exit = on_exit or (lambda code: None)
        self._thread: Optional[threading.Thread] = None
        self._last_lines: list[str] = []
        self._log_fp = None

        os.makedirs(LOG_DIR, exist_ok=True)
        if log_file is None:
            stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            log_file = os.path.join(LOG_DIR, f"launcher-{stamp}.log")
        self.log_path = log_file

    def is_running(self) -> bool:
        return self.process is not None and self.process.poll() is None

    def start(self, command: list[str]):
        if self.is_running():
            raise RuntimeError("Já existe um Minecraft rodando.")

        try:
            self._log_fp = open(self.log_path, "w", encoding="utf-8", errors="replace")
            self._log_fp.write(f"# Comando: {' '.join(command)}\n\n")
            self._log_fp.flush()
        except Exception as e:
            self.on_log(f"[executor] não consegui abrir log: {e}")

        # Não usar universal_newlines junto com bufsize=1 e text=True
        self.process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.PIPE,
            text=True,
            bufsize=1,
        )

        self._thread = threading.Thread(target=self._read_output, daemon=True)
        self._thread.start()

    def _read_output(self):
        try:
            assert self.process and self.process.stdout
            for line in self.process.stdout:
                line = line.rstrip("\n")
                self._last_lines.append(line)
                if len(self._last_lines) > 200:
                    self._last_lines.pop(0)
                self.on_log(line)
                if self._log_fp:
                    try:
                        self._log_fp.write(line + "\n")
                        self._log_fp.flush()
                    except Exception:
                        pass
        except Exception as e:
            self.on_log(f"[executor] erro lendo saída: {e}")
        finally:
            code = self.process.wait() if self.process else -1

            # Se morreu muito rápido, dá dica
            if code != 0 and len(self._last_lines) < 5:
                self.on_log(
                    f"[executor] ⚠️  Processo morreu rápido (código {code}). "
                    f"Provavelmente falta Java ou comando inválido."
                )
                self.on_log(f"[executor] Log salvo em: {self.log_path}")

            if self._log_fp:
                try:
                    self._log_fp.close()
                except Exception:
                    pass

            self.on_exit(code)

    def send_command(self, text: str):
        if not self.is_running():
            raise RuntimeError("Minecraft não está rodando.")
        assert self.process and self.process.stdin
        self.process.stdin.write(text + "\n")
        self.process.stdin.flush()

    def stop(self):
        if self.is_running():
            assert self.process
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()