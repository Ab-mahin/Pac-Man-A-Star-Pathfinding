# 🎮 Pacman Game

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.7+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Pygame-2.0+-green.svg" alt="Pygame">
  <img src="https://img.shields.io/badge/License-Educational-yellow.svg" alt="License">
</p>

<p align="center">
  <b>A classic Pacman game implemented in Python using Pygame</b><br>
  Navigate through the maze, eat all the food pellets, and avoid the ghosts!
</p>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎯 **Classic Gameplay** | Authentic Pacman experience with maze navigation |
| 👻 **4 Unique Ghosts** | Blinky, Pinky, Inky, and Clyde with distinct AI behaviors |
| ⚡ **Power-ups** | Eat bonus pellets to turn the tables on ghosts |
| 🧠 **A* Pathfinding** | Intelligent ghost AI using A* algorithm |
| ⚙️ **Configurable** | Easy JSON-based configuration for all game parameters |
| 🎨 **Custom Colors** | Fully customizable color scheme |

---

## 📁 Project Structure

```
pacman-main/
├── 🐍 pacman.py              # Main game code
├── ⚙️ pacman_config.json     # Configuration file
├── 📁 Pacman/
│   └── 📁 Image/
│       ├── 🖼️ PacmanBoard.png
│       ├── 🟡 pacman.png
│       ├── 🔴 Blinky.png
│       ├── 🩷 Pinky.png
│       ├── 🩵 Inky.png
│       └── 🟠 Clyde.png
└── 📄 PACMAN_README.md
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Pygame library

### Installation

```bash
# 1. Install Pygame
pip install pygame

# 2. Navigate to game directory
cd pacman-main

# 3. Run the game
python pacman.py
```

---

## 🎮 Controls

<p align="center">

| Key | Action |
|:---:|:------:|
| ⬆️ `↑` | Move Up |
| ⬇️ `↓` | Move Down |
| ⬅️ `←` | Move Left |
| ➡️ `→` | Move Right |
| ↩️ `Enter` | Restart Game |

</p>

---

## ⚙️ Configuration

All game settings can be customized in `pacman_config.json`:

### 🖥️ Display Settings

```json
{
    "display": {
        "scale": 20,        // Grid cell size (pixels)
        "width": 560,       // Window width
        "height": 620,      // Window height
        "fps": 60,          // Frames per second
        "title": "Pacman"   // Window title
    }
}
```

### 🎮 Gameplay Settings

| Parameter | Default | Description |
|-----------|:-------:|-------------|
| `pacman_speed` | 2.5 | Pacman movement speed |
| `ghost_speed` | 2.5 | Normal ghost speed |
| `ghost_weak_speed` | 1.25 | Vulnerable ghost speed |
| `weak_duration` | 300 | Power-up duration (frames) |
| `show_ghost_paths` | false | Debug: visualize AI paths |

### 🏆 Scoring System

| Event | Points |
|-------|:------:|
| 🟡 Food Pellet | +10 |
| ⭐ Power Pellet | +50 |
| 👻 Eat Ghost | +200 |

### 🎨 Color Customization

Colors are defined in RGB format `[R, G, B]`:

```json
{
    "colors": {
        "background": [55, 50, 60],
        "wall": [45, 45, 75],
        "path": [160, 170, 185],
        "pacman": [255, 255, 0],
        "food": [255, 220, 50],
        "blinky": [255, 95, 95],
        "pinky": [255, 184, 255],
        "inky": [0, 255, 255],
        "clyde": [255, 184, 81],
        "weak": [27, 112, 247]
    }
}
```

---

## 👻 Ghost Behaviors

Each ghost has a unique personality and hunting strategy:

| Ghost | Color | Personality | Strategy |
|:-----:|:-----:|:-----------:|----------|
| **Blinky** | 🔴 Red | "Shadow" | Directly chases Pacman - the most aggressive |
| **Pinky** | 🩷 Pink | "Speedy" | Ambushes by targeting 4 tiles ahead of Pacman |
| **Inky** | 🩵 Cyan | "Bashful" | Uses Blinky's position for unpredictable moves |
| **Clyde** | 🟠 Orange | "Pokey" | Chases when far, retreats when close |

### Ghost States

```
Normal Mode          Power-up Mode         Recovery Mode
    👻          →         💙          →         👻
  (hunting)         (vulnerable)          (returning)
