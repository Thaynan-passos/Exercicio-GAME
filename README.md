# 🚀 Spacial GAME

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/pygame-2.5%2B-green.svg)](https://www.pygame.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Um jogo de nave espacial 2D retrô (*Shoot 'em up*) desenvolvido em Python com a biblioteca **Pygame**. Desvie de chuvas de meteoritos, destrua naves invasoras, derrote chefes com vida progressiva e conquiste a maior pontuação!

---

## 🎮 Funcionalidades

- **Combate Espacial Dinâmico:** Movimentação fluida da nave e sistema de disparos simultâneos.
- **Inimigos & Meteoros:** Naves invasoras contínuas e eventos aleatórios de queda de meteoritos.
- **Batalhas contra Chefes (Boss Fight):** O chefe surge periodicamente conforme a pontuação avança, com barra de vida dedicada, ataques especiais e dificuldade progressiva.
- **Sistema de Vidas e Dano:** Contador de vidas visual em corações, com tempo de invulnerabilidade e efeito de piscar ao receber impacto.
- **Telas Completas de Fluxo:** Menu inicial e tela de *Game Over* interativa com opção de reinício imediato.
- **Portabilidade Total:** Resolução dinâmica de caminhos compatível com Windows, Linux e macOS.

---

## 🕹️ Controles

| Tecla | Ação |
| :--- | :--- |
| **Setas (← ↑ → ↓)** | Movimentam a nave pelo espaço |
| **Barra de Espaço** | Dispara tiros da nave |
| **Enter** | Inicia a partida na tela de abertura |
| **R** | Reinicia a partida após a derrota (*Game Over*) |
| **ESC** | Sai da partida na tela de *Game Over* |

---

## 📁 Estrutura do Repositório

```text
Exercicio-GAME/
├── .github/
│   └── workflows/
│       └── ci.yml            # Pipeline de integração contínua (CI)
├── examples/                 # Protótipos e exemplos didáticos
│   ├── brick_breaker_prototipo.py
│   ├── criar_inimigo.py
│   ├── criar_tela.py
│   └── exemplo_tiro_inimigo.py
├── fonte/                    # Tipografias e fontes TTF
│   ├── Jacquard_12/
│   └── Pixelify_Sans/
├── imagem/                   # Texturas e sprites do jogo
│   ├── chefe-inimigo-Photoroom.png
│   ├── coração.png
│   ├── fundo2.png
│   ├── gamerover.png
│   ├── inimigo1.png
│   ├── meteoro.png
│   └── nave1.png
├── .gitignore                # Regras de exclusão do Git
├── CONTRIBUTING.md           # Diretrizes para contribuição
├── LICENSE                   # Licença MIT
├── main.py                   # Ponto de entrada oficial do jogo
├── projeto.py                # Módulo de compatibilidade
├── README.md                 # Documentação principal
└── requirements.txt          # Dependências do projeto
```

---

## ⚙️ Pré-requisitos e Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/Exercicio-GAME.git
   cd Exercicio-GAME
   ```

2. **Crie e ative um ambiente virtual (recomendado):**
   ```bash
   # Linux/macOS
   python3 -m venv .venv
   source .venv/bin/activate

   # Windows (PowerShell)
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute o jogo:**
   ```bash
   python main.py
   ```

---

## 🎨 Créditos dos Assets

- **Fontes:** *Pixelify Sans* e *Jacquard 12* (Google Fonts, sob licença Open Font License - OFL).
- **Sprites e Texturas:** Arte pixel art original integrada para o projeto acadêmico/exercício.

---

## 📄 Licença

Este projeto está sob a licença [MIT](LICENSE).
