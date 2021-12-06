

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