"""
Executor via linha de comando.
Uso:
    python cli.py --list
    python cli.py --install 1.20.1
    python cli.py --play 1.20.1 --user Joao
"""

import argparse
import sys

from launcher import versions, launcher_core
from launcher.executor import MinecraftExecutor


def cmd_list():
    print("Versões instaladas:")
    for v in versions.get_installed_versions():
        print(f"  - {v}")
    print("\nÚltima release disponível:", versions.get_latest_release())


def cmd_install(version_id: str):
    print(f"Instalando {version_id}...")
    cb = {
        "setStatus": lambda s: print(f"\r{s:<80}", end=""),
        "setProgress": lambda p: None,
        "setMax": lambda m: None,
    }
    versions.install_version(version_id, cb)
    print("\nConcluído!")


def cmd_play(version_id: str, username: str):
    if not versions.is_installed(version_id):
        print(f"Versão {version_id} não instalada. Instalando...")
        cmd_install(version_id)

    print(f"\nIniciando Minecraft {version_id} como {username}...\n")
    command = launcher_core.build_command(version_id, username)

    executor = MinecraftExecutor(
        on_log=lambda line: print(line),
        on_exit=lambda code: print(f"\n[processo encerrado com código {code}]"),
    )
    executor.start(command)

    try:
        while executor.is_running():
            pass
    except KeyboardInterrupt:
        print("\nEncerrando...")
        executor.stop()


def main():
    parser = argparse.ArgumentParser(description="Executor do MeuLauncher")
    parser.add_argument("--list", action="store_true", help="listar versões")
    parser.add_argument("--install", metavar="VERSAO", help="instalar versão")
    parser.add_argument("--play", metavar="VERSAO", help="jogar versão")
    parser.add_argument("--user", default="Player", help="nickname")

    args = parser.parse_args()

    if args.list:
        cmd_list()
    elif args.install:
        cmd_install(args.install)
    elif args.play:
        cmd_play(args.play, args.user)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()