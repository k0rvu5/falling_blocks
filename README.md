# Falling Blocks

Falling Blocks is a fast-paced, arcade-style game written in Python using [pygame](https://www.pygame.org/). Dodge falling squares for as long as possible and try to beat your high score!

---

## 🕹️ Gameplay

- **Goal:** Survive as long as possible by avoiding the falling colored squares ("blocks").
- Your score increases the longer you stay alive. If a block touches you, it's game over!

### Controls

- **Move:**  
  - Use your **mouse** to control the player block,  
  - or use the **arrow keys** or **HJKL keys** (Vim-style movement):
    - Left: ← or H
    - Right: → or L
    - Up: ↑ or K
    - Down: ↓ or J
- **Pause/Unpause:** `P`
- **Restart after game over:** `Space`
- **Return to Menu:** `Esc`
- **Quit:** Close the window or use `Esc` from the menu.

---

## 🏆 Features

- **Difficulty Modes:** Easy, Medium, Hard—affect speed and spawn rate of falling blocks.
- **Persistent High Score:** Your best score is saved between runs.
- **Starry Background:** Animated stars for a retro arcade feel.
- **Soundtrack:** Background music (if `background_music.mp3` is present).
- **Colorful & Dynamic Obstacles:** Each game is visually unique.
- **User-friendly Menu:** Start game, change difficulty, or quit.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- [pygame](https://www.pygame.org/)  

### Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/k0rvu5/falling_blocks.git
   cd falling_blocks
   ```

2. **Install dependencies:**
   ```sh
   pip install pygame
   ```

3. *(Optional)* Add a file named `background_music.mp3` in the root directory for background music.

### Run the Game

```sh
python main.py
```

---

## 📁 Project Structure

```
falling_blocks/
├── main.py                # Main game logic and entry point
├── README.md
├── game_save.json         # (auto-generated) Stores high score/difficulty
├── background_music.mp3   # (optional) Music file for background soundtrack
└── ... (other assets)
```

---

## ⚙️ Settings & Data

- **High Score & Difficulty:**  
  Saved automatically in `game_save.json` in the project directory.
- **Music:**  
  If `background_music.mp3` is missing, the game plays silently.

---

## 🤝 Contributing

Pull requests, suggestions, and bug reports are welcome!  
Please open an issue or PR if you have ideas for improvements.

---

## 📜 License

MIT License. See [LICENSE](LICENSE) for details.

---

## 🙏 Credits

- Developed by [k0rvu5](https://github.com/k0rvu5)
- Built with [pygame](https://www.pygame.org/)

---

Enjoy the game!