```

---

## 🗺️ Map Elements

| Symbol | Visual | Description |
|:------:|:------:|-------------|
| `1` | ⬛ | Wall - impassable |
| `0` | ⬜ | Empty path |
| `2` | 🟡 | Food pellet (+10 pts) |
| `3` | ⭐ | Power pellet (+50 pts) |
| `-` | 🚪 | Teleport tunnel |

---

## 🎯 How to Play

### Objective
> Eat all food pellets (🟡) and power pellets (⭐) to win!

### Tips & Strategies

1. **Learn the Patterns** 
   - Each ghost has predictable behavior - use it to your advantage

2. **Use Power Pellets Wisely**
   - Save them for when multiple ghosts are nearby
   - Eating ghosts gives 200 points each!

3. **Master the Tunnels**
   - Side tunnels teleport you across the map
   - Ghosts slow down in tunnels - use this to escape

4. **Corner Cutting**
   - Pre-turn around corners to maintain speed
   - Ghosts can't cut corners as efficiently

5. **Safe Zones**
   - The ghost house area is temporarily safe after power-ups

---

## 🖼️ Game Preview

```
╔══════════════════════════════════════════════════════╗
║  ● · · · · · █ · · · · · ██ · · · · · █ · · · · · ●  ║
║  █ · · · █ · ████ · · · ██ · · · ████ · █ · · · █    ║
║  · · · · · · · · · · · · · · · · · · · · · · · · ·   ║
║  █ · · · █ · ██ · ████████████ · ██ · █ · · · █      ║
║  · · · · · · ██ · · · · ██ · · · · ██ · · · · ·      ║
║  █████████ · ████ · · · ██ · · · ████ · █████████    ║
║            · ██ · · · · · · · · · ██ ·               ║
║  █████████ · ██ · ███ 👻👻👻 ███ · ██ · █████████     ║
║  · · · · · · · · │  GHOST   │ · · · · · · ·          ║
║  █████████ · ██ · │  HOUSE  │ · ██ · █████████       ║
║            · ██ · ███████████ · ██ ·                 ║
║  █████████ · ██ · · · · · · · · ██ · █████████       ║
║  · · · · · · · · · · · · · · · · · · · · · · ·       ║
║  █ · · · █ · ████ · · · ██ · · · ████ · █ · · · █    ║
║  ● · ██ · · · · · · 😀 · · · · · · · ██ · ●          ║
║  ██ · ██ · ██ · ████████████ · ██ · ██ · ██          ║
║  · · · · · · · · · · · · · · · · · · · · · · ·       ║
║  █ · ████████████ · ██ · ████████████ · █            ║
║  ● · · · · · · · · · · · · · · · · · · · · · ●       ║
╚══════════════════════════════════════════════════════╝

         😀 = Pacman    👻 = Ghosts    ● = Power Pellet
```

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: pygame` | Run `pip install pygame` |
| Game runs slowly | Lower `fps` in config or close other apps |
| Colors look wrong | Check RGB values in `pacman_config.json` |
| Ghosts not moving | Verify `ghost_speed` > 0 in config |

---

## 📜 License

This project is for **educational purposes**.

---

## 🙏 Credits

- **Original Pacman** - Namco (1980)
- **Python/Pygame Port** - Educational Implementation
- **A* Algorithm** - Peter Hart, Nils Nilsson, Bertram Raphael

---

<p align="center">
  <b>🎮 Have Fun Playing! 🎮</b><br>
  <sub>Made with ❤️ and Python</sub>
</p>
