#!/usr/bin/env python3
"""
Showcase script to demonstrate the enhanced Battleship CLI interface
"""

from battleship import BattleshipGame, Board, Ship
import time

def showcase_enhanced_interface():
    """Showcase the enhanced CLI interface"""
    print("=" * 80)
    print("🚢 BATTLESHIP GAME - ENHANCED CLI INTERFACE SHOWCASE 🚢")
    print("=" * 80)
    print()
    
    game = BattleshipGame()
    
    # Set up a sample game state
    print("Setting up sample game state...")
    
    # Place ships for player
    game.auto_place_ships(game.player_board)
    
    # Place ships for computer
    game.auto_place_ships(game.computer_board)
    
    # Simulate some shots for demonstration
    print("Simulating some gameplay for demonstration...")
    
    # Player takes some shots
    sample_shots = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    for row, col in sample_shots:
        hit, ship = game.computer_board.receive_shot(row, col)
        if hit:
            print(f"Player hit at {chr(65 + col)}{row}: {ship.name}")
        else:
            print(f"Player missed at {chr(65 + col)}{row}")
    
    # Computer takes some shots
    computer_shots = [(0, 1), (1, 2), (2, 3), (3, 4)]
    for row, col in computer_shots:
        hit, ship = game.player_board.receive_shot(row, col)
        if hit:
            print(f"Computer hit at {chr(65 + col)}{row}: {ship.name}")
        else:
            print(f"Computer missed at {chr(65 + col)}{row}")
    
    print()
    print("=" * 80)
    print("ENHANCED GAME INTERFACE")
    print("=" * 80)
    print()
    
    # Display the enhanced game state
    game.display_game_state()
    
    print()
    print("=" * 80)
    print("INTERFACE FEATURES:")
    print("=" * 80)
    print("✅ Side-by-side board display")
    print("✅ Emoji-based ship and status indicators")
    print("✅ Clear distinction between fleet and target boards")
    print("✅ Real-time ship status with hit counts")
    print("✅ Visual legend for all symbols")
    print("✅ Enhanced readability and user experience")
    print()
    print("🎮 Ready to play! Run: python3 battleship.py")

if __name__ == "__main__":
    showcase_enhanced_interface() 