import discord
from discord.ext import commands
import json
import asyncio
import os
import random


class economy:
    
    def __init__(self, bot):
        self.bot = bot
        
    starting_value = 100
    currency_type = "<:wood:478383029891498006>"
    def update_data(self, users, user):
        if not user.id in users:
            users[user.id] = {}
            users[user.id]['balance'] = self.starting_value
    
    def runGamble(self, chance, max):
        result = random.randint(1, max)
        if result <= chance:
            return True
        else:
            return False
    def checkBalance(self, users, user, checkAmount):
        if users[user.id]["balance"] < checkAmount:
            return False
        else:
            return True

    def gambleNow(self, ctx, amountEntered, chance, scale):
        with open('users.json', 'r') as f:
            users = json.load(f)
        amount = int(amountEntered)
        balance = users[ctx.message.author.id]["balance"]
        if ( balance >= amount and amount >= 5):
            result = self.runGamble(chance, 100)
            if result == True:
                reward = amount*(scale)
                self.add_money(users, ctx.message.author, reward)
                embed = discord.Embed(title = "You won!!!", description = "", colour = discord.Colour.green())
                embed.add_field(name = "Your new balance is: ", value = "{} {}".format(str(users[ctx.message.author.id]["balance"]), self.currency_type))
                embed.set_thumbnail(url = "https://media.giphy.com/media/XMc1Ui9rAFR1m/source.gif")
                with open('users.json', 'w') as f:
                    json.dump(users, f)
                return (embed)
            else:
                punishment = amount
                self.subtract_money(users, ctx.message.author, punishment)
                embed = discord.Embed(title = "Sorry, you might have lost...", description = "", colour = discord.Colour.red())
                embed.add_field(name = "Your new balance is: ", value = "{} {}".format(str(users[ctx.message.author.id]["balance"]), self.currency_type))
                embed.set_thumbnail(url = "https://media1.giphy.com/media/Ty9Sg8oHghPWg/giphy.gif")
                with open('users.json', 'w') as f:
                    json.dump(users, f)
                return (embed)  
        elif amount < 5:
            return "You must bet at least 5 {}".format(self.currency_type)
        else:
            return "Lol you don't have that much {}. You only have {}{}".format(self.currency_type, users[ctx.message.author.id]["balance"], self.currency_type)

    async def on_member_join(self, member):
        with open('users.json', 'r') as f:
            users = json.load(f)
        self.update_data(users, member)
        with open('users.json', 'w') as f:
            json.dump(users, f)

    @commands.command(pass_context=True)
    async def balance(self, ctx):
        with open('users.json', 'r') as f:
            users = json.load(f)
        user = ctx.message.author

        if not user.id in users:
            await self.bot.send_message(ctx.message.channel,"You're not in the database. I have registered you into the database with a starting value of 100 {}.".format(self.currency_type))
            self.update_data(users, user)
        else:
            balance = users[user.id]['balance']
            embed = discord.Embed(title = "Your balance:  ", description = "{} {}".format(balance, self.currency_type), colour = discord.Colour.green())
            await self.bot.send_message(ctx.message.channel,"<@!" + ctx.message.author.id + ">")
            await self.bot.send_message(ctx.message.channel, embed = embed)
        
        with open('users.json', 'w') as f:
            json.dump(users, f)

    @commands.command(pass_context=True)
    async def registerBank(self, ctx):
        with open('users.json', 'r') as f:
            users = json.load(f)
        user = ctx.message.author
        if not user.id in users:
            self.update_data(users, ctx.message.author)
            await self.bot.send_message(ctx.message.channel, "You are now registered in the bank with a starting value of 100 {}".format(self.currency_type))
        else:
            await self.bot.send_message(ctx.message.channel, "You are already in the database")
        with open('users.json', 'w') as f:
            json.dump(users, f)
    @commands.command(pass_context = True)
    async def give(self, ctx, amountInput, user: discord.Member):
        if ctx.message.author.server_permissions.administrator == True:
            amount = int(amountInput)
            with open('users.json', 'r') as f:
                users = json.load(f)
            self.add_money(users, user, amount)
            await self.bot.send_message(ctx.message.channel, "{} {} has been added to {}'s balance. {}'s new balance is {} {}.".format(amount, self.currency_type, user.name, user.name, users[user.id]['balance'], self.currency_type))
            with open('users.json', 'w') as f:
                json.dump(users, f)
        else:
            await self.bot.send_message(ctx.message.channel, "You don't have the permission to do this.")

    @commands.command(pass_context = True)
    async def take(self, ctx, amountInput, user: discord.Member):
        if ctx.message.author.server_permissions.administrator == True:
            amount = int(amountInput)
            with open('users.json', 'r') as f:
                users = json.load(f)
            self.subtract_money(users, user, amount)
            await self.bot.send_message(ctx.message.channel, "{} {} has been taken from {}'s balance.".format(amount, self.currency_type, user.name))
            with open('users.json', 'w') as f:
                json.dump(users, f)
        else:
            await self.bot.send_message(ctx.message.channel, "You don't have the permission to do this.")


    @commands.command(pass_context=True)
    async def gambleEasy(self, ctx, amountEntered):
        try:
            msg = self.gambleNow(ctx, amountEntered, 40, (1/2))
            try:
                await self.bot.send_message(ctx.message.channel, "<@!" + ctx.message.author.id + ">")
                await self.bot.send_message(ctx.message.channel, embed = msg)
            except Exception:
                await self.bot.send_message(ctx.message.channel, msg)
        except Exception:
            await self.bot.send_message(ctx.message.channel, "You can only bet with whole positive integers.")
    @commands.command(pass_context=True)
    async def flip(self, ctx, arg1, arg2):
        result = random.randint(1,100)
        if result <= 50:
            await self.bot.send_message(ctx.message.channel, "It's {}!".format(arg1))
        else:
            await self.bot.send_message(ctx.message.channel, "It's {}!".format(arg2))
    @commands.command(pass_context=True)
    async def gambleMedium(self, ctx, amountEntered):
        try:
            msg = self.gambleNow(ctx, amountEntered, 20, 2)
            try:
                await self.bot.send_message(ctx.message.channel, "<@!" + ctx.message.author.id + ">")
                await self.bot.send_message(ctx.message.channel, embed = msg)
            except Exception:
                await self.bot.send_message(ctx.message.channel, msg)
        except Exception:
            await self.bot.send_message(ctx.message.channel, "You can only bet with whole positive integers.")

    @commands.command(pass_context=True)
    async def gambleHard(self, ctx, amountEntered):
        try:
            msg = self.gambleNow(ctx, amountEntered, 10, 3)
            try:
                await self.bot.send_message(ctx.message.channel,"<@!" + ctx.message.author.id + ">")
                await self.bot.send_message(ctx.message.channel, embed = msg)
            except Exception:
                await self.bot.send_message(ctx.message.channel, msg)
        except Exception:
                await self.bot.send_message(ctx.message.channel, "You can only bet with whole positive integers.")

    @commands.command(pass_context=True)
    async def gambleInsane(self, ctx, amountEntered):
        try:

            msg = self.gambleNow(ctx, amountEntered, 1, 10)
            try:
                await self.bot.send_message(ctx.message.channel,"<@!" + ctx.message.author.id + ">")
                await self.bot.send_message(ctx.message.channel, embed = msg)
            except Exception:
                await self.bot.send_message(ctx.message.channel, msg)
        except Exception:
            await self.bot.send_message(ctx.message.channel, "You can only bet with whole positive integers.")
    #async def on_message(self, message):
        #with open('users.json', 'r') as f:
            #users = json.load(f)
            
        #code

        #await update_data(users, message.author)
        #await add_experience(users, message.author, 5)
        #await level_up(users, message.author, message.channel)
        #with open('users.json', 'w') as f:
                #json.dump(users, f)

    @commands.command(pass_context = True)
    async def bet(self, ctx, user: discord.Member, amountEntered):
        amount = int(amountEntered)
        channel = ctx.message.channel
        memes = []
        userpoint = 0
        victimpoint = 0
        with open('users.json', 'r') as f:
            users = json.load(f)
        if users[ctx.message.author.id]["balance"] < amount or users[user.id]["balance"] < amount:
            await self.bot.send_message(channel, "One of you do not have enough to bet this much money.")
        elif amount < 4:
            await self.bot.send_message(channel, "You have to bet at least 5 {}".format(self.currency_type))
        else:
            await self.bot.send_message(channel, "<@!" + user.id + "> {} has challenged you to a bet for {}. Do you accept?(y/n)".format(ctx.message.author.name, amountEntered))
            answer = await self.bot.wait_for_message(timeout = 15, author = user)
            if answer == None:
                await self.bot.send_message(channel, "The request is expired.")
            elif answer.content.lower() == "y" or answer.content.lower() == "yes":
                await self.bot.send_message(channel, "Alright! The bet between {} and {} has begun! <@!".format(ctx.message.author.name, user.name) + ctx.message.author.id + ">please choose one of the following!(Just type the name. No need for /) ")
                dawae = discord.Embed(title = "Dawae", description = "No spaces!", colour = discord.Colour.green())
                dawae.set_thumbnail(url = "https://img00.deviantart.net/cb63/i/2018/011/4/1/ugandan_knuckles_vector_by_surizarin-dbzp0gi.png")
                memes.append(dawae)
                harambe = discord.Embed(title = "Harambe", description = "", colour = discord.Colour.red())
                harambe.set_thumbnail(url = "http://www.stickpng.com/assets/thumbs/584877837b758d6b0758d00d.png")
                memes.append(harambe)
                doge = discord.Embed(title = "Doge", colour = discord.Colour.blue())
                doge.set_thumbnail(url = "https://t6.rbxcdn.com/cd4b72933eae9505c1cff2277029d3b3")
                memes.append(doge)
                for item in memes:
                    await self.bot.send_message(channel, embed = item)
                answer = await self.bot.wait_for_message(timeout = 15, author = ctx.message.author, channel = channel)
                userchoice = answer.content.lower()
                if userchoice == "dawae":
                    memes.remove(dawae)
                elif userchoice == "harambe":
                    memes.remove(harambe)
                elif userchoice == "doge":
                    memes.remove(doge)
                for item in memes:
                    await self.bot.send_message(channel, embed = item)
                await self.bot.send_message(channel, "Alrighty! Now it's <@!" + user.id + "> turn!(Just type the name. No need for /.")
                secondanswer = await self.bot.wait_for_message(timeout = 15, author = user, channel = channel)
                victimchoice = secondanswer.content.lower()
                await self.bot.send_message(channel, "Shuffling dead memes...")
                choices = ["dawae", "harambe", "doge"]
                while userpoint == victimpoint:
                    for item in choices:
                        temp = random.choice(choices)
                        await self.bot.send_message(channel, "I drew a: {}".format(temp))
                        if temp == userchoice:
                            userpoint += 1
                        elif temp == victimchoice:
                            victimpoint += 1
                    if userpoint == victimpoint:
                        await self.bot.send_message(channel, "No one won. I'll draw again!")
                        userpoint = 0
                        victimpoint = 0
                if userpoint > victimpoint:
                    await self.bot.send_message(channel, "{} wins with {} points!".format(ctx.message.author.name, userpoint))
                    self.add_money(users, ctx.message.author, amount)
                    self.subtract_money(users, user, amount)
                    await self.bot.send_message(channel, "{} now has {} {}, while {} has {} {}".format(ctx.message.author.name, users[ctx.message.author.id]['balance'], self.currency_type,user.name, users[user.id]['balance'], self.currency_type))
                else:
                    await self.bot.send_message(channel, "{} wins with {} points!".format(user.name, victimpoint))
                    self.add_money(users, user, amount)
                    self.subtract_money(users, ctx.message.author, amount)
                    await self.bot.send_message(channel, "{} now has {} {}, while {} has {} {}".format(user.name, users[user.id]['balance'], self.currency_type, ctx.message.author.name, users[ctx.message.author.id]['balance'], self.currency_type))
            else:
                await self.bot.send_message(channel, "The bet is off.")
            with open('users.json', 'w') as f:
                json.dump(users, f)
                
                

                    




    
    def add_money(self, users, user, money):
        users[user.id]['balance'] += money

    def subtract_money(self, users, user, money):
        users[user.id]['balance'] -= money

    #def level_up(self, users, user, channel):
        #experience = users[user.id]['experience']
        #lvl_start = users[user.id]['level']
        #lvl_end = int(experience ** (1/4))

        #if lvl_start < lvl_end:
            #await self.client.send_message(channel, '{} has leveled up to level {}'.format(user.mention, lvl_end))
            #users[user.id]['level'] = lvl_end

def setup(client):
    client.add_cog(economy(client))