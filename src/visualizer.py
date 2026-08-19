import arcade
import arcade.gui
import os
from mapdata import Connection, Zone
from parsing import MapParser

screen_width = 1200
screen_height = 800
screen_title = "FLY_IN by mchauvin"


class MenuView(arcade.View):

    def __init__(self) -> None:
        super().__init__()
        self.titre = arcade.Text(
            text=screen_title,
            x=screen_width / 2,
            y=screen_height - 100,
            color=arcade.color.BLACK,
            font_size=40,
            anchor_x="center",
            anchor_y="center"
        )
        self.manager = arcade.gui.UIManager()
        self.v_box = arcade.gui.UIBoxLayout()

        start_button = arcade.gui.UIFlatButton(text="Start Game", width=200,
                                               height=50)
        self.v_box.add(start_button)
        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(child=self.v_box, anchor_x="center_x", anchor_y="center_y")
        self.manager.add(anchor)
        start_button.on_click = self.on_click_start

    def on_click_start(self, event) -> None:
        diff_view = DifficultyView()
        self.window.show_view(diff_view)

    def on_show_view(self) -> None:
        arcade.set_background_color(arcade.color.GRAY_BLUE)
        self.manager.enable()

    def on_hide_view(self) -> None:
        self.manager.disable()

    def on_draw(self) -> None:
        self.clear()
        self.titre.draw()
        self.manager.draw()


class DifficultyView(arcade.View):

    def __init__(self) -> None:
        super().__init__()
        self.selected_map = None
        self.titre = arcade.Text(
            text=screen_title,
            x=screen_width / 2,
            y=screen_height - 100,
            color=arcade.color.BLACK,
            font_size=40,
            anchor_x="center",
            anchor_y="center"
        )
        self.manager = arcade.gui.UIManager()
        self.v_box = arcade.gui.UIBoxLayout()

        for difficulty_name in os.listdir("./maps"):
            if difficulty_name == "README.md":
                continue
            map_button = arcade.gui.UIFlatButton(text=difficulty_name,
                                                 width=200, height=50)

            map_button.on_click = self.on_click_difficulty(difficulty_name)
            self.v_box.add(map_button)
        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(child=self.v_box, anchor_x="center_x", anchor_y="center_y")
        self.manager.add(anchor)

    def on_show_view(self) -> None:
        arcade.set_background_color(arcade.color.GRAY_BLUE)
        self.manager.enable()

    def on_hide_view(self) -> None:
        self.manager.disable()

    def on_draw(self) -> None:
        self.clear()
        self.titre.draw()
        self.manager.draw()

    def on_click_difficulty(self, difficulty) -> callable:
        def action(event) -> None:
            next_window = MapSelectionView(difficulty)
            self.window.show_view(next_window)
        return action


class MapSelectionView(arcade.View):

    def __init__(self, difficulty: str) -> None:
        super().__init__()
        self.selected_map = None
        self.titre = arcade.Text(
            text=screen_title,
            x=screen_width / 2,
            y=screen_height - 100,
            color=arcade.color.BLACK,
            font_size=40,
            anchor_x="center",
            anchor_y="center"
        )
        self.manager = arcade.gui.UIManager()
        self.v_box = arcade.gui.UIBoxLayout()
        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(child=self.v_box, anchor_x="center_x", anchor_y="center_y")
        self.manager.add(anchor)
        self.difficulty = difficulty

        for map_name in os.listdir(f"./maps/{difficulty}"):
            if map_name == "README.md":
                continue
            map_button = arcade.gui.UIFlatButton(text=map_name,
                                                 width=200, height=50)
            map_button.on_click = self.on_click_map(map_name)
            self.v_box.add(map_button)

    def on_show_view(self) -> None:
        arcade.set_background_color(arcade.color.GRAY_BLUE)
        self.manager.enable()

    def on_hide_view(self) -> None:
        self.manager.disable()

    def on_draw(self) -> None:
        self.clear()
        self.titre.draw()
        self.manager.draw()

    def on_click_map(self, map_name) -> None:
        def action(event) -> None:
            map = SimulationView(f"./maps/{self.difficulty}/{map_name}")
            self.window.show_view(map)
        return action


class SimulationView(arcade.View):

    def __init__(self, map_name: str) -> None:
        super().__init__()
        self.current_map: str = map_name
        self.turn = 0
        parser = MapParser()
        parser.parse(self.current_map)
        self.zones: dict[str, Zone] = parser.zones
        self.connections: list[Connection] = parser.connections
        xs: list[int] = [zone.x for zone in self.zones.values()]
        ys: list[int] = [zone.y for zone in self.zones.values()]

        self.min_x: int = min(xs)
        self.max_x: int = max(xs)
        self.min_y: int = min(ys)
        self.max_y: int = max(ys)

        map_width = self.max_x - self.min_x
        map_height = self.max_y - self.min_y
        if map_width == 0:
            map_width = 1
        if map_height == 0:
            map_height = 1

        x_scale = (screen_width - 200) / map_width
        y_scale = (screen_height - 200) / map_height
        self.scale = min(x_scale, y_scale)
        self.offset_x = ((screen_width - map_width * self.scale) / 2)
        self.offset_y = ((screen_height - map_height * self.scale) / 2)

    def on_draw(self) -> None:
        self.clear()
        arcade.set_background_color(arcade.color.WHITE)

        for connection in self.connections:
            zone_source = self.zones[connection.source]
            zone_destination = self.zones[connection.destination]
            arcade.draw_line(
                (zone_source.x - self.min_x) * self.scale + self.offset_x,
                (zone_source.y - self.min_y) * self.scale + self.offset_y,
                (zone_destination.x - self.min_x) * self.scale + self.offset_x,
                (zone_destination.y - self.min_y) * self.scale + self.offset_y,
                arcade.color.BLACK,
                2
            )
        for zone in self.zones.values():
            arcade.draw_circle_filled(
                (zone.x - self.min_x) * self.scale + self.offset_x,
                (zone.y - self.min_y) * self.scale + self.offset_y,
                10,
                arcade.color.BABY_BLUE
            )


class GameView(arcade.Window):

    def __init__(self, width, height, title) -> None:
        super().__init__(width, height, title)


window = GameView(screen_width, screen_height, "FLY_IN")
menu = MenuView()
window.show_view(menu)
arcade.run()
