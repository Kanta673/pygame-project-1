import pygame
import sys

# GameState class to manage the game's data and logic
class GameState:
    def __init__(self):
        self.score = 0
        self.guessed_word = ''
        self.word_to_guess = ''
        self.current_index = 0
        self.clicked_letters = []
        self.available_buttons = list(range(1, 31))
        
        # List of words and images for guessing
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

    def load_current_word(self):
        """Load the current word and image based on current_index"""
        current_data = self.game_data[self.current_index]
        self.word_to_guess = current_data['word']
        self.guessed_word = ['_'] * len(self.word_to_guess)
        return current_data

    def update_word(self, letter):
        """Updates the guessed word with the correct letter"""
        if letter in self.word_to_guess:
            for i, char in enumerate(self.word_to_guess):
                if char == letter:
                    self.guessed_word[i] = letter
        self.clicked_letters.append(letter)

    def is_word_complete(self):
        return '_' not in self.guessed_word

    def next_state(self):
        """Move to the next word and image"""
        if self.current_index < len(self.game_data) - 1:
            self.current_index += 1
        else:
            self.current_index = 0


# Button class to represent interactive buttons
class Button:
    def __init__(self, image_path, x, y):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)


# Main Game class to handle game setup and loop
class Game:
    def __init__(self):
        pygame.init()
        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT = 720
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("เกมทายคำ")

        self.bg_img = pygame.image.load("bg picture.png")

        # Buttons for different states
        self.play_button = Button("play button.png", 250, 500)
        self.hint_button = Button("hint button.png", 600, 500)
        self.home_button = Button("home button.png", 950, 500)

        # Letter buttons for guessing (representative example; you'll need images for each letter)
        self.letter_buttons = self.create_letter_buttons()

        # State variables
        self.running = True
        self.game_state = 'main'  # Can be 'main' or 'question'
        self.game_data = GameState()
        self.current_word_data = None

    def create_letter_buttons(self):
        buttons = []
        alphabets = ['ไ', 'โ', 'แ', 'เ', 'า', 'อ', 'ส์', 'ส', 'ว', 'ลิ', 'ล', 'ร์', 'ร', 'ม', 'ฟ์', 'ฟ', 'พ', 'ป', 'บ', 'น์', 'น', 'ธ', 'ท็', 'ต์', 'ด', 'ซ', 'ชั่', 'ช', 'ค', 'ก์']
        
        button_x, button_y = 100, 600  # Starting position for letter buttons
        for i, letter in enumerate(alphabets):
            # Load button image assuming each letter has a corresponding image
            image_path = f"{letter}.png"
            button = Button(image_path, button_x + (i % 10) * 60, button_y + (i // 10) * 60)
            buttons.append((button, letter))
        return buttons

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_state == 'main':
                    if self.play_button.is_clicked(event):
                        self.game_state = 'question'  # Switch to question page
                        self.current_word_data = self.game_data.load_current_word()  # Load new word
                    elif self.hint_button.is_clicked(event):
                        print("Hint button clicked!")
                elif self.game_state == 'question':
                    if self.home_button.is_clicked(event):
                        self.game_state = 'main'  # Return to main menu
                    else:
                        # Handle letter button clicks during the game
                        for button, letter in self.letter_buttons:
                            if button.is_clicked(event) and letter not in self.game_data.clicked_letters:
                                self.game_data.update_word(letter)
                                if self.game_data.is_word_complete():
                                    print("Word completed!")
                                    self.game_data.next_state()  # Move to the next word
                                    self.current_word_data = self.game_data.load_current_word()

    def draw(self):
        self.screen.blit(self.bg_img, (0, 0))
        if self.game_state == 'main':
            self.play_button.draw(self.screen)
            self.hint_button.draw(self.screen)
        elif self.game_state == 'question':
            self.draw_question_page()

    def draw_question_page(self):
        # Draw the question image and guessed word
        question_image = pygame.image.load(self.current_word_data['image'])
        self.screen.blit(question_image, (400, 100))
        
        # Draw the word with guessed letters and underscores
        font = pygame.font.Font(None, 74)
        guessed_text = font.render(' '.join(self.game_data.guessed_word), True, (0, 0, 0))
        self.screen.blit(guessed_text, (400, 300))

        # Draw letter buttons
        for button, _ in self.letter_buttons:
            button.draw(self.screen)
        self.home_button.draw(self.screen)


# Start the game
if __name__ == "__main__":
    game = Game()
    game.run()
