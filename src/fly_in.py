import arcade
from visualizer import MenuView


def main() -> None:
    try:
        window = arcade.Window(1200, 800, "Fly In - Visualiseur")
        menu_depart = MenuView()
        window.show_view(menu_depart)
        arcade.run()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
