from pygame.sprite import Sprite

from dino_runner.utils.constants import SCREEN_WIDTH

class Obstacle(Sprite):
    # Mudou:
    #   O posicionamento para se adequar a tela
    #   Design do Projeto em si 
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y =600

    def update(self, game_speed, obstacles):
        self.rect.x -=  game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()
        
    def draw(self, screen):
        screen.blit(self.image[self.type], (self.rect.x, self.rect.y))