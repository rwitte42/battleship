#!/usr/bin/env python3
"""
Demo script to show board updates after each turn
"""

from battleship import BattleshipGame
import time

def demo_turn_updates():
    """Demonstrate board updates after each turn"""
    print("=" * 80)
    print("🚢 BATTLESHIP - TURN-BY-TURN BOARD UPDATES DEMO 🚢")
    print("=" * 80)
    print()
    
    game = BattleshipGame()
    
    # Set up the game
    print("Setting up the game...")
    game.auto_place_ships(game.player_board)
    game.auto_place_ships(game.computer_board)
    print("✅ Ships placed successfully!")
    print()
    
    # Show initial state
    print("INITIAL GAME STATE:")
    print("=" * 80)
    game.display_game_state()
    
    # Simulate a few turns
    turns = [
        # (player_shot, computer_shot)
        ((0, 0), (1, 1)),  # Both miss
        ((2, 2), (3, 3)),  # Both miss
        ((4, 4), (5, 5)),  # Both miss
        ((6, 6), (7, 7)),  # Both miss
        ((8, 8), (9, 9)),  # Both miss
    ]
    
    for i, (player_shot, computer_shot) in enumerate(turns, 1):
        print(f"\n{'='*80}")
        print(f"TURN {i}")
        print(f"{'='*80}")
        
        # Player's turn
        print("🎯 Player's turn...")
        row, col = player_shot
        hit, ship = game.computer_board.receive_shot(row, col)
        
        if hit:
            print(f"💥 Hit! Player hit the computer's {ship.name}!")
            if ship.is_sunk():
                print(f"🚢 Player sunk the computer's {ship.name}!")
        else:
            print(f"💨 Miss! Player shot at {chr(65 + col)}{row}")
        
        # Show board after player's shot
        print(f"\n{'='*80}")
        print("BOARD AFTER PLAYER'S SHOT")
        print(f"{'='*80}")
        game.display_game_state()
        
        # Computer's turn
        print("🤖 Computer's turn...")
        row, col = computer_shot
        hit, ship = game.player_board.receive_shot(row, col)
        
        if hit:
            print(f"💥 Hit! Computer hit player's {ship.name}!")
            if ship.is_sunk():
                print(f"🚢 Computer sunk player's {ship.name}!")
        else:
            print(f"💨 Miss! Computer shot at {chr(65 + col)}{row}")
        
        # Show board after computer's shot
        print(f"\n{'='*80}")
        print("BOARD AFTER COMPUTER'S SHOT")
        print(f"{'='*80}")
        game.display_game_state()
        
        if i < len(turns):  # Don't pause after the last turn
            input("\nPress Enter to continue to next turn...")
    
    print(f"\n{'='*80}")
    print("DEMO COMPLETE!")
    print(f"{'='*80}")
    print("✅ Board updates after each shot")
    print("✅ Clear visual feedback for hits and misses")
    print("✅ Real-time ship status updates")
    print("✅ Side-by-side board display")
    print("\n🎮 Ready to play! Run: python3 battleship.py")

if __name__ == "__main__":
    demo_turn_updates()
