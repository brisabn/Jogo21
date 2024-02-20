import arcade
import random
from game_elements import Button, Card, Player, Dealer

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500

CARD_SCALE = 0.05
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 40

class InstructionView(arcade.View):
    def __init__(self):
        super().__init__()

        # Carrega as imagens dos botões
        self.start_button_image = arcade.load_texture("buttons/start_button.png")
        self.rules_button_image = arcade.load_texture("buttons/rules_button.png")

        # Obtém as dimensões das imagens originais
        button_width = self.start_button_image.width
        button_height = self.start_button_image.height

        # x, y, comprimento, altura
        self.start_button = Button(SCREEN_WIDTH / 3 + button_width/6, SCREEN_HEIGHT / 2 - 175 ,  button_width/2, button_height/2, "buttons/start_button.png")
        self.rules_button = Button(SCREEN_WIDTH / 2 + button_width/3.5, SCREEN_HEIGHT / 2 - 175,  button_width/2, button_height/2, "buttons/rules_button.png")
        self.background = None
        self.change_view_delay = 0.15  # delay before switching views
        self.change_to_game_view = False
        self.change_to_rules_view = False

    def on_show_view(self):
        self.background = arcade.load_texture("menu.png")

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.start_button.draw()
        self.rules_button.draw()

    def on_mouse_press(self, x, y, _button, _modifiers):
        if self.start_button.check_click(x, y):
            self.start_button.on_mouse_press(x, y)
            self.change_to_game_view = True
        elif self.rules_button.check_click(x, y):
            self.rules_button.on_mouse_press(x, y)
            self.change_to_rules_view = True

    def on_mouse_release(self, x, y, _button, _modifiers):
        self.start_button.on_mouse_release(x, y)
        self.rules_button.on_mouse_release(x, y)

    def on_update(self, delta_time):
        if self.change_to_game_view:
            self.change_view_delay -= delta_time
            if self.change_view_delay <= 0:
                game_view = GameView()
                game_view.setup()
                self.window.show_view(game_view)
        elif self.change_to_rules_view:
            self.change_view_delay -= delta_time
            if self.change_view_delay <= 0:
                rules_view = RulesView()
                self.window.show_view(rules_view)

