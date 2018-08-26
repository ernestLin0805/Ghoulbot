import discord
from discord.ext import commands
import asyncio
import os
import random
import MAFIA
from MAFIA import story
from MAFIA import prep
from MAFIA import gvar
class mafia:
    def __init__(self, bot):
        self.bot = bot
        
    gameOn = False
    ready = False

    partyL = []#ID
    mafiaList = []#Names 
    DDList = []#Names
    liveList = []#names
    nominateList = []
    mChannel = None

    victim = None
    healVictim = None
    pastHeal = None

    mafia = None#user
    doctor = None#user
    detective = None#user
    villagers = []#id
    werewolf = []#id
    politician = None#id


    @commands.command(pass_context = True)
    async def joinP(self, ctx):
        if not ctx.message.author.id in self.partyL:
            server = ctx.message.server
            self.partyL.append(ctx.message.author.id)
            await self.bot.send_message(ctx.message.channel, "You have been added to the list.")
            embed = discord.Embed(title = "Mafia Party:".format(), colour = discord.Colour.purple())
            server = ctx.message.server
            for item in self.partyL:
                embed.add_field(name = "Player:", value = "{}".format(server.get_member(item).name), inline = True)
            await self.bot.send_message(ctx.message.channel, embed = embed)
        else:
            await self.bot.send_message(ctx.message.channel, "You are already in the party.")


    @commands.command(pass_context = True)
    async def leaveP(self, ctx):
        if not ctx.message.author.id in self.partyL:
            await self.bot.send_message(ctx.message.channel, "You are not in the party.")
        else:
            self.partyL.remove(ctx.message.author.id)
            await self.bot.send_message(ctx.message.channel, "You have left the party.")

    @commands.command(pass_context = True)
    async def party(self, ctx):
        server = ctx.message.server
        embed = discord.Embed(title = "Mafia Party:".format(), colour = discord.Colour.purple())
        server = ctx.message.server
        for item in self.partyL:
            embed.add_field(name = "Player:", value = "{}".format(server.get_member(item).name), inline = True)
        await self.bot.send_message(ctx.message.channel, embed = embed)

    @commands.command(pass_context = True)
    async def setGame(self, ctx):
        #if len(self.partyL) < 5:
            #await self.bot.send_message(ctx.message.channel, "Sorry. You need at least 5 people to play the game. You only have {} players.".format(len(self.partyL)))
        #else:
        server = ctx.message.server
        self.ready = True
        self.gameOn = True
        
        prep.prepare(self.bot, self.partyL)
        self.mafia = prep.prepare.setMafia()
        self.doctor = prep.prepare.setDoctor()
        self.detective = prep.prepare.setDet()
        await self.bot.send_message(self.mafia, "You are the Mafia. Your job is to kill everyone. Pretty simple.")
        await self.bot.send_message(self.doctor, "You are the doctor. Your job is to save people. But you can't save the same person twice in a row.")
        await self.bot.send_message(self.detective, "You are the Detective. Your job is to find the Mafia.")

        chance = randInt(10, 100)
        if chance == True:
            self.politician = prep.prepare.setPolitician()
            await self.bot.send_message(self.politician, "You are the Politician. You're just another villager but you can accept bribe from Mafia to be on his side. Sounds fun. And realistic.")
        await self.bot.create_channel(server, "mafia")
        await self.bot.send_message(ctx.message.channel, "Everything's ready! Type /start to start the game!")
        
        


    @commands.command(pass_context = True)
    async def deleteMafia(self, ctx):
        try:
            server = ctx.message.server
            channel = self.findChannel(server)
            await self.bot.delete_channel(server, "mafia")
        except Exception:
            await self.bot.send_message(ctx.message.channel, "Error")
    
    @commands.command(pass_context = True)
    async def start(self, ctx):
        if self.ready == False:
            await self.bot.send_message(ctx.message.channel, "You didn't set up yet. Type /setGame first.")
        else:
            server = ctx.message.server
            mafiaUser = server.get_member(self.mafia)
            doctorUser = server.get_member(self.doctor)
            detectiveUser = server.get_member(self.detective)
            channel = self.findChannel(server)
            for item in self.partyL:
                await self.bot.send_message(channel, "<@!" + item + ">")
            intro = discord.Embed(title = "Welcome to Mafia!", description = "If you haven't read the rules yet, please type /helpM to view them in your dm!", colour = discord.Colour.dark_purple())
            intro.set_thumbnail(url = "https://pre00.deviantart.net/5183/th/pre/i/2018/011/f/5/league_of_legends___mafia_miss_fortune_by_snatti89-dbznniv.jpg")
            await self.bot.send_message(channel, embed = intro)
            await asyncio.sleep(3)


            await self.bot.send_message(channel, "Alright! Let this game begin! It's night time so everybody mute yourself in the voice chat!.")
            await asyncio.sleep(1)

            #Mafia turn
            await self.bot.send_message(channel, "Mafia please check your dm.")
            await self.bot.send_message(mafiaUser, "Who is your target?(Just type the name. Include any spaces and numbers.)")
            embed = self.displayMember(server, self.mafiaList)
            await self.bot.send_message(mafiaUser, embed = embed)
            answer = await self.bot.wait_for_message(author = mafiaUser, channel = mafiaUser)
            while True:
                if answer.content.lower() in self.liveList:
                    self.victim = answer.content()
                    await self.bot.send_message(channel, "Got it")
                    break
                else:
                    await self.bot.send_message(mafiaUser, "Error. Make sure your spelling is correct and you include the whole name(including numbers). Also no /.")
                    answer = await self.bot.wait_for_message(author = mafiaUser, channel = mafiaUser)
            
            #Doctor turn
            await self.bot.send_message(channel, "Doctor please check your dm.")
            await self.bot.send_message(doctorUser, "Who do you want to save?(Just type the name)")
            embed = self.displayMember(server, self.DDList)
            await self.bot.send_message(doctorUser, embed = embed)
            answer = await self.bot.wait_for_message(author = doctorUser, channel = doctorUser)
            while True:
                if answer.content.lower() in self.liveList and self.pastHeal != answer.content.lower():
                    self.healVictim = answer.content()
                    break
                else:
                    await self.bot.send_message(ctx.message.author, "Error. Make sure your spelling is correct and you include the whole name(including numbers and no /). Also you can't heal the same person twice in a row.")
                    answer = await self.bot.wait_for_message(author = doctorUser, channel = doctorUser)
            
            #Detective turn
            await self.bot.send_message(channel, "Got it. Detective please check your dm.")
            await self.bot.send_message(detectiveUser, "Who do you suspect?(Just type the name)")
            self.displayMember(server, self.DDList)
            await self.bot.send_message(detectiveUser, embed = embed)
            answer = await self.bot.wait_for_message(author = detectiveUser, channel = detectiveUser)
            while True:
                if answer.content.lower() in self.liveList:
                    if answer.content.lower() == mafiaUser.name.lower():
                        await self.bot.send_message(detectiveUser, "Yes. Congrats. He is the mafia. Now try to get people to kill him.")
                    else:
                        await self.bot.send_message(detectiveUser, "Nope. He is not the mafia. Nice try though.")
                    break
                else:
                    await self.bot.send_message(ctx.message.author, "Error. Make sure your spelling is correct and you include the whole name(including numbers). Also no /.")
                    answer = await self.bot.wait_for_message(author = detectiveUser, channel = detectiveUser)

            if self.victim == self.healVictim:
                saved = True
            else:
                saved = False

            #Storytime
            await self.bot.send_message(channel, "Alright everybody get your ass back here and unmute yourself. It's storytime.")
            if saved == True:
                story1 = story.storyTime("alive", self.victim)
            else:
                story1 = story.story("dead", self.victim)
            await self.bot.send_message(channel, story1)

            await self.bot.send_message(channel, "Now I'll give you guys 2 min to talk.")
            await asyncio.sleep(120)

            await self.bot.send_message(channel, "Alright! Any nominations? Just type them in the chat. You have 20 seconds to submit each nomination. When you're done just wait for the timer to finish.")
            nomination = await self.bot.wait_for_message(timeout = 20, channel = channel)
            while True:
                if nomination.content.lower() in self.liveList and not nomination.content.lower() in self.nominateList:
                    self.nominateList.append(nomination.content.lower())
                    await self.bot.send_message(channel, "{} has been added to the nomination list. Any other ones?")
                    nomination = await self.bot.wait_for_message(timeout = 20, channel = channel)
                elif nomination.content == None:
                    await self.bot.send_message(channel, "Ok! No more nominations! Here is the list.")
                    embed = discord.Embed(title = "Nominations", colour = discord.Colour.blue())
                    for item in self.nominateList:
                        embed.add_field(name = "{}".format(item), value = "Nominated to die!", inline = False)
                    await self.bot.send_message(channel, embed = embed)
                    break
                else:
                    await self.bot.send_message("Error. Not valid nomination. This person either doesn't exist or is already in the nomination list.")
                    nomination = await self.bot.wait_for_message(timeout = 20, channel = channel)
            if self.nominateList:
                authors = []
                scoreName = []
                score = []
                await self.bot.send_message(channel, "Ok! Now it's time to vote! The person with the most votes dies and he or she must have two or more votes.")
                for item in self.nominateList:
                    scoreName.append(item)
                    votes = 0
                    await self.bot.send_message(channel, "Who wants to vote for {}?".format(item))
                    vote = await self.bot.wait_for_message(timeout = 20, content = "v", channel = channel)
                    while vote != None:
                        if not vote.content.author.name in authors:
                            authors.append(vote.author.name)
                            votes+=1
                        else:
                            await self.bot.send_message(channel, "You have voted already.")
                    score.append(votes)
                largestVote = 0
                for item in score:
                    if item > largestVote and item > 1:
                        largestVote = item
                if largestVote != 0:
                    deadGuy = scoreName[score.index(largestVote)]
                    await self.bot.send_message(channel, "{} has been hanged by the village. Prss f to pay respect.".format(deadGuy))
                    self.liveList.remove(deadGuy)
                else:
                    await self.bot.send_message(channel, "No one was hanged.")        


                    



    
    @commands.command(pass_context = True)
    async def helpM(self, ctx):
        embed = discord.Embed(title = "Mafia Commands", colour = discord.Colour.orange())
        embed.add_field(name = "How to play:", value = "To play, there must be at least 5 people in the Mafia party.", inline = False)
        embed.add_field(name = "#1", value = "When the game starts, each player will receive their role through dm.", inline = False)
        embed.add_field(name = "#2", value = "Everyone will go to sleep. The Mafia would be the first to wake up, and through dm he/she can choose which player to kill.", inline = False)
        embed.add_field(name = "#3", value = "After, the doctor will wake up, and he/she can choose a person to save through dm.", inline = False)
        embed.add_field(name = "#4", value = "Finally, the detective will wake up and choose a person to accuse through dm. He/she would be informed if the person is the Mafia", inline = False)
        embed.add_field(name = "#5", value = "Everybody wakes up and the bot will inform you through the mafia channel who was killed. The group has a minute to discuss who is the Mafia.", inline = False)
        embed.add_field(name = "#6", value = "Everyone then dm the bot individually and vote on a person to persecute. The bot will then inform the group whether they killed a villager or not a villager.")
        embed.add_field(name = "#7", value = "The cycle continues until only one villager and the Mafia are alive or the Mafia is killed.")
        embed.add_field(name = "Events:", value = "There are chances of events happening each round.", inline = False)
        embed.add_field(name = "Earthquakes", value = "10 percent chance of killing a person each round.", inline = False)
        embed.add_field(name = "Bloodmoon/Werewolf", value = "In game, each villager has 33 percent chance to become a werewolf during bloodmoon. During this time they can kill whoever they want.", inline = False)
        embed.add_field(name = "Politician", value = "With a 10 percent chance of getting this role, the Mafia can bribe this person to work for him. The politician has the option to say yes or no to the bribe. If bribed, this role will be on the side of the Mafia.", inline = False)
        embed.add_field(name = "Commands:", value = "Here are the possible commands.", inline = False)
        embed.add_field(name = "/party", value = "Shows the members currently in the Mafia Party.", inline = False)
        embed.add_field(name = "/joinP", value = "Joins the party.", inline = False)
        embed.add_field(name = "/leaveP", value = "Leaves the party.", inline = False)
        embed.add_field(name = "/setGame", value = "Instructs bot to set up the game(Must be done before game starts)", inline = False)
        embed.add_field(name = "/start", value = "Starts the Mafia game.", inline = False)
        embed.add_field(name = "/vote @person", value = "Votes for a person to be killed.", inline = False)
        embed.add_field(name = "/kill #", value = "Command for Mafia, werewolf, and corrupted politician. A list of people will be shown with numbers assigned to them.", inline = False)
        embed.add_field(name = "/bribe amount", value = "Bribes the politician(if there is one) with a certain amount of money.", inline = False)
        embed.add_field(name = "/save #", value = "Doctor's command. A list of people will be shown with assigned numbers.", inline = False)
        embed.add_field(name = "/inspect #", value = "Detective's command. A list of people will be shown with assigned numbers.", inline = False)
        await self.bot.send_message(ctx.message.author, embed = embed)
    def findChannel(self, server):
        for item in server.channels:
            if item.name == 'mafia':
                return item
    
    def randInt(self, chance, whole):
        result = random.randint(chance, whole)
        if result <= chance:
            return True
        else:
            return False

    def setRoles(self, ctx, group, role):
        role = random.choice(group)
        group.remove(role)

    def displayMember(self, server, group):
        embed = discord.Embed(title = "Targets", colour = discord.Colour.purple())
        for item in group:
            name = server.get_member(item)
            embed.add_field(name = "{}".format(name), value = "Kill me!", inline = False)
        return embed
def setup(bot):
    bot.add_cog(mafia(bot))