import pygame
import sys

class GameState:
    def __init__(self):
        self.score = 0
        self.guessed_word = ''
        self.word_to_guess = ''
        self.current_index = 0
        self.clicked_letters = []
        self.available_buttons = list(range(1, 31))
        
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

    def remove_button(self, number):
        """Remove the clicked number from available buttons."""
        if number in self.available_buttons:
            self.available_buttons.remove(number)
            self.clicked_letters.append(str(number))

    def load_current_word(self):
        #Load the current word and image based on current_index
        current_data = self.game_data[self.current_index]
        self.word_to_guess = current_data['word']
        return current_data

    def next_state(self):
        #Move to the next word and image
        if self.current_index < len(self.game_data) - 1:
            self.current_index += 1
        else:
            #Optionally restart or end the game when the list is exhausted
            self.current_index = 0

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
        current_data = self.game_data.load_current_word()
        question_image = pygame.image.load(current_data['image'])
        resized_image = pygame.transform.scale(question_image, (600, 450))
        self.screen.blit(resized_image, (400, 100))
        self.home_button.draw(self.screen)


# Start the game
if __name__ == "__main__":
    game = Game()
    game.run()
