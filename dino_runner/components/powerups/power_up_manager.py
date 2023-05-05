import random
import pygame
from pygame import mixer

from dino_runner.components.powerups import Shield , Hammer

class PowerUpManager:
    def __init__(self):
        self.power_ups = []
        self.when_appears = 0 
    
    # Mudou:
    #   Acrescentou o Hammer (Martelo)
    #   Logica de geração do martelo  
    def generate_power_up(self, score):

        if len(self.power_ups) == 0 and self.when_appears == score:
            self.when_appears += random.randint(200, 300)
            if random.randint(0, 1) == 0:
                self.power_ups.append(Hammer()) 
            else:
                self.power_ups.append(Shield())
    
    # Mudou:
    #   Logica de escolha de som de acordo com o objeto selecionado
    #   A responsabilidade de com fica por parte do proprio objeto ou seja se tornou um atributo 
    def update(self, score, game_speed, player):
            self.generate_power_up(score)
            for power_up in self.power_ups:
                power_up.update(game_speed, self.power_ups)
                if player.dino_rect.colliderect(power_up.rect): 
                    efects = mixer.Sound(power_up.sound) 
                    efects.play()
                    power_up.start_time = pygame.time.get_ticks()
                    player.shield = True
                    player.has_power_up = True
                    player.type = power_up.type
                    player.power_up_time = power_up.start_time + (power_up.duration * 1000)
                    self.power_ups.remove(power_up)
    
    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)
            
    def reset_power_ups(self):
         self.power_ups = []
         self.when_appears = random.randint(200, 300)