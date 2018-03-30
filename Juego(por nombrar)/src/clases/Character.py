class Character:
    def __init__(self, sprite, HP, melee, ranged, cooldown):
        self.sprite = sprite
        self.HP = HP #__HP?
        self.melee = melee
        self.ranged = ranged
        self.cooldown = 40 #frames ¿Acá o en otro lado? 
        self.frame_wait = 0

    def melee(self):
        #Llama a melee animation en self.sprite
        #Daño
