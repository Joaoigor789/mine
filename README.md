<div align="center">

# ⛏️ MeuLauncher

**Um launcher de Minecraft de código aberto, escrito em Python, feito para Linux.**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.x-41CD52?style=flat-square&logo=qt&logoColor=white)](https://www.riverbankcomputing.com/software/pyqt/)
[![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux-FCC624?style=flat-square&logo=linux&logoColor=black)]()

</div>

---

## 📖 Sobre

Launcher de Minecraft leve e modular, construído do zero em Python com PyQt6.
Suporta instalação automática de versões, login offline, console integrado
e execução de comandos em tempo real.

> ⚠️ **Status:** projeto em desenvolvimento ativo (v0.3.0).
> Login Microsoft oficial está no roadmap.

## ✨ Funcionalidades

- 🎮 **Interface gráfica** com PyQt6 — leve e nativa no Linux
- 📥 **Instalação automática** de qualquer versão release do Minecraft
- 👤 **Login offline** com geração de UUID no padrão Mojang
- 🖥️ **Console integrado** com logs em tempo real
- ⌨️ **Envio de comandos** direto pro jogo (`/gamemode`, `/tp`, etc.)
- 🛑 **Botão de parada** que encerra o processo sem travar a UI
- 📝 **Log persistente** em `~/.minecraft/logs/`
- 🧩 **CLI** para automação e debug (`python cli.py --play 1.20.1`)
- 🔧 **Arquitetura modular** — fácil de estender

## 🏗️ Arquitetura



## 🚀 Instalação

### Requisitos

- Python 3.11+
- Java 17 ou 21 (`sudo apt install openjdk-17-jre openjdk-21-jre`)
- Linux (testado em Ubuntu 22.04+)

### Passo a passo

```bash
# 1. Clone o repositório
git clone https://github.com/SEU-USUARIO/meu-launcher.git
cd meu-launcher

# 2. Crie um ambiente virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Rode
python main.py

---

linha de comando 
# Listar versões instaladas
python cli.py --list

# Instalar uma versão específica
python cli.py --install 1.20.1

# Jogar direto pelo terminal
python cli.py --play 1.20.1 --user Joao

--

🗺️ Roadmap
☑ v0.1.0 — Estrutura inicial e GUI
☑ v0.2.0 — Modularização e instalação de versões
☑ v0.3.0 — Executor, console e CLI
□ v0.4.0 — Login Microsoft oficial
□ v0.5.0 — Suporte a Forge / Fabric
□ v0.6.0 — Detecção de crash
□ v1.0.0 — Empacotamento AppImage / .deb

📄 Licença
Distribuído sob a licença MIT. Veja LICENSE para mais informações.

⚖️ Aviso legal
Este projeto não é afiliado, associado ou endossado pela Mojang Studios ou Microsoft.
"Minecraft" é uma marca registrada da Mojang Synergies AB.

