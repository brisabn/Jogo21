import arcade

CARD_SCALE = 0.05

class Button:
    def __init__(self, center_x, center_y, width, height, texture_path):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.texture = arcade.load_texture(texture_path)
        self.is_pressed = False
        self.normal_scale = 1.0
        self.pressed_scale = 0.9

    def draw(self):
        if self.is_pressed:
            scale = self.pressed_scale
        else:
            scale = self.normal_scale
        arcade.draw_texture_rectangle(self.center_x, self.center_y, self.width * scale, self.height * scale, self.texture)

    def check_click(self, x, y): # considerando botão retangular...
        if (x > self.center_x - self.width / 2 and x < self.center_x + self.width / 2 and
                y > self.center_y - self.height / 2 and y < self.center_y + self.height / 2):
            return True
        return False

    def on_mouse_press(self, x, y):
        if self.check_click(x, y):
            self.is_pressed = True

    def on_mouse_release(self, x, y):
        self.is_pressed = False

        
class Card:
    def __init__(self, value, flip_finished=False, is_face_up=False):
        self.value = value
        self.front_image = arcade.load_texture(f"cards/card_{self.value}.png")
        self.back_image = arcade.load_texture("cards/card_back.png")
        self.width = self.front_image.width * CARD_SCALE
        self.height = self.front_image.height * CARD_SCALE
        self.center_x = 0
        self.center_y = 0
        self.flip_progress = 0
        self.flip_speed = 0.02
        self.is_face_up = is_face_up
        self.flip_finished = flip_finished

    def draw(self):
        image = self.front_image if self.is_face_up else self.back_image
        if self.flip_progress > 0.5:
            image = self.back_image if self.is_face_up else self.front_image
        arcade.draw_texture_rectangle(self.center_x, self.center_y, self.width, self.height, image)

    def update(self):
        if self.flip_progress <= 1.0:
            if self.flip_progress < 0.5:
                self.width -= self.flip_speed * self.front_image.width * 2 * CARD_SCALE
            else:
                self.width += self.flip_speed * self.front_image.width * 2 * CARD_SCALE
            self.flip_progress += self.flip_speed

    def flip(self):
        if self.flip_progress >= 1.0:
            self.is_face_up = not self.is_face_up
            self.flip_progress = 0

class Player:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def calculate_sum(self):
        total = 0
        for card in self.cards:
            total += card.value
        return total

class Dealer(Player):
    def __init__(self):
        super().__init__()
        self.hidden_card = None # não deu certo fazendo isso daqui

    def add_hidden_card(self, card):
        self.hidden_card = card

    def reveal_hidden_card(self):
        if self.hidden_card:
            self.hidden_card.flip()