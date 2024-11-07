import pygame
import sys

class Button:
    def __init__(self, image_path, x, y):
        # Load button image and create a rect for positioning and collision
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        # Draw the button image onto the screen
        screen.blit(self.image, self.rect.topleft)

class Game:
    def __init__(self):
        pygame.init()
        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT = 720
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH,self.SCREEN_HEIGHT))
        pygame.display.set_caption("เกมทายคาม")

        self.bg_img = pygame.image.load("bg picture.png")

        self.play_button = Button("play button.png", 250, 500)
        self.hint_button = Button("hint button.png", 600, 500)
        self.home_button = Button("home button.png", 950, 500)

        self.running = True

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

    def draw(self):
        # Draw background and buttons
        self.screen.blit(self.bg_img, (0, 0))
        self.play_button.draw(self.screen)
        self.hint_button.draw(self.screen)
        self.home_button.draw(self.screen)

# Start the game
if __name__ == "__main__":
    game = Game()
    game.run()
        