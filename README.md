# Battleship Game

A classic Battleship game implementation in Python with CLI interface.

## Features

- **Single Player Mode**: Play against the computer
- **Computer vs Computer Mode**: Watch two AI players battle it out
- **Auto Ship Placement**: Ships are automatically placed for both players
- **Standard Rules**: Uses classic Battleship rules and ship configurations
- **Enhanced Visual Interface**: Beautiful emoji-based display with side-by-side boards
- **Separate Fleet and Target Boards**: Clear distinction between your ships and your guesses
- **Real-time Ship Status**: Visual indicators for hits, misses, and sunk ships

## Ship Configuration

The game uses the standard Battleship fleet:
- **Carrier**: 5 spaces
- **Battleship**: 4 spaces  
- **Cruiser**: 3 spaces
- **Submarine**: 3 spaces
- **Destroyer**: 2 spaces

## How to Play

### Setup

1. Make sure you have Python 3.6+ installed
2. Navigate to the project directory
3. Run the game: `python battleship.py`

### Game Modes

1. **Single Player**: You vs Computer
   - Ships are automatically placed for both players
   - Take turns firing shots at each other's boards
   - First to sink all enemy ships wins

2. **Computer vs Computer**: Demo mode
   - Watch two AI players battle it out
   - Useful for testing or demonstration

### Gameplay

- **Board Display**: 
  - **Fleet Board**: Shows your ships with emoji symbols and shot results
  - **Target Board**: Shows your guesses on the computer's board (❓ for unknown, 💥 for hits, 💨 for misses)
  - **Side-by-side Layout**: Both boards displayed simultaneously for easy comparison
  - **Ship Status**: Real-time status of your ships with hit counts and sunk indicators

- **Taking Shots**:
  - Enter coordinates in format: `A5` (letter + number)
  - Letters A-J represent columns (left to right)
  - Numbers 0-9 represent rows (top to bottom)
  - Clear visual feedback for hits and misses

- **Game Flow**:
  - You and the computer take turns
  - Each turn consists of one shot
  - Hits are marked with 'X', misses with 'O'
  - When a ship is completely hit, it's considered sunk
  - First player to sink all enemy ships wins

## Board Legend

### Fleet Board (Your Ships)
- **🚢**: Carrier (5 spaces)
- **🛥️**: Battleship (4 spaces)
- **🚤**: Cruiser/Submarine (3 spaces)
- **⛵**: Destroyer (2 spaces)
- **💥**: Hit on your ship
- **💨**: Miss on your ship
- **🌊**: Water

### Target Board (Your Guesses)
- **❓**: Unknown/Unshot location
- **💥**: Hit on enemy ship
- **💨**: Miss

### Ship Status
- **💀**: Ship sunk
- **💥**: Ship damaged (shows hit count)
- **🚢**: Ship undamaged

## Future Enhancements

This CLI version is the foundation for future improvements:
- Web-based GUI using Flask/Django
- Desktop GUI using Tkinter or PyQt
- Multiplayer support
- Advanced AI strategies
- Custom board sizes
- Manual ship placement option

## Requirements

- Python 3.6+
- No external dependencies required

## Running the Game

```bash
# Activate virtual environment (if using one)
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows

# Run the game
python battleship.py
```

Enjoy playing Battleship! 