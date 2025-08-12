import random
import os
import time
from typing import List, Tuple, Optional

class Ship:
    """Represents a ship in the battleship game"""
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size
        self.positions = []
        self.hits = set()
    
    def is_sunk(self) -> bool:
        """Check if the ship is completely sunk"""
        return len(self.hits) == self.size
    
    def place_ship(self, positions: List[Tuple[int, int]]):
        """Place the ship on the board"""
        self.positions = positions
    
    def hit(self, position: Tuple[int, int]) -> bool:
        """Record a hit on the ship"""
        if position in self.positions:
            self.hits.add(position)
            return True
        return False

class Board:
    """Represents a battleship game board"""
    def __init__(self, size: int = 10):
        self.size = size
        self.grid = [[' ' for _ in range(size)] for _ in range(size)]
        self.ships = []
        self.shots_fired = set()
        self.hits = set()
        self.misses = set()
    
    def is_valid_position(self, row: int, col: int) -> bool:
        """Check if a position is within the board boundaries"""
        return 0 <= row < self.size and 0 <= col < self.size
    
    def is_valid_placement(self, positions: List[Tuple[int, int]]) -> bool:
        """Check if ship placement is valid (within bounds and not overlapping)"""
        for row, col in positions:
            if not self.is_valid_position(row, col):
                return False
            if self.grid[row][col] != ' ':
                return False
        return True
    
    def place_ship(self, ship: Ship, positions: List[Tuple[int, int]]) -> bool:
        """Place a ship on the board"""
        if not self.is_valid_placement(positions):
            return False
        
        ship.place_ship(positions)
        self.ships.append(ship)
        
        # Mark ship positions on the grid
        for row, col in positions:
            self.grid[row][col] = ship.name[0].upper()
        
        return True
    
    def receive_shot(self, row: int, col: int) -> Tuple[bool, Optional[Ship]]:
        """Process a shot and return (hit, ship_hit)"""
        if not self.is_valid_position(row, col):
            return False, None
        
        if (row, col) in self.shots_fired:
            return False, None  # Already shot here
        
        self.shots_fired.add((row, col))
        
        if self.grid[row][col] != ' ':
            # Hit a ship
            self.hits.add((row, col))
            self.grid[row][col] = 'X'
            
            # Find which ship was hit
            for ship in self.ships:
                if ship.hit((row, col)):
                    return True, ship
        else:
            # Miss
            self.misses.add((row, col))
            self.grid[row][col] = 'O'
        
        return False, None
    
    def all_ships_sunk(self) -> bool:
        """Check if all ships are sunk"""
        return all(ship.is_sunk() for ship in self.ships)
    
    def display(self, show_ships: bool = False):
        """Display the board"""
        # Print column headers
        print("   " + " ".join([chr(65 + i) for i in range(self.size)]))
        
        for row in range(self.size):
            # Print row header
            print(f"{row:2d} ", end="")
            
            for col in range(self.size):
                cell = self.grid[row][col]
                if not show_ships and cell not in ['X', 'O'] and cell != ' ':
                    cell = ' '  # Hide ships when not showing them
                
                # Enhanced display with better symbols
                if cell == 'X':
                    print("💥 ", end="")  # Hit
                elif cell == 'O':
                    print("💨 ", end="")  # Miss
                elif cell == ' ':
                    print("🌊 ", end="")  # Water
                else:
                    # Ship display
                    ship_symbols = {
                        'C': '🚢',  # Carrier
                        'B': '🛥️ ',  # Battleship
                        'S': '🚤',  # Submarine/Cruiser
                        'D': '⛵'   # Destroyer
                    }
                    symbol = ship_symbols.get(cell, cell)
                    print(f"{symbol} ", end="")
            print()
    
    def display_guess_board(self):
        """Display the board for guessing (opponent's board)"""
        # Print column headers
        print("   " + " ".join([chr(65 + i) for i in range(self.size)]))
        
        for row in range(self.size):
            # Print row header
            print(f"{row:2d} ", end="")
            
            for col in range(self.size):
                if (row, col) in self.shots_fired:
                    if (row, col) in self.hits:
                        print("💥 ", end="")  # Hit
                    else:
                        print("💨 ", end="")  # Miss
                else:
                    print("❓ ", end="")  # Unknown/Unshot
            print()

