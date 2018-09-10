import discord
from discord.ext import commands
import asyncio
import os
import random
import MAFIA.story as story
import MAFIA.prep as prep
import MAFIA.gvar as gvar

class mafia:
    def __init__(self, bot):
        self.bot = bot
        
    gameOn = False
    ready = False

    mafiaList = [] #Names 
    DDList = [] #Names
    liveList = [] #names
    nominateList = []
    mChannel = None

    mLive = 0
    mDead = 0
    vLive = 0
    vDead = 0

    mafiaPlayers = {}

    victim = None
    healVictim = None
    pastHeal = None

    mafia = None #user
    doctor = None #user
    detective = None #user
    villagers = [] #id
    werewolf = [] #id
    politician = None #id

    @commands.command(pass_context = True)
    async def joinP(self, ctx):
        if self.gameOn == True or self.ready == True:
            await self.bot.send_message(ctx.message.channel, "You cannot currently join right now because there is a game going on.")
        else:
            if not ctx.message.author in self.mafiaPlayers.keys():
                self.mafiaPlayers[ctx.message.author] = "" # add author to dictionary

                await self.bot.send_message(ctx.message.channel, "You have been added to the list.")
                embed = discord.Embed(title = "Mafia Party:".format(), colour = discord.Colour.purple())
                server = ctx.message.server
                for player in self.mafiaPlayers.keys():
                    embed.add_field(name = "Player:", value = "{}".format(player.name), inline = False)
                await self.bot.send_message(ctx.message.channel, embed = embed)
            else:
                await self.bot.send_message(ctx.message.channel, "You are already in the party.")

    @commands.command(pass_context = True)
    async def leaveP(self, ctx):
        if self.gameOn == True or self.ready == True:
            await self.bot.send_message(ctx.message.channel, "You cannot currently leave right now because there is a game going on.")
        else:
            if not ctx.message.author in self.mafiaPlayers.keys():
                await self.bot.send_message(ctx.message.channel, "You are not in the party.")
            else:
                self.mafiaPlayers.pop(ctx.message.author, None)
                await self.bot.send_message(ctx.message.channel, "You have left the party.")

    @commands.command(pass_context = True)
    async def party(self, ctx):
        server = ctx.message.server
        embed = discord.Embed(title = "Mafia Party:".format(), colour = discord.Colour.purple())
        server = ctx.message.server
        for player in self.mafiaPlayers.keys():
            embed.add_field(name = "Player:", value = "{}".format(player.name), inline = True)
        await self.bot.send_message(ctx.message.channel, embed = embed)

    @commands.command(pass_context = True)
    async def setGame(self, ctx):
        #if len(self.mafiaPlayers) < 5:
            #await self.bot.send_message(ctx.message.channel, "Sorry. You need at least 5 people to play the game. You only have {} players.".format(len(self.partyL)))
        #else:
        if self.ready == True:
            await self.bot.send_message(ctx.message.channel, "You have already set up. Type /start to begin.")
        
        elif self.gameOn == True:
            await self.bot.send_message(ctx.message.channel, "There is already a game playing.")

        else:
            server = ctx.message.server
            self.ready = True

            prepObj = prep.prepare(self.bot, self.mafiaPlayers)
            prepObj.assignRoles()
            # Finished settings roles

            # Inform player of roles
            for player, data in self.mafiaPlayers.items():
                if(data.roleName == 'mafia'):
                    embed = discord.Embed(title = "You are the Mafia. Your job is to kill everyone. Pretty simple.", colour = discord.Colour.red())
                    embed.set_thumbnail(url = "https://images2.minutemediacdn.com/image/upload/c_scale,w_912,h_516,c_fill,g_auto/shape/cover/sport/5b73276e8f1752549a000001.jpeg")
                    await self.bot.send_message(player, embed = embed)
                elif(data.roleName == 'doctor'):
                    embed = discord.Embed(title = "You are the Doctor. Your job is to save people. But you can't save the same person twice in a row.", colour = discord.Colour.blue())
                    embed.set_thumbnail(url = "https://res.cloudinary.com/teepublic/image/private/s--NyIx9Nop--/t_Preview/b_rgb:c62b29,c_limit,f_jpg,h_630,q_90,w_630/v1469022975/production/designs/592798_1.jpg")
                    await self.bot.send_message(player, embed = embed)
                elif(data.roleName == 'detective'):
                    embed = discord.Embed(title = "You are the Detective. Your job is to find the Mafia.", colour = discord.Colour.orange())
                    embed.set_thumbnail(url = "https://78.media.tumblr.com/9681fb542682771069c3864dcbae7ef8/tumblr_o1mh5vUWe91r0sasuo1_400.gif")
                    await self.bot.send_message(player, embed = embed)
                elif(data.roleName == 'politician'):
                    embed = discord.Embed(title = "You are the Politician. You're just another villager, but you can accept bribe from Mafia to be on his side. Sounds fun. And realistic.", colour = discord.Colour.green())
                    await self.bot.send_message(player, embed = embed)
                else:
                    embed = discord.Embed(title = "You are just a normal innocent villager who might get accused for crimes you didn't commit ¯\_(ツ)_/¯ ", colour = discord.Colour.dark_gold())
                    embed.set_thumbnail(url = "https://www.ssbwiki.com/images/thumb/a/ac/Villager_SSBU.png/250px-Villager_SSBU.png")
                    await self.bot.send_message(player, embed = embed)
            await self.bot.create_channel(server, "mafia")
            await self.bot.send_message(ctx.message.channel, "Everything's ready! Type /start to start the game!")


    @commands.command(pass_context = True)
    async def deleteMafia(self, ctx):
        try:
            server = ctx.message.server
            channel = self.findChannel(server)
            await self.bot.delete_channel(channel)
        except Exception:
            await self.bot.send_message(ctx.message.channel, "Error")
    
    @commands.command(pass_context = True)
    async def start(self, ctx):
        if self.ready == False:
            await self.bot.send_message(ctx.message.channel, "You didn't set up yet. Type /setGame first.")
        
        elif self.gameOn == True:
            await self.bot.send_message(ctx.message.channel, "There is already a game going on!")
        else:
            self.gameOn = True
            server = ctx.message.server
            channel = self.findChannel(server)
            for player in self.mafiaPlayers.keys():
                await self.bot.send_message(channel, player.mention)
            intro = discord.Embed(title = "Welcome to Mafia!", description = "If you haven't read the rules yet, please type /helpM to view them in your dm!", colour = discord.Colour.dark_purple())
            intro.set_image(url = "https://pre00.deviantart.net/5183/th/pre/i/2018/011/f/5/league_of_legends___mafia_miss_fortune_by_snatti89-dbznniv.jpg")
            await self.bot.send_message(channel, embed = intro)
            await asyncio.sleep(3)

            await self.bot.send_message(channel, "Alright! Let this game begin!")
            await asyncio.sleep(1)
            mafiaList = []
            mafiaCount = 0
            for player, data in self.mafiaPlayers.items():
                if(data.roleName == 'mafia'):
                    mafiaList.append(player)
                    mafiaCount += 1


            while True:
                doctorAlive = False
                detAlive = False
                temp = [] # names
                for player, data in self.mafiaPlayers.items():
                    if (data.alive == True):
                        temp.append(player.name.lower())
                embed = discord.Embed(title = "It is currently nightime, so everyone mute yourself. Please.", colour = discord.Colour.dark_blue())
                await self.bot.send_message(channel, embed = embed)

                await asyncio.sleep(3)
                embed = discord.Embed(title = "Mafia please check your dm.", colour = discord.Colour.dark_green())
                await self.bot.send_message(channel, embed = embed)


                #Mafia turn
                #self.MafiaTurn(ctx)
                
                mafiaNames = []
                for item in mafiaList:
                    mafiaNames.append(item.name.lower())
                mafiaKillVote = {}
                for player in mafiaList:

                    tempM = []

                    for thing in temp:
                        if not thing in mafiaNames:
                            tempM.append(thing)

                    embed = discord.Embed(title = "Targets", colour = discord.Colour.purple())
                    embed.add_field(name = "Who is your target?", value = "Be sure to include any numbers and spaces", inline = False)
                    for item in tempM:
                        embed.add_field(name = "{}".format(item), value = "Kill me!", inline = False)
                    embed.set_image(url = "https://www.mobafire.com/images/champion/skins/landscape/graves-mafia.jpg")
                    await self.bot.send_message(player, embed = embed)

                    answer = await self.bot.wait_for_message(author = player)
                    while True:
                        if answer.content.lower() in tempM:
                            self.victim = answer.content.lower()
                            await self.bot.send_message(player, "Gotcha. You may now return to the mafia channel")
                            await self.bot.send_message(channel, "Got it Mafia.")
                            break
                        else:
                            await self.bot.send_message(player, "Error. Please check your spelling. Be sure to include any spaces, and numbers!")
                            answer = await self.bot.wait_for_message(author = player)
                
                #Doctor turn
                
                for player, data in self.mafiaPlayers.items():
                    if(data.roleName == 'doctor'):
                        doctorUser = player
                        doctorAlive = True

                # Only if doc is alive
                if doctorAlive == True:
                    await self.bot.send_message(channel, "Doctor please check your DM.")
                    embed = discord.Embed(title = "Targets", colour = discord.Colour.purple())
                    tempD = []
                    for stuff in temp:
                        if stuff.lower() != self.pastHeal:
                            tempD.append(stuff)
                    for item in tempD:
                        embed.add_field(name = "{}".format(item), value = "Save me!", inline = False)
                        
                    embed.set_image(url = "https://vignette.wikia.nocookie.net/leagueoflegends/images/f/f7/Akali_NurseSkin_old.jpg/revision/latest?cb=20120609043410")
                    await self.bot.send_message(doctorUser, embed = embed)  
                    
                    await self.bot.send_message(doctorUser, "Alright who do you want to save?")
                    answer = await self.bot.wait_for_message(author = doctorUser)
                    while True:
                            if answer.content.lower() == self.pastHeal:
                                await self.bot.send_message(doctorUser, "You cannot heal the same person twice in a row!")
                                answer = await self.bot.wait_for_message(author = doctorUser)
                            elif answer.content.lower() in tempD:
                                self.healVictim = answer.content.lower()
                                self.pastHeal = answer.content.lower()
                                await self.bot.send_message(doctorUser, "Gotcha. You may now return to the mafia channel.")
                                await self.bot.send_message(channel, "Got it Doctor.")
                                break
                            else:
                                await self.bot.send_message(player, "Error. Please check your spelling. Be sure to include any spaces and numbers!")
                                answer = await self.bot.wait_for_message(author = doctorUser)

                #Detective turn
                
                for player, data in self.mafiaPlayers.items():
                    if(data.roleName == 'detective'):
                        detUser = player
                        detAlive = True

                # only if det is alive
                if detAlive == True:
                    tempDT = []
                    await self.bot.send_message(channel, "Detective please check your DMs.")

                    embed = discord.Embed(title = "Targets", colour = discord.Colour.purple())
                    embed.add_field(name = "Who do you suspect?", value = "Please include all spaces and numbers.", inline = False)
                    for item in tempDT:
                        embed.add_field(name = "{}".format(item), value = "Pick me!", inline = True)
                    embed.set_image(url = "https://na.leagueoflegends.com/sites/default/files/styles/scale_xlarge/public/upload/cops_1920.jpg?itok=-T6pbISx")
                    await self.bot.send_message(detUser, embed = embed)
                    for stuff in temp:
                        if stuff != detUser.name:
                            tempDT.append(stuff)
                    suspect = "Boi"
                    for player, data in self.mafiaPlayers.items():
                        if(data.roleName == 'suspect'):
                            suspect = player.name
                    answer = await self.bot.wait_for_message(author = detUser)
                    while True:
                            if answer.content.lower() in tempDT:
                                if answer.content.lower() in mafiaNames or answer.content.lower() == suspect:
                                    embed = discord.Embed(title = "Yes. That person is the mafia. Now try to convince the others. Please return to the mafia chat now.", colour = discord.Colour.green())
                                    
                                else:
                                    embed = discord.Embed(title = "Sorry. That person is not the mafia. Please return to the mafia chat now.", colour = discord.Colour.dark_red())
                                
                                await self.bot.send_message(detUser, embed = embed)
                                break
                            else:
                                await self.bot.send_message(detUser, "Error. Please check your spelling. Be sure to include any spaces, and numbers!")
                                answer = await self.bot.wait_for_message(author = detUser)

                if self.victim == self.healVictim:
                    saved = True
                else:
                    saved = False

                #Storytime
                await self.bot.send_message(channel, "Alright everybody get your ass back here and unmute yourself. It's storytime.")
                await asyncio.sleep(3)
                story1 = discord.Embed(title = "Story", description = "All of these stories are written by Ernest and Leonard", colour = discord.Colour.purple())
                await self.bot.send_message(channel, embed = story1)
                if saved == True:
                    aStory = story.storyTime("alive", self.victim)
                    storyEmbed = discord.Embed(title = "{} lives!".format(self.victim), description = "{}".format(aStory), colour = discord.Colour.green())
                    storyEmbed.set_thumbnail(url = "https://vignette.wikia.nocookie.net/dragonfable/images/f/f1/Heal_Icon.png/revision/latest?cb=20130329031111")
                else:
                    aStory = story.storyTime("dead", self.victim)
                    storyEmbed = discord.Embed(title = "{} died :(".format(self.victim), description = "{}".format(aStory), colour = discord.Colour.red())
                    storyEmbed.set_thumbnail(url = "https://image.flaticon.com/icons/png/512/155/155266.png")
                    for player, data in self.mafiaPlayers.items():
                        if (player.name.lower() == self.victim):
                            data.alive = False

                await self.bot.send_message(channel, embed = storyEmbed)
                await asyncio.sleep(3)
                check = self.checkWin(mafiaCount)


                if check == "m":
                    embed = discord.Embed(title = "The mafia(s) win!", colour = discord.Colour.purple())
                    for item in mafiaList:
                        embed.add_field(name = "{}".format(item.name), value = "I'm the Mafia!", inline = False)
                    await self.bot.send_message(channel, embed = embed)
                    await self.bot.send_message(channel, "Thank you all for playing!")
                    await asyncio.sleep(10)
                    await self.bot.delete_channel(channel)
                    break


                elif check == "v":
                    embed = discord.Embed(title = "The villagers win", colour = discord.Colour.purple())
                    for item in mafiaList:
                        embed.add_field(name = "{}".format(item.name), value = "I'm the Mafia!", inline = False)
                    await self.bot.send_message(channel, embed = embed)
                    await self.bot.send_message(channel, "Thank you all for playing!")
                    await asyncio.sleep(10)
                    await self.bot.delete_channel(channel)
                    break


                elif check == "none": # lynch
                    await self.bot.send_message(channel, "Now I'll give you guys 2 min to talk.")
                    #await asyncio.sleep(120)

                    # nomination
                    nom = discord.Embed(title = "Players:", colour = discord.Colour.purple())
                    await self.bot.send_message(channel, "Alright! Any nominations? Just type them in the chat. You have 5 seconds to submit each nomination. When you're done just wait for the timer to finish.")
                    for item in temp:
                        nom.add_field(name = "{}".format(item), value = "Pick me!", inline = False)
                    await self.bot.send_message(channel, embed = nom)


                    nomination = await self.bot.wait_for_message(timeout = 5, channel = channel)
                    embed = discord.Embed(title = "Nominations", colour = discord.Colour.purple())
                    while True:
                        if nomination == None:
                            await self.bot.send_message(channel, "The nomination time is closed.")
                            if self.nominateList:
                                await self.bot.send_message(channel, embed = embed)
                            break
                        elif nomination.author == self.bot.user:
                            nomination = await self.bot.wait_for_message(timeout = 5, channel = channel)
                    
                        elif nomination.content.lower() in temp and not nomination.content.lower() in self.nominateList:
                            self.nominateList.append(nomination.content.lower())
                            embed.add_field(name = "{}".format(item), value = "Nominated to die!", inline = False)
                            await self.bot.send_message(channel, "{} has been added to the nomination list. Any other ones?".format(nomination.content.lower()))
                            await self.bot.send_message(channel, embed = embed)
                                
                            nomination = await self.bot.wait_for_message(timeout = 5, channel = channel)
                        elif not nomination.content.lower() in temp or nomination.content.lower() in self.nominateList:
                            await self.bot.send_message(channel, "Error. Not valid nomination. This person either doesn't exist or is already in the nomination list.")
                            nomination = await self.bot.wait_for_message(timeout = 5, channel = channel)

                    # voting time
                    if self.nominateList:
                        authors = []
                        scoreName = []
                        score = []
                        await self.bot.send_message(channel, "Ok! Now it's time to vote! The person with the most votes dies and he or she must have two or more votes.")
                        for item in self.nominateList:
                            scoreName.append(item)
                            votes = 0
                            await self.bot.send_message(channel, "Who wants to vote for {}? Type v to vote.".format(item))
                            vote = await self.bot.wait_for_message(timeout = 5, content = "v", channel = channel)


                            while True:
                                if vote == None:
                                    break
                                elif vote.author == self.bot.user:
                                    vote = await self.bot.wait_for_message(timeout = 5, content = "v", channel = channel)
                                elif vote.author.name in authors:
                                    await self.bot.send_message(channel, "You have voted already. Or your input was incorrect.")
                                    vote = await self.bot.wait_for_message(timeout = 5, content = "v", channel = channel)
                                elif not vote.author.name.lower() in temp:
                                    await self.bot.send_message(channel, "You are not in the game, or you're dead.")
                                    vote = await self.bot.wait_for_message(timeout = 5, content = "v", channel = channel)
                                elif not vote.author.name.lower() in authors and vote.author.name.lower() in temp:
                                    authors.append(vote.author.name)
                                    votes+=1
                                    await self.bot.send_message(channel, "One vote has been put into {}".format(item))
                                    vote = await self.bot.wait_for_message(timeout = 5, content = "v", channel = channel)
                                
                            score.append(votes)
                            embed = discord.Embed(title = "Total votes for {}".format(item), description = "{}".format(votes), colour = discord.Colour.purple())
                            await self.bot.send_message(channel, embed = embed)
                        

                        # finds largest vote
                        largestVote = 0
                        for item in score:
                            if item > largestVote and item > 1:
                                largestVote = item
                            elif item == largestVote:
                                largestVote = 0
                        
                        # kills nominated

                        if largestVote != 0:
                            deadGuy = scoreName[score.index(largestVote)]
                            embed = discord.Embed(title = "{} has been hanged by the village. Press f to pay respect.".format(deadGuy), colour = discord.Colour.red())
                            embed.set_image(url = "https://cdn.shopify.com/s/files/1/0895/0864/products/42-47714084_1024x1024.jpeg?v=1451772538")
                            await self.bot.send_message(channel, embed = embed)
                            for player, data in self.mafiaPlayers.items():
                                if (player.name.lower() == deadGuy.lower()):
                                    data.alive = False
                        elif largestVote == 0:
                            await self.bot.send_message(channel, "No one was hanged.")
                                    
                    else:
                        await self.bot.send_message(channel, "No one was hanged.")
                    
                    check = self.checkWin(mafiaCount)

                    if check == "m":
                        embed = discord.Embed(title = "The mafia(s) win!", colour = discord.Colour.purple())
                        for item in mafiaList:
                            embed.add_field(name = "{}".format(item.name), value = "I'm the Mafia!", inline = False)
                        await self.bot.send_message(channel, embed = embed)
                        await asyncio.sleep(10)
                        await self.bot.delete_channel(channel)
                        break
                    elif check == "v":
                        embed = discord.Embed(title = "The villagers win!", colour = discord.Colour.purple())
                        for item in mafiaList:
                            embed.add_field(name = "{}".format(item.name), value = "I'm the Mafia!", inline = False)
                        await self.bot.send_message(channel, embed = embed)
                        await asyncio.sleep(10)
                        await self.bot.delete_channel(channel)
                        break
        self.ready = False
        self.gameOn = False
                
                    
                    

    @commands.command(pass_context = True)
    async def helpM(self, ctx):
        embed = discord.Embed(title = "Mafia Game", colour = discord.Colour.orange())
        embed.add_field(name = "How to play:", value = "To play, there must be at least 5 people in the Mafia party.", inline = False)
        embed.add_field(name = "#1", value = "When the game starts, each player will receive their role through dm.", inline = False)
        embed.add_field(name = "#2", value = "Everyone will go to sleep. The Mafia would be the first to wake up, and through dm he/she can choose which player to kill.", inline = False)
        embed.add_field(name = "#3", value = "After, the doctor will wake up, and he/she can choose a person to save through dm.", inline = False)
        embed.add_field(name = "#4", value = "Finally, the detective will wake up and choose a person to accuse through dm. He/she would be informed if the person is the Mafia. If he/her investigates the suspect, then he/she will be informed that the suspect is the mafia.", inline = False)
        embed.add_field(name = "#5", value = "Everybody wakes up and the bot will inform you through the mafia channel who was killed. The group has a minute to discuss who is the Mafia.", inline = False)
        embed.add_field(name = "#6", value = "Everyone then nominate and vote on people to lynch. The most voted person will then be lynched.")
        embed.add_field(name = "#7", value = "The cycle continues until only if the number of mafias are greater than villagers, the mafia kills everyone, or all the mafia dies.")
        embed.set_footer(text = "For more information, type /helpR for roles, /helpC for commands, and /helpGame for setup.")
        await self.bot.send_message(ctx.message.author, embed = embed)

    @commands.command(pass_context = True)
    async def helpR(self, ctx):
        embed = discord.Embed(title = "Mafia Roles", colour = discord.Colour.orange())
        embed.add_field(name = "Mafia", value = "Side: Mafia. Your role is to kill everyone. And don't get caught.", inline = False)
        embed.add_field(name = "Doctor", value = "Side: Villager. Your role is to save people. You cannot save the same person twice in a row.", inline = False)
        embed.add_field(name = "Detective", value = "Side: Villager. Your role is to find the mafia and tell everyone.", inline = False)
        embed.add_field(name = "Suspect", value = "Side: Villager. When inspected by the detective, the suspect would return Mafia, even though the suspect is on the villager's side. The suspect won't know that he/she is a suspect. There must be at least 6 people to have a chance of gaining this role.", inline = False)
        await self.bot.send_message(ctx.message.author, embed = embed)
    
    @commands.command(pass_context = True)
    async def helpC(self, ctx):
        embed = discord.Embed(title = "Mafia Commands", colour = discord.Colour.orange())
        embed.add_field(name = "/joinP", value = "Joins the current mafia party.", inline = False)
        embed.add_field(name = "/leaveP", value = "Leaves the current mafia party.", inline = False)
        embed.add_field(name = "/party", value = "Displays current party.", inline = False)
        embed.add_field(name = "/setGame", value = "Sets up the game.(Must do before /start)", inline = False)
        embed.add_field(name = "/start", value = "Starts the game with the current people in the mafia party. Must do /setGame first.", inline = False)
        await self.bot.send_message(ctx.message.author, embed = embed)
    
    @commands.command(pass_context = True)
    async def helpGame(self, ctx):
        embed = discord.Embed(title = "Mafia Setup", colour = discord.Colour.orange())
        embed.add_field(name = "Requirement:", value = "There must be at least 5 people in the mafia party.", inline = False)
        embed.add_field(name = "Joining the Game:", value = "Everyone playing must enter /joinP to join the party. Type /leaveP to leave the party.", inline = False)
        embed.add_field(name = "Step 1", value = "Enter /setGame to set up and assign the roles for the game.", inline = False)
        embed.add_field(name = "Step 2", value = "Enter /start to start the game.", inline = False)
        embed.add_field(name = "Step 3", value = "Play", inline = False)
        await self.bot.send_message(ctx.message.author, embed = embed)
        
    async def MafiaTurn(self, ctx):
        
        mafiaList = []
        for player, data in self.mafiaPlayers.items():
            if(data.roleName == 'mafia'):
                mafiaList.append(player)
        
        mafiaKillVote = {}
        for player in mafiaList:
            await self.bot.send_message(player, 'Vote for a player to kill! (The vote must be unanimous)')
            await self.bot.send_message(player, "Who is your target? (Just type the name. Include any spaces and numbers.)")
            embed = self.displayMember(ctx.message.channel, self.mafiaList)
            await self.bot.send_message(player, embed = embed)
            answer = await self.bot.wait_for_message(author = player, channel = player)
            while True:
                if answer.content.lower() in self.liveList:
                    self.victim = answer.content()
                    await self.bot.send_message(ctx.message.channel, "Got it")
                    break
                else:
                    await self.bot.send_message(player, "Error. Make sure your spelling is correct and you include the whole name(including numbers). Also no /.")
                    answer = await self.bot.wait_for_message(author = player, channel = player)

    def findChannel(self, server):
        for item in server.channels:
            if item.name == 'mafia':
                return item
    
    def checkGame(self, mafias, status, mafiaV):
        num = 0
        if mafiaV == True:
            for player, data in mafias.items():
                if data.roleName == "mafia":
                    if data.alive == status:
                        num += 1
        else:
            for player, data in mafias.items():
                if data.roleName != "mafia":
                    if data.alive == status:
                        num += 1
        return num
    
    def checkWin(self, mafiaCount):
        self.mLive = self.checkGame(self.mafiaPlayers, True, True)
        self.mDead = self.checkGame(self.mafiaPlayers, False, True)
        self.vLive = self.checkGame(self.mafiaPlayers, True, False)
        self.vDead = self.checkGame(self.mafiaPlayers, False, False)
        if self.mLive >= self.vLive or (self.vLive ==1 and self.mLive >= 1):
            return "m"
        elif self.mDead == mafiaCount:
            return "v"
        else:
            return "none"
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
        for item in group.keys():
            name = server.get_member(item)
            embed.add_field(name = "{}".format(name), value = "Kill me!", inline = False)
        return embed

def setup(bot):
    bot.add_cog(mafia(bot))