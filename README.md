"<div align="center">

# 🎮 SquidStrike

### A Strategic Turn-Based Combat Game with AI

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Pygame](https://img.shields.io/badge/Pygame-2.0+-green.svg)](https://www.pygame.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

_Squid Game meets Chess - A tactical battle of wits and strategy_

[Features](#-features) • [Installation](#-installation) • [How to Play](#-how-to-play) • [AI System](#-ai-system) • [Screenshots](#-screenshots)

---

</div>

## 📖 Overview

**SquidStrike** is an innovative turn-based strategy game that combines tactical movement, strategic shooting, and intelligent AI opponents. Control a team of 5 unique pieces (circles, squares, triangles) equipped with different weapons (short gun, long gun, blast gun) in an intense battle on a 10x10 grid board.

The game features a sophisticated **Minimax algorithm with Alpha-Beta pruning** for AI decision-making, creating challenging opponents with distinct playing styles - aggressive Red team vs defensive Blue team.

---

## ✨ Features

### 🎯 Core Gameplay

- **Turn-Based Combat**: Strategic movement and shooting phases
- **5v5 Team Battles**: Red team vs Blue team
- **Three Piece Types**: Circles (cardinal movement), Squares (diagonal movement), Triangles (8-directional movement)
- **Three Weapon Types**:
  - 🔫 **Short Gun**: 2-range straight shots
  - 🎯 **Long Gun**: 2-range diagonal shots
  - 💣 **Blast Gun**: Area-of-effect damage with friendly fire

### 🤖 Advanced AI System

- **Minimax Algorithm** with Alpha-Beta pruning
- **Dual Heuristics**:
  - Red AI: Aggressive playstyle (prioritizes damage and kills)
  - Blue AI: Defensive playstyle (prioritizes survival and positioning)
- **Configurable Search Depth** for difficulty adjustment
- **Intelligent Decision-Making**: Evaluates piece positioning, health, and tactical opportunities

### 🎨 Visual Features

- Beautiful checkerboard design with gradient tiles
- Health bars with color-coded status (green → yellow → red)
- Smooth animations and visual effects
- Selection highlights and movement indicators
- Game over popup with victory animations
- Sound effects for actions (fire, reload, movement, death)
- Background music

### 🎵 Audio

- Background music for immersive gameplay
- Sound effects for all major actions
- Volume-controlled audio system

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/tashib11/SquidStrike.git
cd SquidStrike
```

2. **Install dependencies**

```bash
pip install pygame
```

3. **Verify file structure**

```
AI_Project/
├── main.py
├── README.md
└── res/
    ├── Sounds/
    │   ├── fire.mp3
    │   ├── reload.mp3
    │   ├── piece_place.mp3
    │   ├── death.mp3
    │   └── background_music.mp3
    └── weapon/
        ├── short.png
        ├── long.png
        └── blast.png
```

4. **Run the game**

```bash
python main.py
```

---

## 🎮 How to Play

### Game Objective

Eliminate all enemy pieces by reducing their health to zero while keeping your team alive.

### Game Phases

Each turn consists of two phases:

1. **Movement Phase**

   - Select a piece (click on it)
   - Valid moves are highlighted
   - Click on a destination to move

2. **Shooting Phase**
   - After moving, valid shooting targets are shown with crosshairs
   - Click on a target to shoot
   - Turn passes to the opponent

### Piece Types & Movement

| Piece           | Movement Pattern           | Range       |
| --------------- | -------------------------- | ----------- |
| 🔴 **Circle**   | Cardinal directions (↑↓←→) | 1-2 squares |
| 🟦 **Square**   | Diagonal directions (⤡⤢)   | 1-2 squares |
| 🔺 **Triangle** | All 8 directions           | 1 square    |

### Weapon Types

| Weapon           | Range        | Damage     | Special                     |
| ---------------- | ------------ | ---------- | --------------------------- |
| 🔫 **Short Gun** | 1-2 straight | 10 HP      | Standard shots              |
| 🎯 **Long Gun**  | 1-2 diagonal | 10 HP      | Diagonal targeting          |
| 💣 **Blast Gun** | 2 (fixed)    | 29/14/7 HP | Area damage + friendly fire |

**Blast Gun Damage:**

- Direct hit: 29 HP
- Adjacent (1 square): 14 HP
- Diagonal (2 squares): 7 HP

### Health System

- Each piece starts with **30 HP**
- Health bars show current status with color coding:
  - 🟢 Green: >60% health
  - 🟡 Yellow: 30-60% health
  - 🔴 Red: <30% health
- Health pickups spawn randomly on the board

### AI Configuration

Modify these variables in `main.py` to customize AI behavior:

```python
AI_ENABLED = True        # Enable/disable AI vs AI mode
AI_DELAY = 0.5          # Delay between AI moves (seconds)
MINIMAX_DEPTH = 3       # Search depth (higher = smarter but slower)
```

---

## 🧠 AI System

### Minimax Algorithm with Alpha-Beta Pruning

The AI uses a **minimax search tree** with **alpha-beta pruning** to evaluate moves up to a configurable depth. This allows the AI to "think ahead" several turns and choose optimal strategies.

### Heuristic Functions

#### Red AI - Aggressive Heuristic

- **Goal**: Maximize enemy damage and eliminations
- **Priorities**:
  1. Eliminate low-health enemies (50 point bonus per vulnerable enemy)
  2. Deal maximum damage (15 points per enemy HP lost)
  3. Maintain piece count advantage (1000 points per piece advantage)
  4. Preserve own health (5 points per own HP)

#### Blue AI - Defensive Heuristic

- **Goal**: Survival and opportunistic damage
- **Priorities**:
  1. Preserve own pieces (500 points per piece advantage)
  2. Maintain high health (weighted HP preservation)
  3. Capitalize on safe kill opportunities (50 point bonus)
  4. Avoid risky engagements

### Performance

- **Search Depth 3**: Fast, medium difficulty (~1000 game states evaluated)
- **Search Depth 4**: Balanced, challenging (~10,000 game states)
- **Search Depth 5+**: Expert level but slower (100,000+ states)

---

## 📸 Screenshots

### Gameplay in Action

<div align="center">

<img src="demo\war.png" alt="SquidStrike Gameplay" width="800">

_Intense strategic battle between Red and Blue teams_

</div>

<div align="center">

<img src="demo\war2.png" alt="SquidStrike Battle" width="800">

_Tactical positioning and weapon targeting in progress_

</div>

---

## 🛠️ Technical Details

### Technologies Used

- **Python 3.8+**: Core programming language
- **Pygame**: Game engine for graphics and input handling
- **NumPy-free AI**: Custom minimax implementation without external ML libraries

### Key Algorithms

- **Minimax with Alpha-Beta Pruning**: Game tree search
- **State Space Search**: Action generation and evaluation
- **Heuristic Evaluation**: Position scoring for decision-making

### Code Structure

```
main.py
├── Game Setup & Constants
├── Graphics & Rendering
│   ├── draw_board()
│   ├── draw_piece()
│   ├── draw_ui_info()
│   └── draw_game_over_popup()
├── Game Logic
│   ├── Movement validation
│   ├── Shooting mechanics
│   ├── Health management
│   └── Win condition checking
└── AI System
    ├── GameState class
    ├── minimax_alpha_beta()
    ├── heuristic_aggressive()
    ├── heuristic_defensive()
    └── get_all_possible_actions()
```

---

## 🎯 Game Modes

### AI vs AI (Default)

Watch two AI opponents battle with different strategies. Perfect for:

- Testing AI algorithms
- Learning optimal strategies
- Entertainment

### Player vs AI (Coming Soon)

Control your own team against the AI opponent.

### Player vs Player (Coming Soon)

Hot-seat multiplayer on the same computer.

---

## 📊 Game Statistics

Track performance metrics:

- Win rates per team
- Average game length
- Most effective strategies
- Piece survival rates

---

## 🤝 Contributing

Contributions are welcome! Here are some ideas:

- Add new piece types with unique movement patterns
- Implement new weapon types
- Create new AI heuristics
- Add multiplayer networking
- Improve graphics and animations
- Add game replays and analysis tools

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**tashib11**

- GitHub: [@tashib11](https://github.com/tashib11)
- Repository: [SquidStrike](https://github.com/tashib11/SquidStrike)

---

## 🙏 Acknowledgments

- Inspired by Squid Game and classic strategy board games
- Built with Pygame community support
- AI concepts from game theory and computer science research

---

<div align="center">

### 🌟 Star this repository if you found it helpful!

Made with ❤️ and ☕

</div>"