class RulesView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show_view(self):
        """ This is run once when we switch to this view """
        self.window.background_color = arcade.csscolor.LIGHT_SKY_BLUE

    def on_draw(self):
        self.clear()
        arcade.draw_text("Game Rules", self.window.width / 2, self.window.height - 50,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("1. Objetivo: Alcançar um total de pontos próximo a 21 sem ultrapassá-lo.", self.window.width / 2, self.window.height - 150,
                         arcade.color.BLACK, font_size=20, anchor_x="center")
        arcade.draw_text("2. As cartas numéricas têm o valor correspondente ao número nelas impresso.", self.window.width / 2, self.window.height - 200,
                         arcade.color.BLACK, font_size=20, anchor_x="center")
        arcade.draw_text("3. As cartas 'J', 'Q' e 'K' valem 10 pontos.", self.window.width / 2, self.window.height - 250,
                         arcade.color.BLACK, font_size=20, anchor_x="center")
        arcade.draw_text("4. O ás ('A') pode valer 1 ou 11 pontos, dependendo do que for mais vantajoso.", self.window.width / 2, self.window.height - 300,
                         arcade.color.BLACK, font_size=20, anchor_x="center")
        arcade.draw_text("5. Clique em 'Start' para iniciar o jogo.", self.window.width / 2, self.window.height - 350,
                         arcade.color.BLACK, font_size=20, anchor_x="center")
        arcade.draw_text("Click to return", self.window.width / 2, 50,
                         arcade.color.BLACK, font_size=20, anchor_x="center")

    def on_mouse_press(self, x, y, _button, _modifiers):
        game_view = InstructionView()
        self.window.show_view(game_view)

class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        arcade.set_background_color(arcade.color.AMAZON)

        self.player = Player()
        self.dealer = Dealer()
        self.hit_button = None  # Botão "Hit Me"
        self.stand_button = None  # Botão "Stand"

        self.player_sum = 0
        self.dealer_sum = 0
        self.result_message = ""

        self.game_over = False
        self.stand_check = False
        
    def setup(self):
        # Criando sprites e listas de sprites aqui
        for i in range(2):
            player_card_value = random.randint(1, 11) if i == 0 else random.randint(1, 9)
            dealer_card_value = random.randint(1, 11) if i == 0 else random.randint(1, 9)
            player_card = Card(player_card_value, flip_finished=True, is_face_up=True)
            dealer_card = Card(dealer_card_value, flip_finished=True, is_face_up=(i != 0))
            self.player.add_card(player_card)
            self.dealer.add_card(dealer_card)
      
        # Posicionamento inicial das cartas
        self.position_cards()

        # Criações dos Botões
        self.hit_button = Button(SCREEN_WIDTH - BUTTON_WIDTH // 2 - 70, BUTTON_HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT, "buttons/hit_button.png")
        self.stand_button = Button(SCREEN_WIDTH - BUTTON_WIDTH // 2 - 70, BUTTON_HEIGHT // 2 + BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT, "buttons/stand_button.png")
    
    def position_cards(self):
        card_spacing = Card(1).width + CARD_SCALE*100
        player_card_start_x = SCREEN_WIDTH // 4 - (len(self.player.cards) * card_spacing) // 2
        dealer_card_start_x = SCREEN_WIDTH // 4 - (len(self.dealer.cards) * card_spacing) // 2
        for i, card in enumerate(self.player.cards):
            card.center_x = player_card_start_x + i * card_spacing
            card.center_y = SCREEN_HEIGHT // 4  # Ajuste para a posição inferior da tela

        for i, card in enumerate(self.dealer.cards):
            card.center_x = dealer_card_start_x + i * card_spacing
            card.center_y = SCREEN_HEIGHT * 3 // 4  # Ajuste para a posição superior da tela

    def calculate_and_display_sum(self):
        # Calcula e exibe a soma das cartas do jogador
        self.player_sum = self.player.calculate_sum()
        arcade.draw_text(f"Player Total: {self.player_sum}", 10, SCREEN_HEIGHT - 20, arcade.color.WHITE, 14)

        # Calcula e exibe a soma das cartas do dealer
        if self.stand_check:
            self.dealer_sum = self.dealer.calculate_sum()
            arcade.draw_text(f"Dealer Total: {self.dealer_sum}", 10, SCREEN_HEIGHT - 40, arcade.color.WHITE, 14)
        else:
            arcade.draw_text("Dealer Total: ?", 10, SCREEN_HEIGHT - 40, arcade.color.WHITE, 14)

    def update(self, delta_time):
        for card in self.player.cards:
            if not card.flip_finished:
                card.update()

        for card in self.dealer.cards:
            if not card.flip_finished:
                card.update()

    def on_draw(self):
        # Limpa a tela com a cor de fundo
        self.clear()

        # Desenha as cartas
        for card in self.player.cards:
            card.draw()
        for card in self.dealer.cards:
            card.draw()

        # Desenha os botões "Hit Me" e "Stand"
        self.hit_button.draw()
        self.stand_button.draw()

        # Calcula e exibe a soma das cartas do jogador e do dealer
        self.calculate_and_display_sum()

        # Exibe a mensagem de resultado do jogo
        arcade.draw_text(self.result_message, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, arcade.color.WHITE, 36, anchor_x="center", anchor_y="center")

    def on_mouse_press(self, x, y, button, modifiers):
        if not self.game_over:
            if self.hit_button.check_click(x, y):
                self.hit()

            elif self.stand_button.check_click(x, y):
                self.stand_check = True
                self.stand()
                self.game_over = True

    def hit(self):
        # Adiciona uma nova carta para o jogador
        value = random.randint(1, 9)
        new_card = Card(value, flip_finished=False, is_face_up=False)
        self.player.add_card(new_card)
        # Reposiciona a nova carta do jogador
        card_spacing = Card(1).width + CARD_SCALE*100
        new_card.center_x = self.player.cards[-2].center_x + card_spacing  # Coloca ao lado da última carta
        new_card.center_y = SCREEN_HEIGHT // 4  # Ajuste para a posição inferior da tela

        # Atualiza e exibe a soma das cartas do jogador e do dealer
        self.calculate_and_display_sum()

        if self.player_sum >= 21:
            self.finish_game()

    def finish_game(self):
        self.game_over = True

        if self.dealer_sum > 21 or self.player_sum == 21:
            self.result_message = "GANHOU"
        elif self.dealer_sum == self.player_sum:
            self.result_message = "EMPATOU"
        elif (self.dealer_sum > self.player_sum and self.dealer_sum < 21) or self.dealer_sum == 21 or self.player_sum > 21:
            self.result_message = "PERDEU"

        arcade.schedule(self.show_game_over_view, 1.8) 
        
    def show_game_over_view(self, delta_time: float):
        arcade.unschedule(self.show_game_over_view)  # Cancela o agendamento anterior
        view = GameOverView(self.result_message)  # Passa o resultado do jogo para a tela de GameOverView
        self.window.show_view(view)

    def deal_dealer_card(self, dt = None):
        arcade.unschedule(self.deal_dealer_card)
        self.calculate_and_display_sum()

        if self.dealer_sum < self.player_sum:
            value = random.randint(1, 9)
            new_card = Card(value, flip_finished=False, is_face_up=False)
            self.dealer.add_card(new_card)

            card_spacing = Card(1).width + CARD_SCALE * 100
            new_card.center_x = self.dealer.cards[-2].center_x + card_spacing
            new_card.center_y = SCREEN_HEIGHT * 3 // 4

            arcade.schedule(self.deal_dealer_card, 0.8) # Agenda a próxima exibição de carta do dealer
        else:
            self.finish_game()

    def stand(self):
        if not self.dealer.cards[0].is_face_up:
            self.dealer.cards[0].flip()
            self.dealer.cards[0].flip_finished = False
        
        self.dealer_sum = self.dealer.calculate_sum()
        if self.dealer_sum >= self.player_sum:
            self.finish_game()

        arcade.schedule(self.deal_dealer_card, 0.8)

class GameOverView(arcade.View):
    def __init__(self, result):
        super().__init__()
        self.result = result
        self.restart_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, BUTTON_WIDTH, BUTTON_HEIGHT, "buttons/stand_button.png")
        self.return_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 - BUTTON_HEIGHT * 2, BUTTON_WIDTH, BUTTON_HEIGHT, "buttons/hit_button.png")

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Game Over", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text(f"Você {self.result}!", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, arcade.color.WHITE, font_size=20, anchor_x="center")
        self.restart_button.draw()
        self.return_button.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.restart_button.check_click(x, y):
            # Cria uma nova instância de GameView e troca para ela
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)

        elif self.return_button.check_click(x, y):
            start_view = InstructionView()
            self.window.show_view(start_view)