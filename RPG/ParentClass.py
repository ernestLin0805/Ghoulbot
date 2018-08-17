import os

class RPGClass:

    def __init__(self, name, attack, health, speed):
        self.name = name
        self.attack = attack
        self.health = health
        self.speed = speed
        self.picturePath = os.getcwd + "/LinkCharacters/" + name + ".png"

    def GetHealth(self):
        return self.health
