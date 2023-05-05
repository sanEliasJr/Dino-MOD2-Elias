from dino_runner.utils.constants import HAMMER, HAMMER_TYPE, HAMMER_SOUND

from dino_runner.components.powerups.power_up import PowerUp


#Criação da Classe Hammer(Martelo)
#Parecida com a classe Shield
class Hammer(PowerUp):

    def __init__(self):
        self.image = HAMMER
        self.type = HAMMER_TYPE
        self.sound = HAMMER_SOUND
        super().__init__(self.image, self.type)