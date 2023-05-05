from pygame import mixer
from dino_runner.utils.constants import BIRD, EAGLE
from dino_runner.components.obstacles.obstacle import Obstacle


class Bird(Obstacle):
    
    # Mudou:
    #   O posicionamento para se adequar a tela
    #   Design do Projeto em si 
    def __init__(self):
        super().__init__(BIRD, 0)
        self.rect.y = 440
        self.step_index = 0

    def draw(self, screen):
        screen.blit(self.image[self.step_index // 5], self.rect)
        self.step_index += 1

        if self.step_index >= 10:
            self.step_index = 0

        eagle_sound = mixer.Sound(EAGLE)
        eagle_sound.play()
        eagle_sound.set_volume(0.1) #Diminui o volume da águia