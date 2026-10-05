import shutil
import os
import minecraft_launcher_lib

from . import auth

MINECRAFT_DIR = os.path.expanduser("~/.minecraft")


def check_java() -> bool:
    """Verifica se Java está no PATH."""
    return shutil.which("java") is not None


def build_command(version_id: str, username: str) -> list[str]:
    if not check_java():
        raise RuntimeError(
            "Java não encontrado no PATH. Instala com:\n"
            "  sudo apt install openjdk-17-jre -y"
        )

    account = auth.login_offline(username)
    options = {
        "username": account.username,
        "uuid": account.uuid,
        "token": account.token,
        "launcherName": "MeuLauncher",
        "launcherVersion": "1.0",
        "gameDirectory": MINECRAFT_DIR,
    }
    return minecraft_launcher_lib.command.get_minecraft_command(
        version_id, MINECRAFT_DIR, options
    )