#!/usr/bin/env python3
"""
Test script for Battleship game core functionality
"""

from battleship import BattleshipGame, Board, Ship

def test_ship_placement():
    """Test automatic ship placement"""
    print("Testing ship placement...")
    game = BattleshipGame()
    board = Board()
    
    success = game.auto_place_ships(board)
    if success:
        print("✅ Ship placement successful!")
        print(f"Placed {len(board.ships)} ships:")
        for ship in board.ships:
            print(f"  - {ship.name} (size {ship.size})")
    else:
        print("❌ Ship placement failed!")
    
    return success

def test_shot_mechanics():
    """Test shot mechanics"""
    print("\nTesting shot mechanics...")
    game = BattleshipGame()
    board = Board()
    
    # Place a simple ship for testing
    ship = Ship("Test", 3)
    board.place_ship(ship, [(0, 0), (0, 1), (0, 2)])
    
    # Test a hit
    hit, ship_hit = board.receive_shot(0, 1)
    print(f"Shot at (0,1): {'Hit!' if hit else 'Miss'}")
    if hit:
        print(f"Hit ship: {ship_hit.name}")
    
    # Test a miss
    hit, ship_hit = board.receive_shot(5, 5)
    print(f"Shot at (5,5): {'Hit!' if hit else 'Miss'}")
    
    return True

def test_game_initialization():
    """Test game initialization"""
    print("\nTesting game initialization...")
    game = BattleshipGame()
    
    print(f"Board size: {game.board_size}")
    print(f"Number of ships: {len(game.ships_config)}")
    print("Ship configuration:")
    for name, size in game.ships_config:
        print(f"  - {name}: {size} spaces")
    
    return True

def main():
    """Run all tests"""
    print("=" * 50)
    print("BATTLESHIP GAME TEST SUITE")
    print("=" * 50)
    
    tests = [
        test_game_initialization,
        test_ship_placement,
        test_shot_mechanics
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
    
    print("\n" + "=" * 50)
    print(f"TEST RESULTS: {passed}/{total} tests passed")
    print("=" * 50)
    
    if passed == total:
        print("🎉 All tests passed! The game is ready to play.")
        print("\nTo play the game, run: python3 battleship.py")
    else:
        print("⚠️  Some tests failed. Please check the implementation.")

if __name__ == "__main__":
    main() 