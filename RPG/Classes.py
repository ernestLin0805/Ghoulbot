from ParentClass import RPGClass
import os

class Caveman(RPGClass):

    def __init__(self):
        RPGClass.__init__(self, "Caveman", 1, 100, 1)

class Archer(RPGClass):

    def __init__(self):
        RPGClass.__init__(self, "Archer", 70, 100, 1.5)
