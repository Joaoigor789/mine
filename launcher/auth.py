"""
Autenticação do usuário.
Por enquanto suporta apenas modo OFFLINE (cracked / testes).
Estrutura pronta para adicionar Microsoft Account depois.
"""

import uuid
import hashlib
from dataclasses import dataclass


@dataclass
class Account:
    username: str
    uuid: str
    token: str
    account_type: str  # "offline" | "microsoft"


def _generate_offline_uuid(username: str) -> str:
    """UUID offline estilo Minecraft (MD5 de 'OfflinePlayer:<nick>')."""
    string = "OfflinePlayer:" + username
    md5 = hashlib.md5(string.encode("utf-8")).digest()
    return str(uuid.UUID(bytes=md5, version=3))


def login_offline(username: str) -> Account:
    """
    Cria uma conta offline com o nickname informado.
    Só funciona em servidores que aceitam modo offline.
    """
    username = (username or "Player").strip()
    if not username:
        username = "Player"

    return Account(
        username=username,
        uuid=_generate_offline_uuid(username),
        token="",  # offline não tem token
        account_type="offline",
    )


# ---- Espaço reservado para Microsoft Account (futuro) ----

def login_microsoft(callback: dict | None = None) -> Account:
    """
    Placeholder para login Microsoft real.
    Para implementar de verdade, usar:
        from minecraft_launcher_lib.microsoft_account import (
            get_login_url, complete_login, ...
        )
    """
    raise NotImplementedError(
        "Login Microsoft ainda não implementado neste launcher."
    )


def refresh_microsoft(account: Account) -> Account:
    """Renova token de uma conta Microsoft (placeholder)."""
    raise NotImplementedError("Refresh Microsoft ainda não implementado.")