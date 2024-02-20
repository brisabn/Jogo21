import arcade
from game_views import InstructionView, SCREEN_HEIGHT, SCREEN_WIDTH

SCREEN_TITLE = "Jogo"

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = InstructionView()
    window.show_view(start_view)
    arcade.run()

if __name__ == "__main__":
    main()