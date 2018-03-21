class Entity:
    def __init__(self, *args, **kwargs):
        self.__HP = HP
        self.name = name
        self.__isAlive = bool()
    @property
    def HP(self):
        return self.__HP
    @property
    def isAlive(self):
        return self.HP > 0
    @HP.setter
    def HP(self, value):
        if value < 0:
            self.__HP = 0
     #tratar de implementar mecanismos de defensa en esta función
        
