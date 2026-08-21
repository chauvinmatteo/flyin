import arcade
from visualizer import MapSelectionView


def main() -> None:
    window = arcade.Window(1200, 800, "Fly In - Visualiseur")
    menu_depart = MapSelectionView()
    window.show_view(menu_depart)
    arcade.run()


if __name__ == "__main__":
    main()
