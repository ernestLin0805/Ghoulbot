import discord
from discord.ext import commands
import asyncio
import os
import random
import MAFIA
from MAFIA import gvar

class prepare:
    def __init__(self, bot, partyL):
        gvar.glob(bot, partyL)
        self.bot = bot

    def setMafia(self):
        mafia = self.setRole()
        return mafia
    def setDoctor(self):
        doctor = self.setRole()
        return doctor

    def setDet(self):
        det = self.setRole()
        return det

    def setPolitician(self):
        poli = self.setRole()
        return poli

    def setRole(self):
        userID = random.choice(gvar.gameListID)
        gvar.gameListID.remove(userID)
        return self.bot.get_member(userID)   
        
