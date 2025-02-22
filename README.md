# Tic Tac Toe Game

## Overview
This is a simple Tic Tac Toe game built with Flask for the backend and HTML/CSS/JavaScript for the frontend. The game supports both multiplayer and single-player modes with varying difficulty levels (Easy, Medium, Hard).

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [How to Play](#how-to-play)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Features
- **Multiplayer Mode:** Two players can play against each other.
- **Single-Player Mode:** Play against the computer with three difficulty levels:
  - *Easy*
  - *Medium*
  - *Hard*
- **Dynamic Game Board:** Interactive board that updates based on player moves.
- **Score Tracking:** Keeps track of wins, losses, draws, and match progress (best of 10 games).

## Installation

### Prerequisites
- Python 3.x
- [Flask](https://flask.palletsprojects.com/) web framework

### Setup Steps
1. **Clone or Download the Repository:**  
   Clone the repository or download the project files into your desired directory.
2. **Navigate to the Project Directory:**  
   Open your terminal/command prompt and change to the project directory.
3. **Install Dependencies:**  
   Install Flask using pip:
   \`\`\`bash
   pip install flask
   \`\`\`

## Usage
1. **Run the Application:**  
   Start the Flask server by running:
   \`\`\`bash
   python app.py
   \`\`\`
2. **Access the Game:**  
   Open your web browser and navigate to:
   \`\`\`
   http://127.0.0.1:5000/
   \`\`\`
3. **Play the Game:**  
   - Choose your game mode (Multiplayer or Single-Player).
   - For single-player mode, select your symbol and difficulty.
   - Enjoy playing Tic Tac Toe!

## Project Structure
\`\`\`
TicTacToe/
├── app.py          # Backend Flask application handling game logic and API endpoints.
├── index.html      # Main HTML file that serves the game UI.
├── script.js       # JavaScript file handling game functionality and API interactions.
├── style.css       # CSS file for styling the game interface.
└── README.md       # This file.
\`\`\`

## How to Play
- **Multiplayer Mode:**  
  Enter player names for X and O. Players take turns clicking on the board to place their symbol.
  
- **Single-Player Mode:**  
  Choose your symbol (X or O) and the difficulty level. Play against the computer which makes its move automatically.
  
- **Match Rules:**  
  The game is played over a series of 10 games. Wins, losses, and draws are tracked to determine the overall match winner.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for further details.

## Acknowledgements
- Thanks to all contributors and the open source community.
- Inspired by classic Tic Tac Toe games.