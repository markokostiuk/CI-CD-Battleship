from UI import BattleshipGame

# Create an instance of the BattleshipGame class
game = BattleshipGame()

# Main game loop
while True:
    game.handle_events()
    game.update_screen()
