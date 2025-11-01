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

- **Beautiful checkerboard design** with gradient tiles (light and dark shades)
- **Enhanced health bars** with gradient colors (green → yellow → red)
- **Shadow effects** on pieces for depth perception
- **Glow effects** on selected pieces with rounded borders
- **Movement indicators** with pulsing circles for valid moves
- **Crosshair targeting** for shooting phase with visual feedback
- **Game over popup** with trophy/star decorations and gradient buttons
- **UI panel** at bottom showing turn indicator and team status
- **Real-time health updates** visible during gameplay
- **Background colors** optimized for better contrast (50, 55, 65 RGB)

### 🎵 Audio

- **Background music** for immersive gameplay (looping, volume-controlled)
- **Sound effects** for all major actions:
  - Fire sound when shooting
  - Reload sound when moving
  - Piece placement sound on selection
  - Death sound when pieces are eliminated
- Volume-controlled audio system (background music at 10% volume)

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
├── demo/
│   ├── war.png
│   └── war2.png
└── res/
    ├── circle_red.png
    ├── circle_blue.png
    ├── square_red.png
    ├── square_blue.png
    ├── triangle_red.png
    ├── triangle_blue.png
    ├── health_pickup.png
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

### Team Composition

Each team consists of 5 pieces with assigned weapons:

**Red Team** (Starts at top, rows 0):

- Position 0: Circle + Short Gun
- Position 1: Square + Long Gun
- Position 2: Triangle + Blast Gun (Center piece)
- Position 3: Square + Long Gun
- Position 4: Circle + Short Gun

**Blue Team** (Starts at bottom, row 9):

- Position 0: Circle + Short Gun
- Position 1: Square + Long Gun
- Position 2: Triangle + Blast Gun (Center piece)
- Position 3: Square + Long Gun
- Position 4: Circle + Short Gun

_Both teams have identical compositions for fair gameplay. Turn order is randomized at game start._

### Weapon Types

| Weapon           | Range        | Damage     | Special                     |
| ---------------- | ------------ | ---------- | --------------------------- |
| 🔫 **Short Gun** | 1-2 straight | 10 HP      | Standard shots              |
| 🎯 **Long Gun**  | 1-2 diagonal | 10 HP      | Diagonal targeting          |
| 💣 **Blast Gun** | 2 (fixed)    | 29/14/7 HP | Area damage + friendly fire |

**Blast Gun Damage:**

- Direct hit (0 distance): 29 HP (near-lethal)
- Adjacent (1 Manhattan distance): 14 HP
- Diagonal corners (2 Manhattan distance): 7 HP
- **Warning**: Blast gun damages ALL pieces in range, including friendly units!

### Game Mechanics Details

**Movement Rules:**

- Pieces cannot move through other pieces (blocked paths)
- Circles/Squares can move 2 squares if path is clear
- Each piece must move before shooting (no stationary shots)

**Shooting Rules:**

- All shots require line of sight (no shooting through pieces for regular guns)
- Blast gun always fires at exactly 2 squares distance in cardinal directions
- Blast gun can damage multiple pieces in its area of effect
- Regular guns (short/long) deal 10 HP damage per hit

**Turn Structure:**

1. AI selects a piece
2. AI calculates valid moves from current position
3. AI moves to chosen position
4. AI calculates valid shots from new position
5. AI shoots at chosen target
6. Turn switches to opponent

### Health System

- Each piece starts with **30 HP**
- Health bars show current status with color coding:
  - 🟢 Green: >60% health (18-30 HP)
  - 🟡 Yellow: 30-60% health (9-17 HP)
  - 🔴 Red: <30% health (1-8 HP)
- Health pickups spawn randomly on the board after each turn (not yet implemented for collection)
- Dead pieces (HP ≤ 0) are removed from play permanently

### Win Conditions

The game ends when:

1. **Elimination Victory**: All pieces of one team are eliminated
2. **Stalemate**: Both teams have no valid actions for 2 consecutive turns
   - Winner determined by:
     - Piece count (more alive pieces wins)
     - If tied, total health remaining
     - If still tied, declared a Draw

### Game Controls

- **Mouse Click**: Select pieces, choose moves, and shoot targets
- **Reset Button**: Restart the game after game over
- **Exit Button**: Close the game

### AI Configuration

Modify these variables in `main.py` to customize AI behavior:

