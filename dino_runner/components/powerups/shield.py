from dino_runner.utils.constants import SHIELD, SHIELD_TYPE, SHIELD_SOUND
from dino_runner.components.powerups.power_up import PowerUp


class Shield(PowerUp):
    def __init__(self):
        self.image = SHIELD
        self.type = SHIELD_TYPE
        self.sound = SHIELD_SOUND
        super().__init__(self.image, self.type)