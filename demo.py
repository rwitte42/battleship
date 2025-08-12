#!/usr/bin/env python3
"""
Demo script for Battleship game - shows a quick computer vs computer match
"""

from battleship import BattleshipGame
import time

def run_demo():
    """Run a quick demo of the battleship game"""
    print("=" * 60)
    print("BATTLESHIP GAME DEMO")
    print("Computer vs Computer - Quick Match")
    print("=" * 60)
    print()
    
    game = BattleshipGame()
    
    # Set up the game
    print("Setting up the game...")
    if not game.auto_place_ships(game.player_board):
        print("Error: Could not place computer 1 ships.")
        return
    
    if not game.auto_place_ships(game.computer_board):
        print("Error: Could not place computer 2 ships.")
        return
    
    print("✅ Ships placed successfully!")
    print()
    
    # Show initial board setup
    print("Computer 1's board (ships hidden):")
    game.player_board.display_guess_board()
    print()
    
    print("Computer 2's board (ships hidden):")
    game.computer_board.display_guess_board()
    print()
    
    # Run the game with automatic turns
    print("Starting the battle...")
    print("-" * 40)
    
    turn = 0
    max_turns = 50  # Prevent infinite loops
    
    while turn < max_turns:
        turn += 1
        print(f"\n=== TURN {turn} ===")
        
        # Computer 1's turn
        row, col = game.get_computer_shot()
        hit, ship = game.computer_board.receive_shot(row, col)
        print(f"Computer 1 shoots at {chr(65 + col)}{row}: ", end="")
        
        if hit:
            print(f"💥 HIT! {ship.name}")
            if ship.is_sunk():
                print(f"🚢 Computer 1 sunk the {ship.name}!")
        else:
            print("💨 MISS!")
        
        # Show board after Computer 1's shot
        print("\n" + "=" * 80)
        print("BOARD AFTER COMPUTER 1'S SHOT")
        print("=" * 80)
        game.display_game_state()
        
        if game.computer_board.all_ships_sunk():
            print("\n🎉 COMPUTER 1 WINS!")
            print(f"Game completed in {turn} turns")
            break
        
        # Computer 2's turn
        row, col = game.get_computer_shot()
        hit, ship = game.player_board.receive_shot(row, col)
        print(f"Computer 2 shoots at {chr(65 + col)}{row}: ", end="")
        
        if hit:
            print(f"💥 HIT! {ship.name}")
            if ship.is_sunk():
                print(f"🚢 Computer 2 sunk the {ship.name}!")
        else:
            print("💨 MISS!")
        
        # Show board after Computer 2's shot
        print("\n" + "=" * 80)
        print("BOARD AFTER COMPUTER 2'S SHOT")
        print("=" * 80)
        game.display_game_state()
        
        if game.player_board.all_ships_sunk():
            print("\n🎉 COMPUTER 2 WINS!")
            print(f"Game completed in {turn} turns")
            break
        
        # Brief pause to make it readable
        time.sleep(0.5)
    
    if turn >= max_turns:
        print(f"\n⚠️  Game stopped after {max_turns} turns (preventing infinite loop)")
    
    print("\n" + "=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)
    print("\nTo play yourself, run: python3 battleship.py")

if __name__ == "__main__":
    run_demo() 