```python
AI_ENABLED = True        # Enable/disable AI vs AI mode
AI_DELAY = 0.5          # Delay between AI moves (seconds)
MINIMAX_DEPTH = 3       # Search depth (higher = smarter but slower)
MAX_NO_ACTIONS = 2      # Consecutive turns without valid actions before stalemate
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
  5. Advance toward enemy territory (2 points per row advancement)

#### Blue AI - Defensive Heuristic

- **Goal**: Survival and opportunistic damage
- **Priorities**:
  1. Preserve own pieces (800 points per alive piece + 20 points per HP)
  2. Maintain high health (30 point bonus for pieces with ≥25 HP)
  3. Defensive positioning (3 points per turn for staying in safe zones)
  4. Opportunistic damage (5 points per enemy HP lost, 300 per kill)
  5. Avoid risky engagements and maintain formation

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
main.py (~1500 lines)
├── Game Setup & Constants
│   ├── Window configuration (800x860)
│   ├── Team initialization (pieces, guns, locations, health)
│   ├── Game state variables
│   └── Asset loading (images, sounds)
│
├── Graphics & Rendering Functions
│   ├── draw_board() - Checkerboard with grid lines
│   ├── draw_piece() - Pieces with shadows, health bars, selection highlights
│   ├── draw_ui_info() - Turn indicator and team status panel
│   ├── draw_valid() - Movement indicators with pulsing effects
│   ├── draw_valid_shoot() - Crosshair targeting markers
│   └── draw_game_over_popup() - Victory screen with buttons
│
├── Game Logic Functions
│   ├── Movement Validation
│   │   ├── check_option() - Get all valid moves for all pieces
│   │   ├── check_circle() - Cardinal direction movement (1-2 squares)
│   │   ├── check_square() - Diagonal movement (1-2 squares)
│   │   └── check_triangle() - 8-directional movement (1 square)
│   │
│   ├── Shooting Mechanics
│   │   ├── check_shoot() - Get all valid shoot targets
│   │   ├── check_short_gun() - Straight line shots (1-2 range)
│   │   ├── check_long_gun() - Diagonal shots (1-2 range)
│   │   ├── check_blast() - Fixed 2-distance AOE targeting
│   │   └── blast_damage() - Calculate area damage with friendly fire
│   │
│   ├── Health Management
│   │   ├── check_healths() - Update dead pieces and check win conditions
│   │   ├── check_stalemate() - Detect no-action stalemates
│   │   └── spawn_health_pickup() - Random health pickup generation
│   │
│   └── Game Control
│       ├── reset_game() - Reset all variables to initial state
│       └── Event handling (mouse clicks, buttons)
│
└── AI System (Minimax Implementation)
    ├── GameState class
    │   ├── __init__() - Store board state snapshot
    │   ├── copy() - Deep copy for simulation
    │   └── is_terminal() - Check game over condition
    │
    ├── simulate_move_and_shoot() - Apply action and return new state
    │
    ├── Heuristic Functions
    │   ├── heuristic_aggressive() - Red AI evaluation (offense-focused)
    │   └── heuristic_defensive() - Blue AI evaluation (defense-focused)
    │
    ├── Action Generation
    │   └── get_all_possible_actions() - Generate all valid (move, shoot) pairs
    │
    ├── Search Algorithm
    │   ├── minimax_alpha_beta() - Recursive tree search with pruning
    │   └── ai_decide_action_minimax() - Top-level AI decision maker
    │
    └── Game Loop Integration
        └── Turn-by-turn AI execution with visualization delay
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

**Gameplay Enhancements:**

- Add player vs AI mode with mouse input handling
- Implement health pickup collection mechanics
- Add special abilities or power-ups
- Create new piece types with unique movement patterns
- Design new weapon types with different mechanics

**AI Improvements:**

- Implement different difficulty levels
- Add Monte Carlo Tree Search (MCTS) as alternative AI
- Create tournament mode with multiple AI strategies
- Add learning/adaptive AI that improves over games

**Visual & Audio:**

- Add particle effects for explosions and hits
- Implement smooth piece movement animations
- Create more sound effects and music tracks
- Add themes/skins for pieces and board

**Technical:**

- Add game replays and save/load functionality
- Implement multiplayer networking
- Create AI vs AI tournament statistics
- Add performance profiling and optimization

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**tashib11**

- GitHub: [@tashib11](https://github.com/tashib11)
- Repository: [SquidStrike](https://github.com/tashib11/SquidStrike)
- Project Type: AI Lab Assignment (Academic Project)
- Course: 4-1 Semester, AI Laboratory

---

## 🙏 Acknowledgments

- **Inspiration**: Squid Game series and classic strategy board games (Chess, Checkers)
- **Game Engine**: Built with [Pygame](https://www.pygame.org/) - Python game development library
- **AI Concepts**:
  - Minimax algorithm from game theory (John von Neumann, 1928)
  - Alpha-Beta pruning optimization (McCarthy, 1956)
  - Heuristic evaluation functions from chess engines
- **Educational Resources**:
  - Game theory and adversarial search algorithms
  - Python programming and object-oriented design
  - Computer graphics and event-driven programming

**Special Thanks**:

- Pygame community for excellent documentation and examples
- Classic AI game research papers and implementations
- Strategy game design principles from board game designers

---

## 🎓 Learning Outcomes

This project demonstrates:

- ✅ Implementation of minimax algorithm with alpha-beta pruning
- ✅ Game state representation and action space modeling
- ✅ Heuristic function design for different playing styles
- ✅ Event-driven programming with Pygame
- ✅ Object-oriented design for game systems
- ✅ Performance optimization through pruning techniques
- ✅ User interface design and visualization
- ✅ Audio integration and resource management

---

<div align="center">

### 🌟 Star this repository if you found it helpful!

**Perfect for**: AI students, game developers, Python learners, strategy game enthusiasts

Made with ❤️ and ☕ | Built for learning and fun! 🎮

</div>"
