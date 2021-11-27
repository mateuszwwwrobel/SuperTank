from kivy.config import Config

Config.set('graphics', 'width', '1300')
Config.set('graphics', 'height', '1300')

from kivy.app import App
from kivy.graphics import Color, Rectangle, Point, Quad, Line
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ObjectProperty, Clock
from kivy.core.window import Window

from levels import level_1


class MainWidget(RelativeLayout):
    menu_widget = ObjectProperty()

    menu_title = "S U P E R    T A N K"
    menu_start_button = "START"
    menu_settings_button = "SETTINGS"
    menu_quit_button = "QUIT"

    map = None
    tank = None
    barrel = None
    hero_coordinates = [(0, 0), (0, 0), (0, 0), (0, 0)]
    last_move = 'up'
    map_borders = [(0, 0), (0, 0)]  # [(left, right), (bottom, top)]
    wall_collision = None
    map_initialized = False

    BULLETS_SPEED = 10
    bullets_list = []
    init_shot = False

    SPEED = 5
    current_speed_x = 0
    current_speed_y = 0
    current_offset_y = 0
    current_offset_x = 0

    start_game_state = False

    walls = []

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.init_tank()
        self.init_game_field()

        self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
        self._keyboard.bind(on_key_down=self.on_keyboard_down)
        self._keyboard.bind(on_key_up=self.on_keyboard_up)

        Clock.schedule_interval(self.update, 1 / 60)

    def init_game_field(self):
        with self.canvas:
            Color(1, 1, 1)
            self.map = Rectangle()

    def update_game_field(self):
        x_coord_1 = int(.05 * self.width)
        y_coord_1 = int(.05 * self.height)
        x_coord_2 = int(.9 * self.width)
        y_coord_2 = int(.8 * self.height)
        if self.start_game_state:
            self.map.size = [x_coord_2, y_coord_2]
            self.map.pos = [x_coord_1, y_coord_1]

    def init_map(self):
        level_schema = level_1
        start_point_x = int(self.width * .05)
        start_point_y = int(self.height * .85)
        row_counter = 0
        x_interval = (self.map_borders[0][1] - self.map_borders[0][0]) / 40
        y_interval = int((self.height * .8) / 40)

        x3, y3 = start_point_x, start_point_y - y_interval
        x4, y4 = start_point_x, start_point_y

        for index, lf in enumerate(level_schema):
            if index % 40 == 0:
                row_counter += 1
                x1, y1 = start_point_x, start_point_y - (row_counter - 1) * y_interval
                x2, y2 = start_point_x, start_point_y - row_counter * y_interval
                x3, y3 = start_point_x + x_interval, start_point_y - row_counter * y_interval
                x4, y4 = start_point_x + x_interval, start_point_y - (row_counter - 1) * y_interval
            else:
                x1, y1 = x4, y4
                x2, y2 = x3, y3
                x3, y3 = x3 + x_interval, y3
                x4, y4 = x4 + x_interval, y4

            if lf == ['X']:
                with self.canvas:
                    Color(.7, .4, .2)
                    field = Quad(points=[x1, y1, x2, y2, x3, y3, x4, y4])
                    self.walls.append(field)

    def init_tank(self):
        with self.canvas.after:
            Color(0, 0, 0)
            self.tank = Quad(points=[0, 0, 0, 0, 0, 0, 0, 0])
            self.barrel = Line(points=[0, 0, 0, 0], width=2)

    def update_tank(self):
        if self.start_game_state:
            center_x = self.width / 2 + self.current_offset_x
            base_y = (self.height / 2) - 10 + self.current_offset_y

            self.hero_coordinates[0] = (center_x - 20, base_y)
            self.hero_coordinates[1] = (center_x - 20, 40 + base_y)
            self.hero_coordinates[2] = (center_x + 20, 40 + base_y)
            self.hero_coordinates[3] = (center_x + 20, base_y)

            x1, y1 = self.hero_coordinates[0]
            x2, y2 = self.hero_coordinates[1]
            x3, y3 = self.hero_coordinates[2]
            x4, y4 = self.hero_coordinates[3]

            self.tank.points = [x1, y1, x2, y2, x3, y3, x4, y4]

    def check_collision_with_borders_x(self):
        hero_left_edge = self.hero_coordinates[0][0]
        hero_right_edge = self.hero_coordinates[2][0]

        if hero_left_edge <= self.map_borders[0][0]:
            self.wall_collision = 'left'
            if self.wall_collision == 'right':
                return False
            else:
                return True
        if hero_right_edge >= self.map_borders[0][1]:
            self.wall_collision = 'right'
            if self.wall_collision == 'left':
                return False
            else:
                return True
        return False

    def check_collision_with_borders_y(self):
        hero_bottom_edge = self.hero_coordinates[1][1] + 20
        hero_top_edge = self.hero_coordinates[0][1] - 20

        if hero_top_edge > self.map_borders[1][1]:
            self.wall_collision = 'top'
            if self.wall_collision == 'bottom':
                return False
            else:
                return True
        if hero_bottom_edge < self.map_borders[1][0]:
            self.wall_collision = 'bottom'
            if self.wall_collision == 'top':
                return False
            else:
                return True
        return False

    def on_start_button_press(self):
        self.menu_widget.opacity = 0
        self.start_game_state = True

    def on_settings_button_press(self):
        print('settings')

    def update_barrel_direction(self):
        x, y = self.hero_coordinates[0]
        if self.last_move == 'up':
            self.barrel.points = [x + 20, y + 10, x + 20, y + 60]
        elif self.last_move == 'down':
            self.barrel.points = [x + 20, y, x + 20, y - 20]
        elif self.last_move == 'left':
            self.barrel.points = [x + 10, y + 20, x - 20, y + 20]
        elif self.last_move == 'right':
            self.barrel.points = [x + 30, y + 20, x + 60, y + 20]

    def update(self, dt):
        self.get_map_borders()
        self.update_game_field()
        self.update_tank()
        self.update_barrel_direction()
        if self.init_shot:
            self.init_new_bullet()
            self.init_shot = False
        self.update_bullets()

        if self.start_game_state:
            if not self.map_initialized:
                self.init_map()
                self.map_initialized = True

            if not self.check_collision_with_borders_x():
                self.current_offset_x += self.current_speed_x
            else:
                if self.wall_collision == 'right':
                    self.current_offset_x -= 1
                if self.wall_collision == 'left':
                    self.current_offset_x += 1

            if not self.check_collision_with_borders_y():
                self.current_offset_y += self.current_speed_y
            else:
                if self.wall_collision == 'top':
                    self.current_offset_y -= 1
                if self.wall_collision == 'bottom':
                    self.current_offset_y += 1

    def get_map_borders(self):
        left_border = int(.05 * self.width)
        right_border = int(.95 * self.width)
        bottom_border = int(.1 * self.height)
        top_border = int(.8 * self.height)

        self.map_borders[0] = (left_border, right_border)
        self.map_borders[1] = (bottom_border, top_border)

    def update_bullets(self) -> None:
        for bullet, direction in self.bullets_list:
            x, y = bullet.points

            if direction == 'up':
                y += self.BULLETS_SPEED
                if y > self.height:
                    self.bullets_list.remove((bullet, direction))
                    continue
            elif direction == 'down':
                y -= self.BULLETS_SPEED
                if y < 0:
                    self.bullets_list.remove((bullet, direction))
                    continue
            elif direction == 'left':
                x -= self.BULLETS_SPEED
                if x < 0:
                    self.bullets_list.remove((bullet, direction))
                    continue
            elif direction == 'right':
                x += self.BULLETS_SPEED
                if x > self.width:
                    self.bullets_list.remove((bullet, direction))
                    continue

            bullet.points = [x, y]

    def get_bullet_start_point(self) -> (int, int):
        x, y = self.hero_coordinates[0]
        if self.last_move == 'up':
            return x + 20, y + 40
        elif self.last_move == 'down':
            return x + 20, y
        elif self.last_move == 'left':
            return x, y + 20
        elif self.last_move == 'right':
            return x + 40, y + 20

    def shot(self):
        with self.canvas:
            Color(0, 0, 0)
            x1, y1 = self.get_bullet_start_point()
            bullet = Point(points=(x1, y1))
            return bullet

    def init_new_bullet(self):
        bullet = self.shot()
        last_move = self.last_move
        self.bullets_list.append((bullet, last_move))

    def on_keyboard_down(self, keyboard, keycode, text, modifiers) -> bool:
        if keycode[1] == 'spacebar':
            self.init_shot = True

        elif keycode[1] == 'left':
            self.last_move = 'left'
            self.current_speed_x = -self.SPEED

        elif keycode[1] == 'right':
            self.last_move = 'right'
            self.current_speed_x = self.SPEED

        elif keycode[1] == 'up':
            self.last_move = 'up'
            self.current_speed_y = self.SPEED

        elif keycode[1] == 'down':
            self.last_move = 'down'
            self.current_speed_y = -self.SPEED
        return True

    def keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self.on_keyboard_down)
        self._keyboard.unbind(on_key_up=self.on_keyboard_up)
        self._keyboard = None

    def on_keyboard_up(self, keyboard, keycode) -> bool:
        self.current_speed_x = 0
        self.current_speed_y = 0
        return True


class MenuWidget(RelativeLayout):
    def on_touch_down(self, touch):
        if self.opacity == 0:
            return False
        return super(RelativeLayout, self).on_touch_down(touch)


class SuperTank(App):
    pass


if __name__ == '__main__':
    SuperTank().run()

# TODO: do not allow window size change when game in progress
# TODO: bullets stay near the edge of the window? Does it affect performance or something? Investigate.
# TODO: Add Enemies? They want to shot hero.
# TODO: Add Map? Randomly generated map? Levele dodawać predefiniowane?
# TODO: Allow shot when moving ? new variable? which switch very fast?
# TODO: Problem z mapa.
