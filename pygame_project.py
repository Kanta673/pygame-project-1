import pygame
import sys

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Screen dimensions
WIDTH, HEIGHT = 1280, 720

# Fonts
pygame.font.init()
big_font = pygame.font.Font(None, 60)
font = pygame.font.Font(None, 36)

# GameState Class
class Gamestate:
    def __init__(self):
        self.game_data = [
    {"image": "q1.png", "word": ["ไ", "พ", "ธ", "อ", "น"], "hint": "h1.png","answer":"a1.jpg"},
    {"image": "q2.png", "word": ["แ", "อ", "ป", "พ", "ลิ", "เ", "ค", "ชั่", "น"], "hint": "h2.png","answer":"a2.jpg"},
    {"image": "q3.png", "word": ["เ", "ม", "า", "ส์"], "hint": "h3.png","answer":"a3.jpg"},
    {"image": "q4.png", "word": ["บ", "ร", "า", "ว", "เ", "ซ", "อ", "ร์"], "hint": "h4.png","answer":"a4.jpg"},
    {"image": "q5.png", "word": ["เ", "ด", "ส", "ก์" , "ท็", "อ", "ป"], "hint": "h5.png","answer":"a5.jpg"},
    {"image": "q6.png", "word": ["ไ", "ซ", "เ", "บ", "อ", "ร์"], "hint": "h6.png","answer":"a6.jpg"},
    {"image": "q7.png", "word": ["ไ", "ม", "โ", "ค", "ร", "ซ", "อ", "ฟ", "ต์"], "hint": "h7.png","answer":"a7.jpg"},
    {"image": "q8.png", "word": ["อ", "อ", "น", "ไ", "ล", "น์"], "hint": "h8.png","answer":"a8.jpg"},
    {"image": "q9.png", "word": ["แ", "ฟ", "ล", "ช", "ไ", "ด", "ร", "ฟ์"], "hint": "h9.png","answer":"a9.jpg"}
]

        self.current_word_index = 0
        self.word_to_guess = self.game_data[self.current_word_index]["word"]  # Start with the first word
        self.word_length = len(self.word_to_guess)
        self.guessed_word = ['_'] * self.word_length
        self.clicked_letters = []
        self.show_answer = False  # New flag to control answer image display
        self.game_over = False
        self.letter_images = {}

         # Preload images
        self.preloaded_images = {entry["image"]: pygame.image.load(entry["image"]) for entry in self.game_data}
        self.preloaded_hints = {entry["hint"]: pygame.image.load(entry["hint"]) for entry in self.game_data}
        self.preloaded_answers = {entry["answer"]: pygame.image.load(entry["answer"]) for entry in self.game_data}

    def get_current_image(self):
        return self.preloaded_images[self.game_data[self.current_word_index]["image"]]

    def get_current_hint(self):
        return self.preloaded_hints[self.game_data[self.current_word_index]["hint"]]

    def update_word(self, letter):
        if letter in self.word_to_guess:
            for i in range(self.word_length):
                if self.word_to_guess[i] == letter:
                    self.guessed_word[i] = letter  # Replace underscore with the letter

            if letter not in self.letter_images:
                self.letter_images[letter] = pygame.image.load(f"{letter}.png")  # Load the image for the letter

        self.clicked_letters.append(letter)

        # Check if the word is completed
        if '_' not in self.guessed_word:
            self.show_answer = True  # Show answer image when word is completed

    def move_to_next_word(self):
        """Transition to the next word."""
        if self.current_word_index + 1 < len(self.game_data):
            self.current_word_index += 1
            self.word_to_guess = self.game_data[self.current_word_index]["word"]
            self.word_length = len(self.word_to_guess)
            self.guessed_word = ['_'] * self.word_length
            self.clicked_letters = []
            self.show_answer = False  # Reset for the next word
            self.letter_images = {}
        else:
            self.game_over = True  # All words have been guessed, game over

    def get_hint_image(self):
        """Returns the hint image path for the current word."""
        return self.game_data[self.current_word_index]["hint"]



    def draw_word(self, screen):
        x_offset = WIDTH // 2 - (self.word_length * 40) // 2  # Center the word on the screen
        for i, letter in enumerate(self.guessed_word):
            if letter != '_':
                letter_image = pygame.transform.scale(self.letter_images[letter], (40, 40))
                screen.blit(letter_image, (x_offset + i * 40, HEIGHT // 2))
            else:
                pygame.draw.rect(screen, BLACK, (x_offset + i * 40, HEIGHT // 2, 50, 50), 2)


# Button Class
class Button:
    def __init__(self, letter, x, y, image, width=50, height=50):  # Added width and height parameters
        self.letter = letter
        self.image = pygame.transform.scale(image, (width, height))  # Resize the image to given width and height
        self.rect = pygame.Rect(x, y, width, height)  # Adjust the button rect to the new image size
        self.clicked = False
        self.mouse_pressed = False  # Track the mouse pressed state

    def draw(self, screen):
        if self.clicked:
            # Change the button's appearance to show it was clicked (e.g., gray it out)
            image_with_overlay = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
            image_with_overlay.fill(GRAY)
            image_with_overlay.blit(self.image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(image_with_overlay, self.rect.topleft)
        else:
            screen.blit(self.image, self.rect.topleft)

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            return True
        return False

    def on_mouse_down(self):
        self.mouse_pressed = True
        self.clicked = True

    def on_mouse_up(self):
        self.mouse_pressed = False
        self.clicked = False


# Game Class
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("เกมทายคำ")
        self.bg_img = pygame.image.load("Home.png")
        self.state_img = pygame.image.load("bg picture.png")
        self.running = True
        self.game_state = "home"  # Start in the home screen
        self.gamestate = Gamestate()

        # Create buttons for home and game
        self.play_button = Button("Play", 550, 300, pygame.image.load("play button.png"))
        self.home_button = Button("Home", 50, 50, pygame.image.load("home button.png"))
        self.hint_button = Button("Hint", 1100, 50, pygame.image.load("hint button.png"), width=150, height=100)
        self.letter_buttons = self.create_buttons()
        self.show_hint = False

        #Create game over page
        self.game_over_img = pygame.image.load("game_over.jpg")  # Replace with your image path
        self.game_over_img_rect = self.game_over_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Center it

    def create_buttons(self):
        buttons = []
        alphabets = ['ไ', 'โ', 'แ', 'เ', 'า', 'อ', 'ส์', 'ส', 'ว', 'ลิ', 'ล', 'ร์', 'ร', 'ม', 'ฟ์', 'ฟ', 'พ', 'ป', 'บ', 'น์', 'น', 'ธ', 'ท็', 'ต์', 'ด', 'ซ', 'ชั่', 'ช', 'ค', 'ก์']
        button_x, button_y = 50, HEIGHT // 2 + 100
        button_width, button_height = 50, 50
        gap = 20

        for i, letter in enumerate(alphabets):
            try:
                image = pygame.image.load(f"{letter}.png").convert_alpha()
            except FileNotFoundError:
                print(f"Missing image: {letter}.png")
                continue
            x = button_x + (i % 15) * (button_width+ 10 + gap)
            y = button_y + (i // 15) * (button_height + gap)
            buttons.append(Button(letter, x, y, image))

        # Add Play and Home Buttons separately since they should not have letter text
        play_button_image = pygame.image.load("play button.png")  # Example play button image
        home_button_image = pygame.image.load("home button.png")  # Example home button image

        # Scale the play and home buttons to a larger size (150x100)
        self.play_button = Button("Play", 550, 500, play_button_image, width=150, height=100)
        self.home_button = Button("Home", 50, 50, home_button_image, width=150, height=100)

        return buttons

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if self.game_state == "home":
                    if self.play_button.check_click(pos):
                        self.game_state = "play"  # Switch to the game screen
                elif self.game_state == "play":
                    if self.gamestate.show_answer:  # If showing answer image
                        answer_rect = self.gamestate.preloaded_answers[
                            self.gamestate.game_data[self.gamestate.current_word_index]["answer"]
                        ].get_rect(center=(WIDTH // 2, HEIGHT // 2))
                        if answer_rect.collidepoint(pos):  # Check if clicked on answer image
                            self.gamestate.move_to_next_word()
                    else:
                        if self.home_button.check_click(pos):
                            self.game_state = "home"
                        elif self.hint_button.check_click(pos):
                            self.show_hint = not self.show_hint
                        else:
                            for button in self.letter_buttons:
                                if button.check_click(pos):
                                    button.on_mouse_down()
                                    if button.letter not in self.gamestate.clicked_letters:
                                        self.gamestate.update_word(button.letter)
                                        self.show_hint = False
            elif event.type == pygame.MOUSEBUTTONUP:
                for button in self.letter_buttons:
                    button.on_mouse_up()

    def draw(self):
        self.screen.blit(self.bg_img, (0, 0))  # Draw background

        if self.game_state == "home":
            self.draw_home_page()  # Draw the home page
        elif self.game_state == "play":
            self.draw_play_page()  # Draw the gameplay page

        pygame.display.flip()

    def draw_home_page(self):
        # Draw "Home" page (main menu)
        self.play_button.draw(self.screen)

    def draw_play_page(self):
        # Draw the gameplay page
        self.screen.blit(self.state_img, (0, 0))
        self.gamestate.draw_word(self.screen)
        self.home_button.draw(self.screen)
        self.hint_button.draw(self.screen)

        for button in self.letter_buttons:
            button.draw(self.screen)

        # Draw the image for the current word
        current_image = pygame.image.load(self.gamestate.game_data[self.gamestate.current_word_index]["image"])
        resized_image = pygame.transform.scale(current_image, (600, 450))
        self.screen.blit(resized_image, (WIDTH // 2 - 300, HEIGHT // 4 - 200))

        # Draw the hint image if show_hint is True
        if self.show_hint:
            hint_image = pygame.image.load(self.gamestate.game_data[self.gamestate.current_word_index]["hint"])
            resized_hint_image = pygame.transform.scale(hint_image, (300, 150))  # Adjust hint size as needed
            self.screen.blit(resized_hint_image, (WIDTH // 2 + 300, HEIGHT // 4 + 150))

        if self.gamestate.show_answer:  # Show answer image if flag is set
            answer_image = self.gamestate.preloaded_answers[
                self.gamestate.game_data[self.gamestate.current_word_index]["answer"]
            ]
            resized_answer_image = pygame.transform.scale(answer_image, (1280, 720))  # Resize as needed
            answer_rect = resized_answer_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(resized_answer_image, answer_rect.topleft)

        if self.gamestate.game_over:
            # Show a "Game Over" image
            self.screen.blit(self.game_over_img, self.game_over_img_rect.topleft)

    def draw_next_game_page(self):
        self.screen.fill(WHITE)  # Clear the screen

        def draw(self):
            self.screen.blit(self.bg_img, (0, 0))  # Draw background

            if self.game_state == "home":
                self.draw_home_page()
            elif self.game_state == "play":
                self.draw_play_page()
            elif self.game_state == "next_game":
                self.draw_next_game_page()

        pygame.display.flip()

# Run the game
game = Game()
while game.running:
    game.handle_events()
    game.draw()
