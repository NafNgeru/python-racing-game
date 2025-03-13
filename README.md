# 2D Racing Game

## Overview
This is a **2D Racing Game** built using **Python** and **Pygame**. The player controls a car on a track, navigating around obstacles and attempting to complete the race as quickly as possible. The game features smooth car movement, collision detection, and a timer to track progress.

## Features
- **Player-controlled car:** Move forward, backward, and rotate left or right.
- **Real-time timer:** Tracks the time taken to complete the race.
- **Collision detection:** Prevents the player from driving off the track.
- **Finish line detection:** Ends the race when the player crosses the finish line.

## Installation
### Prerequisites
Make sure you have Python installed. You also need to install Pygame:

```bash
pip install pygame
```

### Clone the Repository
```bash
git clone https://github.com/your-repo/2D-Racing-Game.git
cd 2D-Racing-Game
```

## Running the Game
Run the following command to start the game:

```bash
python main.py
```

## Controls
| Key  | Action |
|------|--------|
| Left Arrow  | Rotate Left |
| Right Arrow | Rotate Right |
| Up Arrow    | Move Forward |
| Down Arrow  | Move Backward |

## File Structure
```
2D-Racing-Game/
│-- game_images/        # Folder containing all images (track, cars, etc.)
│-- util.py             # Utility functions (scaling, blitting, etc.)
│-- main.py             # Main game logic
│-- README.md           # Project documentation
```

## Known Issues
- Collision detection may need fine-tuning for better accuracy.

## Future Improvements
- Adding multiple difficulty levels.
- Implementing a multiplayer mode.
- Enhancing graphics and animations.

## Credits
This game was developed using **Pygame** and Python. Special thanks to open-source resources for images and inspiration.

## License
This project is licensed under the MIT License.

