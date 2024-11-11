import pygame
import sys

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Gamestate:
    def __init__(self):
        self.game_data = [
            {"image": "q1.png", "word": "ไพธอน"},
            {"image": "q2.png", "word": "แอปพลิเคชั่น"},
            {"image": "q3.png", "word": "เมาส์"},
            {"image": "q4.png", "word": "บราวเซอร์"},
            {"image": "q5.png", "word": "เดสก์ท็อป"},
            {"image": "q6.png", "word": "ไซเบอร์"},
            {"image": "q7.png", "word": "ไมโครซอฟต์"},
            {"image": "q8.png", "word": "ออนไลน์"},
            {"image": "q9.png", "word": "แฟลชไดรฟ์"}
        ]

        self.word_list = []
        for i in self.game_data:
            word = i.get(i[1])
            self.word_list.append(word)
            
        self.word_to_guess = ''
        self.current_index = 0
        self.clicked_letters = []
        self.available_buttons = list(range(1, 31))
        self.word_length = len(self.word_to_guess)
        self.guessed_word = ['_'] * self.word_length
        
    

    def create_button(self, image_files):
        buttons = []
        button_width = 60
        button_height = 60
        x_start = 50
        y_start = HEIGHT // 2 + 50

        alphabets = ['ไ','โ','แ','เ','า','อ','ส์','ส','ว','ลิ','ล','ร์','ร','ม','ฟ์','ฟ','พ','ป','บ','น์','น','ธ','ท็','ต์','ด','ซ','ชั่','ช','ค','ก์']
        for i, letter in enumerate(alphabets):
            image_path = f"{letter}.png"
            if image_path in image_files:
                image = pygame.image.load(image_path).convert_alpha()
            rect = pygame.Rect(x_start + (i % 13) * (button_width + 10), y_start + (i // 13) * (button_height + 10), button_width, button_height)
            buttons.append(Button(letter, rect, image))
        return buttons

    def update_word(self, letter):
        if letter in self.word_to_guess and letter not in self.guessed_letters:
            for i in range(self.word_length):
                if self.word_to_guess[i] == letter:
                    self.guessed_word[i] = letter
            self.guessed_letters.append(letter)
        else:
            self.guessed_letters.append(letter)
        if '_' not in self.guessed_word:
            self.game_over = True

    def draw_word(self):
        word_display = ' '.join(self.guessed_word)
        text_surface = big_font.render(word_display, True, BLACK)
        screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 4))

    def draw_buttons(self):
        for button in self.buttons:
            button.draw()

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
            pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button.rect.collidepoint(pos):
                    button.clicked = True  # Mark the button as clicked
                    self.update_word(button.letter)
                    self.buttons.remove(button)  # Remove the button from the list after clicking
                    break
        elif event.type == pygame.KEYDOWN and not self.game_over:
            if event.key >= pygame.K_a and event.key <= pygame.K_z:
                letter = chr(event.key).upper()
                if letter not in self.guessed_letters:
                    self.update_word(letter)

    def check_game_over(self):
        if self.game_over:
            game_over_text = big_font.render("You guessed the word!", True, BLACK)
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 40))


class Button:
    def __init__(self, letter, rect, image):
        self.letter = letter
        self.rect = rect
        self.image = image

    def draw(self):
        if self.clicked:
            # Draw the button with a gray color to show it was clicked
            self.image.fill(GRAY)
        screen.blit(self.image, self.rect)  # Draw the image on the button
        letter_text = font.render(self.letter, True, BLACK)
        # Draw the letter on top of the image (centered)
        screen.blit(letter_text, (self.rect.centerx - letter_text.get_width() // 2, self.rect.centery - letter_text.get_height() // 2))




class user_input:
    def __init__(self):
        self.guessed_word = ''
        
    def process(self, event):
        rows = 3
        cols = 10
        gap = 20
        size = 40
        boxes = []
        for row in range(rows):
            for col in range(cols):
                x = ((col * gap) + gap + (size * col))
                y = ((row * gap) + gap + (size * row))
                box = pygame.rect(x, y, size, size)
                boxes.append(box)
        letter_font = pygame.font.System('arial', 80)

        for letter in words:
            self.guessed_word += f'{letter}'
        
class Button:
    def __init__(self, image_path, x, y):
        # Load button image and create a rect for positioning and collision
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        # Draw the button image onto the screen
        screen.blit(self.image, self.rect.topleft)

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

class Game:
    def __init__(self):
        pygame.init()
        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT = 720
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH,self.SCREEN_HEIGHT))
        pygame.display.set_caption("เกมทายคาม")

        self.bg_img = pygame.image.load("bg picture.png")

        self.play_button = Button("play button.png", 550, 500)
        self.hint_button = Button("hint button.png", 600, 500)
        self.home_button = Button("home button.png", 950, 500)

        self.running = True
        self.game_state = "main"
        self.game_data = GameState()

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            pygame.display.flip()  
        
        pygame.quit()
        sys.exit()

    def handle_events(self):
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_state == 'main':
                    if self.play_button.clicked(event):
                        self.game_state = 'play'
                    elif self.hint_button.clicked(event):
                        pass
                elif self.game_state == 'play':
                    if self.home_button.clicked(event):
                        self.game_state = 'main'


    def draw(self):
        # Draw background and buttons
        self.screen.blit(self.bg_img, (0, 0))
        if self.game_state == 'main':
            self.play_button.draw(self.screen)
        elif self.game_state == 'play':
            self.draw_play_page()
            

    def draw_play_page(self):
        game = Gamestate(word_list, image_files)
        # Draw current guessed word
        game.draw_word()
            
        # Draw letter buttons
        game.draw_buttons()
        
        current_data = self.game_data.load_current_word()
        question_image = pygame.image.load(current_data['image'])
        resized_image = pygame.transform.scale(question_image, (600, 450))
        self.screen.blit(resized_image, (400, 100))
        self.home_button.draw(self.screen)


# Start the game
if __name__ == "__main__":
    game = Game()
    game.run()
