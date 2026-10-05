"""
Gerenciamento de versões do Minecraft:
- Listar versões disponíveis
- Listar versões instaladas
- Instalar uma versão
- Verificar se uma versão já está instalada
"""

import os
import minecraft_launcher_lib

MINECRAFT_DIR = os.path.expanduser("~/.minecraft")


def get_available_versions(only_release: bool = True):
    """
    Retorna lista de versões disponíveis para download.
    only_release=True filtra apenas releases (sem snapshots).
    """
    versions = minecraft_launcher_lib.utils.get_available_versions(MINECRAFT_DIR)
    if only_release:
        versions = [v for v in versions if v.get("type") == "release"]
    return versions


def get_installed_versions():
    """Retorna lista de IDs das versões já instaladas."""
    return minecraft_launcher_lib.utils.get_installed_versions(MINECRAFT_DIR)


def is_installed(version_id: str) -> bool:
    """Verifica se uma versão específica já está instalada."""
    return version_id in get_installed_versions()


def install_version(version_id: str, callback: dict | None = None):
    """
    Instala uma versão do Minecraft.
    callback: dict com chaves 'setStatus', 'setProgress', 'setMax'.
    """
    if callback is None:
        callback = {
            "setStatus": lambda x: print(f"[status] {x}"),
            "setProgress": lambda x: None,
            "setMax": lambda x: None,
        }
    minecraft_launcher_lib.install.install_minecraft_version(
        version_id, MINECRAFT_DIR, callback=callback
    )


def get_latest_release() -> str | None:
    """Retorna o ID da versão release mais recente."""
    try:
        return minecraft_launcher_lib.utils.get_latest_version()["release"]
    except Exception:
        return None