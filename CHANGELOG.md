# Changelog

Todas as mudanças notáveis deste projeto são documentadas neste arquivo.

O formato segue [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/)
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [Não lançado]

### Planejado
- Login oficial via Microsoft Account (OAuth2)
- Suporte a mod loaders (Forge, Fabric, Quilt, NeoForge)
- Seleção manual de versão do Java
- Detecção automática de crash com sugestão de correção
- Empacotamento como AppImage e `.deb`
- Temas claro/escuro na interface

---

## [0.3.0] - 2026-10-04

### Adicionado
- **Executor de processos** (`launcher/executor.py`) com captura de `stdout` e `stderr` em tempo real
- **Console integrado** na GUI com auto-scroll e cores
- **Envio de comandos** ao Minecraft pelo console (ex: `/gamemode creative`)
- **Botão "Parar"** para encerrar o processo do jogo sem travar a interface
- **Executor via CLI** (`cli.py`) com subcomandos `--list`, `--install` e `--play`
- **Log persistente** em `~/.minecraft/logs/launcher-YYYYMMDD-HHMMSS.log`
- **Detecção de saída prematura**: avisa quando o processo morre em menos de 5 linhas
- **Verificação de Java** no PATH antes de montar o comando
- Geração de **UUID offline** (algoritmo MD5 `OfflinePlayer:<nick>`)

### Modificado
- `launcher_core.py` agora **apenas monta o comando** (responsabilidade única)
- Login refatorado no módulo `auth.py` com dataclass `Account`
- Listagem de versões refatorada no módulo `versions.py`
- Interface reorganizada com layout vertical + barra de ações horizontal

### Corrigido
- Erro `module 'minecraft_launcher_lib.utils' has no attribute 'generate_uuid'`
  (função removida na lib 6.x — substituída por implementação própria)
- Processo morrendo silenciosamente sem mostrar logs
- Console fechando inesperadamente por falta de captura de `stderr`

### Removido
- Dependência implícita de funções obsoletas da `minecraft-launcher-lib`

---

## [0.2.0] - 2026-10-04

### Adicionado
- Módulo `auth.py` com suporte a login offline
- Módulo `versions.py` para listar, instalar e verificar versões
- Filtro de versões por tipo (`release` / `snapshot`)
- Thread separada para instalação, evitando travamento da UI
- Barra de progresso durante download/instalação

### Modificado
- Separação do código monolítico em módulos independentes
- Uso de sinais Qt (`pyqtSignal`) para comunicação entre threads e UI

### Corrigido
- Congelamento da interface durante instalação de versões

---

## [0.1.0] - 2026-10-04

### Adicionado
- Estrutura inicial do projeto
- Interface gráfica básica com PyQt6
- Campo de nickname
- Seleção de versão do Minecraft
- Botões de instalar e jogar
- Integração com `minecraft-launcher-lib` 6.x

---

## Tipos de mudança

- `Adicionado` para novas funcionalidades
- `Modificado` para mudanças em funcionalidades existentes
- `Obsoleto` para funcionalidades que serão removidas
- `Removido` para funcionalidades removidas
- `Corrigido` para correções de bugs
- `Segurança` para vulnerabilidades