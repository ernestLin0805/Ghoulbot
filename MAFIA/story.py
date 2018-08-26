import discord
from discord.ext import commands
import asyncio
import os
import random

class storyTime:

    badS = [
    "{} was playing league one day, when suddenly all the electricity went out, and {} was found dead in front of the computer later. The teammates were not happy with the afk and {} received a 14 day ban. Oof.", 
    "{} decided to go to Comic Con this year. However {} was stabbed by a Kirito cosplayer during the event, and no one could find {}'s killer."
    , "{} and {}'s waifu are on a date. They went in a love tunnel to make out. However, when they came out of the tunnel, only only {}'s head was on the ride. Turns out the waifu also works for the Mafia."
    , "One day {} was running across a bridge. All of a sudden, they see a child crying on the road. {} walks up to the child and asks whats wrong. In the next five minutes, {} was found dead by a tunnel.",
    "{} is on a date (somehow). When {} asked the date what is his/her occupation she said 'Hired Gun' and shot {} 3 times. Press f to pay respect.",
    "{} is at a concert one night with {}'s friends. When the friends came back from the bathroom, {} was found strangled.",
    "{} was plagued by a dreams of slenderman. The one fateful night came. {} was found in his room dead. When the cops analyzed the footage from his computer, there was no slenderman or supernatural force, it white light was shining above a suit. {} scared himself so hard, he pissed himself and died of a heartattack.",
    "{} was walking alone at night(because {} has no friends) when suddenly a van pulled over and grabbed {}. The body was found later in a dumpster.",
    "{} was playing super smash bros one night, when suddenly {}'s house exploded and {} lost to a level 1 CPU.",
    "Some random stranger said he wants to help {} to become a movie star. {} happily accepted the offer, but after entering the room, {} said 'Wait a minute, this isn't a porn studio. It's a room full of mobsters!'",
    "{} was found dead in the room. {} thought it was bdsm. Turns out, {} was whipped to death.",
    "{} trained in martial arts by watching Bruce Lee movies, and {} decided that he is now the master of fighting. {} was later found dead in a dark alley. What a legend."]

    goodS = ["{} ate a cookie and started choking. Luckily the doctor was nearby and saved {}. Turns out someone replaced the chocolate chips with rocks. Ew.",
    "{} was playing hearthstone when suddenly the computer exploded. Thankfully the doctor was outside the house and saved {} just in time. Sadly {} lost the match due to afk and is still stuck in rank 25.",
    "One day {} saw a kitten on the road. When {} went over to pet it the kitten exploded. Thankfully {} survived because the doctor was there.",
    "{} was eating ice cream at a park when {} started feeling ill and collapsed. Thankfully the doctor was there and took {} to a hospital quickly.",
    "{} went to Disneyland, but {} was stabbed by a Micky Mouse. Thankfully the doctor was also there and saved {}.",
    "{} wanted to buy a skin but {} is out of money, so {} decided to loan some money from the Mafia. The body was found 2 hours later."]
    def __init__(self, outcome, victim):
        if outcome == "alive":
            self.story = random.choice(self.goodS)
        else:
            self.story = random.choice(self.badS)
        self.victim = victim
    
    def __str__(self):
        return self.story.format(self.victim, self.victim, self.victim)