class BattleshipGame:
    """Main battleship game class"""
    def __init__(self):
        self.board_size = 10
        self.ships_config = [
            ("Carrier", 5),
            ("Battleship", 4),
            ("Cruiser", 3),
            ("Submarine", 3),
            ("Destroyer", 2)
        ]
        self.player_board = Board(self.board_size)
        self.computer_board = Board(self.board_size)
        self.game_mode = None
    
    def auto_place_ships(self, board: Board) -> bool:
        """Automatically place all ships on a board"""
        for ship_name, ship_size in self.ships_config:
            ship = Ship(ship_name, ship_size)
            attempts = 0
            max_attempts = 1000
            
            while attempts < max_attempts:
                # Randomly choose orientation (horizontal or vertical)
                horizontal = random.choice([True, False])
                
                if horizontal:
                    # Place horizontally
                    row = random.randint(0, self.board_size - 1)
                    col = random.randint(0, self.board_size - ship_size)
                    positions = [(row, col + i) for i in range(ship_size)]
                else:
                    # Place vertically
                    row = random.randint(0, self.board_size - ship_size)
                    col = random.randint(0, self.board_size - 1)
                    positions = [(row + i, col) for i in range(ship_size)]
                
                if board.place_ship(ship, positions):
                    break
                
                attempts += 1
            
            if attempts >= max_attempts:
                return False  # Failed to place all ships
        
        return True
    
    def get_player_shot(self) -> Tuple[int, int]:
        """Get shot coordinates from player"""
        while True:
            try:
                shot = input("Enter your shot (e.g., A5): ").strip().upper()
                if len(shot) < 2:
                    print("Invalid input. Please enter a letter and number (e.g., A5)")
                    continue
                
                col = ord(shot[0]) - ord('A')
                row = int(shot[1:])
                
                if not (0 <= col < self.board_size and 0 <= row < self.board_size):
                    print(f"Invalid coordinates. Please enter A-{chr(65 + self.board_size - 1)} and 0-{self.board_size - 1}")
                    continue
                
                return row, col
            except (ValueError, EOFError, KeyboardInterrupt):
                print("Invalid input. Please enter a letter and number (e.g., A5)")
                raise
    
    def get_computer_shot(self) -> Tuple[int, int]:
        """Get shot coordinates from computer (simple random strategy)"""
        while True:
            row = random.randint(0, self.board_size - 1)
            col = random.randint(0, self.board_size - 1)
            
            if (row, col) not in self.player_board.shots_fired:
                return row, col
    
    def display_game_state(self):
        """Display current game state"""
        os.system('clear' if os.name == 'posix' else 'cls')
        print("=" * 80)
        print("🚢 BATTLESHIP GAME 🚢")
        print("=" * 80)
        print()
        
        # Display boards side by side
        print("YOUR FLEET BOARD (Your Ships)                    YOUR TARGET BOARD (Computer's Ships)")
        print("=" * 60 + "    " + "=" * 60)
        
        # Get both board displays
        player_lines = self._get_board_lines(self.player_board, show_ships=True)
        target_lines = self._get_guess_board_lines(self.computer_board)
        
        # Display side by side
        for i in range(len(player_lines)):
            print(f"{player_lines[i]:<60}    {target_lines[i]}")
        
        print()
        print("-" * 80)
        
        # Show ship status
        print("YOUR SHIPS STATUS:")
        for ship in self.player_board.ships:
            if ship.is_sunk():
                status = "💀 SUNK"
                symbol = "💀"
            else:
                hits = len(ship.hits)
                status = f"💥 {hits}/{ship.size} hits"
                symbol = "🚢" if hits == 0 else "💥"
            
            ship_symbols = {
                'Carrier': '🚢',
                'Battleship': '🛥️ ',
                'Cruiser': '🚤',
                'Submarine': '🚤',
                'Destroyer': '⛵'
            }
            ship_icon = ship_symbols.get(ship.name, '🚢')
            print(f"  {ship_icon} {ship.name}: {status}")
        
        print()
        print("LEGEND:")
        print("  🚢🛥️🚤⛵ = Your ships    💥 = Hit    💨 = Miss    🌊 = Water    ❓ = Unknown")
        print()
    
    def _get_board_lines(self, board, show_ships: bool = False):
        """Get board display as list of lines for side-by-side display"""
        lines = []
        
        # Add column headers
        header = "   " + " ".join([chr(65 + i) for i in range(board.size)])
        lines.append(header)
        
        for row in range(board.size):
            line = f"{row:2d} "
            
            for col in range(board.size):
                cell = board.grid[row][col]
                if not show_ships and cell not in ['X', 'O'] and cell != ' ':
                    cell = ' '  # Hide ships when not showing them
                
                # Enhanced display with better symbols
                if cell == 'X':
                    line += "💥 "
                elif cell == 'O':
                    line += "💨 "
                elif cell == ' ':
                    line += "🌊 "
                else:
                    # Ship display
                    ship_symbols = {
                        'C': '🚢',  # Carrier
                        'B': '🛥️ ',  # Battleship
                        'S': '🚤',  # Submarine/Cruiser
                        'D': '⛵'   # Destroyer
                    }
                    symbol = ship_symbols.get(cell, cell)
                    line += f"{symbol} "
            
            lines.append(line)
        
        return lines
    
    def _get_guess_board_lines(self, board):
        """Get guess board display as list of lines for side-by-side display"""
        lines = []
        
        # Add column headers
        header = "   " + " ".join([chr(65 + i) for i in range(board.size)])
        lines.append(header)
        
        for row in range(board.size):
            line = f"{row:2d} "
            
            for col in range(board.size):
                if (row, col) in board.shots_fired:
                    if (row, col) in board.hits:
                        line += "💥 "  # Hit
                    else:
                        line += "💨 "  # Miss
                else:
                    line += "❓ "  # Unknown/Unshot
            
            lines.append(line)
        
        return lines
    
    def play_turn(self) -> bool:
        """Play one turn of the game. Returns True if game should continue."""
        # Don't display game state here as it's handled by the calling method
        
        # Player's turn
        print("Your turn!")
        row, col = self.get_player_shot()
        hit, ship = self.computer_board.receive_shot(row, col)
        
        if hit:
            print(f"💥 Hit! You hit the computer's {ship.name}!")
            if ship.is_sunk():
                print(f"🚢 You sunk the computer's {ship.name}!")
        else:
            print("💨 Miss!")
        
        # Show updated board after player's shot
        print("\n" + "=" * 80)
        print("BOARD AFTER YOUR SHOT")
        print("=" * 80)
        self.display_game_state()
        
        if self.computer_board.all_ships_sunk():
            print("\n🎉 CONGRATULATIONS! You won!")
            return False
        
        try:
            input("\nPress Enter for computer's turn...")
        except (EOFError, KeyboardInterrupt):
            print("\nGame cancelled.")
            return False
        
        # Computer's turn
        print("\nComputer's turn...")
        row, col = self.get_computer_shot()
        hit, ship = self.player_board.receive_shot(row, col)
        
        if hit:
            print(f"💥 Computer hit your {ship.name}!")
            if ship.is_sunk():
                print(f"🚢 Computer sunk your {ship.name}!")
        else:
            print("💨 Computer missed!")
        
        # Show updated board after computer's shot
        print("\n" + "=" * 80)
        print("BOARD AFTER COMPUTER'S SHOT")
        print("=" * 80)
        self.display_game_state()
        
        if self.player_board.all_ships_sunk():
            print("\n💥 GAME OVER! Computer won!")
            return False
        
        try:
            input("\nPress Enter to continue to next turn...")
        except (EOFError, KeyboardInterrupt):
            print("\nGame cancelled.")
            return False
        return True
    
    def play_single_player(self):
        """Play single player mode (player vs computer)"""
        print("Setting up single player game...")
        
        # Place ships for both players
        if not self.auto_place_ships(self.player_board):
            print("Error: Could not place player ships. Please restart.")
            return
        
        if not self.auto_place_ships(self.computer_board):
            print("Error: Could not place computer ships. Please restart.")
            return
        
        print("Ships placed successfully!")
        try:
            input("Press Enter to start the game...")
        except (EOFError, KeyboardInterrupt):
            print("\nGame cancelled.")
            return
        
        # Main game loop
        turn = 0
        max_turns = 100  # Prevent infinite loops
        
        while turn < max_turns:
            turn += 1
            print(f"\n=== TURN {turn} ===")
            
            # Show current game state
            self.display_game_state()
            
            if not self.play_turn():
                break
        
        if turn >= max_turns:
            print(f"\n⚠️  Game stopped after {max_turns} turns (preventing infinite loop)")
        
        print("\nThanks for playing!")
    
    def play_computer_vs_computer(self):
        """Play computer vs computer mode (for testing/demo)"""
        print("Setting up computer vs computer game...")
        
        # Place ships for both computers
        if not self.auto_place_ships(self.player_board):
            print("Error: Could not place computer 1 ships.")
            return
        
        if not self.auto_place_ships(self.computer_board):
            print("Error: Could not place computer 2 ships.")
            return
        
        print("Ships placed successfully!")
        
        # Ask for simulation speed
        print("\nSimulation Speed:")
        print("1. Fast (no pauses)")
        print("2. Normal (brief pauses)")
        print("3. Slow (longer pauses)")
        
        try:
            speed_choice = input("Select speed (1-3): ").strip()
            if speed_choice == "1":
                pause_time = 0
            elif speed_choice == "2":
                pause_time = 0.5
            elif speed_choice == "3":
                pause_time = 1.0
            else:
                pause_time = 0.5  # Default to normal
        except (EOFError, KeyboardInterrupt):
            print("\nSimulation cancelled.")
            return
        
        try:
            input("Press Enter to start the simulation...")
        except (EOFError, KeyboardInterrupt):
            print("\nSimulation cancelled.")
            return
        
        turn = 0
        max_turns = 100  # Prevent infinite loops
        
        while turn < max_turns:
            turn += 1
            print(f"\n{'='*80}")
            print(f"🚢 TURN {turn} 🚢")
            print(f"{'='*80}")
            
            # Show initial state for this turn
            print("CURRENT GAME STATE:")
            self.display_game_state()
            
            # Computer 1's turn
            print(f"\n🤖 COMPUTER 1'S TURN")
            print("-" * 40)
            row, col = self.get_computer_shot()
            hit, ship = self.computer_board.receive_shot(row, col)
            print(f"Computer 1 shoots at {chr(65 + col)}{row}: ", end="")
            
            if hit:
                print(f"💥 Hit! {ship.name}")
                if ship.is_sunk():
                    print(f"🚢 Computer 1 sunk the {ship.name}!")
            else:
                print("💨 Miss!")
            
            # Show board after Computer 1's shot
            print(f"\n{'='*80}")
            print("BOARD AFTER COMPUTER 1'S SHOT")
            print(f"{'='*80}")
            self.display_game_state()
            
            if self.computer_board.all_ships_sunk():
                print(f"\n🎉 COMPUTER 1 WINS in {turn} turns!")
                break
            
            # Computer 2's turn
            print(f"\n🤖 COMPUTER 2'S TURN")
            print("-" * 40)
            row, col = self.get_computer_shot()
            hit, ship = self.player_board.receive_shot(row, col)
            print(f"Computer 2 shoots at {chr(65 + col)}{row}: ", end="")
            
            if hit:
                print(f"💥 Hit! {ship.name}")
                if ship.is_sunk():
                    print(f"🚢 Computer 2 sunk the {ship.name}!")
            else:
                print("💨 Miss!")
            
            # Show board after Computer 2's shot
            print(f"\n{'='*80}")
            print("BOARD AFTER COMPUTER 2'S SHOT")
            print(f"{'='*80}")
            self.display_game_state()
            
            if self.player_board.all_ships_sunk():
                print(f"\n🎉 COMPUTER 2 WINS in {turn} turns!")
                break
            
            print(f"\n{'='*80}")
            print(f"TURN {turn} COMPLETE")
            print(f"{'='*80}")
            
            # Add pause based on speed setting
            if pause_time > 0:
                import time
                time.sleep(pause_time)
            else:
                try:
                    input("Press Enter to continue to next turn...")
                except (EOFError, KeyboardInterrupt):
                    print("\nSimulation cancelled.")
                    break
        
        if turn >= max_turns:
            print(f"\n⚠️  Game stopped after {max_turns} turns (preventing infinite loop)")
        
        print("\nSimulation complete!")
    
    def play_two_player(self):
        """Play two player mode (human vs human)"""
        print("Setting up two player game...")
        
        # Place ships for both players
        if not self.auto_place_ships(self.player_board):
            print("Error: Could not place player 1 ships.")
            return
        
        if not self.auto_place_ships(self.computer_board):
            print("Error: Could not place player 2 ships.")
            return
        
        print("Ships placed successfully!")
        try:
            input("Press Enter to start the game...")
        except (EOFError, KeyboardInterrupt):
            print("\nGame cancelled.")
            return
        
        turn = 0
        max_turns = 100  # Prevent infinite loops
        
        while turn < max_turns:
            turn += 1
            print(f"\n=== TURN {turn} ===")
            
            # Player 1's turn
            print("\n" + "=" * 80)
            print("PLAYER 1'S TURN")
            print("=" * 80)
            self.display_two_player_state(player_turn=1)
            
            print("Player 1's turn!")
            row, col = self.get_player_shot()
            hit, ship = self.computer_board.receive_shot(row, col)
            
            if hit:
                print(f"💥 Hit! Player 1 hit Player 2's {ship.name}!")
                if ship.is_sunk():
                    print(f"🚢 Player 1 sunk Player 2's {ship.name}!")
            else:
                print("💨 Miss!")
            
            # Show board after Player 1's shot
            print("\n" + "=" * 80)
            print("BOARD AFTER PLAYER 1'S SHOT")
            print("=" * 80)
            self.display_two_player_state(player_turn=1)
            
            if self.computer_board.all_ships_sunk():
                print(f"\n🎉 PLAYER 1 WINS in {turn} turns!")
                break
            
            try:
                input("\nPress Enter for Player 2's turn...")
            except (EOFError, KeyboardInterrupt):
                print("\nGame cancelled.")
                return
            
            # Player 2's turn
            print("\n" + "=" * 80)
            print("PLAYER 2'S TURN")
            print("=" * 80)
            self.display_two_player_state(player_turn=2)
            
            print("Player 2's turn!")
            row, col = self.get_player_shot()
            hit, ship = self.player_board.receive_shot(row, col)
            
            if hit:
                print(f"💥 Hit! Player 2 hit Player 1's {ship.name}!")
                if ship.is_sunk():
                    print(f"🚢 Player 2 sunk Player 1's {ship.name}!")
            else:
                print("💨 Miss!")
            
            # Show board after Player 2's shot
            print("\n" + "=" * 80)
            print("BOARD AFTER PLAYER 2'S SHOT")
            print("=" * 80)
            self.display_two_player_state(player_turn=2)
            
            if self.player_board.all_ships_sunk():
                print(f"\n🎉 PLAYER 2 WINS in {turn} turns!")
                break
            
            try:
                input("\nPress Enter to continue to next turn...")
            except (EOFError, KeyboardInterrupt):
                print("\nGame cancelled.")
                return
        
        if turn >= max_turns:
            print(f"\n⚠️  Game stopped after {max_turns} turns (preventing infinite loop)")
        
        print("\nGame complete!")
    
    def display_two_player_state(self, player_turn: int):
        """Display game state for two player mode"""
        os.system('clear' if os.name == 'posix' else 'cls')
        print("=" * 80)
        print(f"🚢 BATTLESHIP GAME - PLAYER {player_turn}'S TURN 🚢")
        print("=" * 80)
        print()
        
        if player_turn == 1:
            # Player 1's view: their ships vs their guesses on Player 2's board
            print("PLAYER 1'S FLEET BOARD                    PLAYER 1'S TARGET BOARD (Player 2's Ships)")
            print("=" * 60 + "    " + "=" * 60)
            
            player_lines = self._get_board_lines(self.player_board, show_ships=True)
            target_lines = self._get_guess_board_lines(self.computer_board)
            
            for i in range(len(player_lines)):
                print(f"{player_lines[i]:<60}    {target_lines[i]}")
            
            print()
            print("-" * 80)
            print("PLAYER 1'S SHIPS STATUS:")
            for ship in self.player_board.ships:
                if ship.is_sunk():
                    status = "💀 SUNK"
                else:
                    hits = len(ship.hits)
                    status = f"💥 {hits}/{ship.size} hits"
                
                ship_symbols = {
                    'Carrier': '🚢',
                    'Battleship': '🛥️ ',
                    'Cruiser': '🚤',
                    'Submarine': '🚤',
                    'Destroyer': '⛵'
                }
                ship_icon = ship_symbols.get(ship.name, '🚢')
                print(f"  {ship_icon} {ship.name}: {status}")
        
        else:
            # Player 2's view: their ships vs their guesses on Player 1's board
            print("PLAYER 2'S FLEET BOARD                    PLAYER 2'S TARGET BOARD (Player 1's Ships)")
            print("=" * 60 + "    " + "=" * 60)
            
            player_lines = self._get_board_lines(self.computer_board, show_ships=True)
            target_lines = self._get_guess_board_lines(self.player_board)
            
            for i in range(len(player_lines)):
                print(f"{player_lines[i]:<60}    {target_lines[i]}")
            
            print()
            print("-" * 80)
            print("PLAYER 2'S SHIPS STATUS:")
            for ship in self.computer_board.ships:
                if ship.is_sunk():
                    status = "💀 SUNK"
                else:
                    hits = len(ship.hits)
                    status = f"💥 {hits}/{ship.size} hits"
                
                ship_symbols = {
                    'Carrier': '🚢',
                    'Battleship': '🛥️ ',
                    'Cruiser': '🚤',
                    'Submarine': '🚤',
                    'Destroyer': '⛵'
                }
                ship_icon = ship_symbols.get(ship.name, '🚢')
                print(f"  {ship_icon} {ship.name}: {status}")
        
        print()
        print("LEGEND:")
        print("  🚢🛥️🚤⛵ = Your ships    💥 = Hit    💨 = Miss    🌊 = Water    ❓ = Unknown")
        print()
    
    def run(self):
        """Main game loop"""
        print("Welcome to Battleship!")
        print()
        print("Game Modes:")
        print("0. Computer vs Computer (Watch AI battle)")
        print("1. Single Player (You vs Computer)")
        print("2. Two Player (Human vs Human)")
        print()
        
        while True:
            try:
                choice = input("Select game mode (0, 1, or 2): ").strip()
                if choice == "0":
                    self.play_computer_vs_computer()
                    break
                elif choice == "1":
                    self.play_single_player()
                    break
                elif choice == "2":
                    self.play_two_player()
                    break
                else:
                    print("Invalid choice. Please enter 0, 1, or 2.")
            except (EOFError, KeyboardInterrupt):
                print("\nGame cancelled.")
                break

if __name__ == "__main__":
    game = BattleshipGame()
    game.run() 