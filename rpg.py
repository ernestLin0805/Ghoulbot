import discord
from discord.ext import commands
import json
import os
os.chdir(r'C:\Users\ernes\OneDrive\Desktop\GhoulbotBeta')


class rpg:

    def __init__(self, bot):
        self.bot = bot
    currency_type = "<:wood:478383029891498006>"

    @commands.command(pass_context = True)
    async def register(self, ctx):
        with open('stats.json', 'r') as f:
            stats = json.load(f)
        id = ctx.message.author.id
        if not id in stats:
            stats[id] = {}
            stats[id]['Class'] = 'Caveman'
            stats[id]['Attack'] = 10
            stats[id]['Health'] = 100
            stats[id]['Speed'] = 5
            stats[id]['Picture'] = r'C:\Users\ernes\OneDrive\Pictures\LinkCharacters\LinkDefault.png'
            embed = discord.Embed(title = "{}".format(ctx.message.author.name), description = 'Class: {}'.format(stats[id]['Class']))
            embed.add_field(name = "Attack: ", value = "{}".format(str(stats[id]['Attack'])))
            embed.add_field(name = "Health: ", value = "{}".format(stats[id]['Health']))
            embed.add_field(name = "Speed: ", value = "{}".format(stats[id]['Speed']))
            await self.bot.send_file(ctx.message.channel, stats[id]['Picture'])
            await self.bot.send_message(ctx.message.channel, embed = embed)
        else:
            await self.bot.send_message(ctx.message.channel, "You are already in the database.")
        with open('stats.json', 'w') as f:
            json.dump(stats, f)
    
    @commands.command(pass_context = True)
    async def shop(self, ctx):
        embed = discord.Embed(title = "Shop", description = "", colour = discord.Colour.blue())
        embed.add_field(name = "Upgrade character class", value = "/upgrade (must have a class bought first)", inline = True)
        embed.add_field(name = "\nBuy character class", value = "/buy *character class*", inline = True)
        embed.add_field(name = "Upgrade discord role", value = "/upRole", inline = True)
        embed.set_image(url = "https://i.imgur.com/NCULLnm.gif")
        await self.bot.send_message(ctx.message.channel, embed = embed)

    @commands.command(pass_context = True)
    async def buy(self, ctx, target):
        with open('stats.json', 'r') as f:
            stats = json.load(f)
        with open('users.json', 'r') as f2:
            users = json.load(f2)
        with open('ClassesInfo.json', 'r') as f3:
            classes = json.load(f3)
        id = ctx.message.author.id
        balance = users[id]['balance']
        if id in stats and balance >= classes[target]['Price']:
            stats[id]["Class"] = target
            stats[id]["Attack"] = classes[target]["Attack"]
            stats[id]["Health"] = classes[target]["Health"]
            stats[id]["Speed"] = classes[target]["Speed"]
            stats[id]["Picture"] = classes[target]["Picture"]
            users[id]["balance"] -= classes[target]["Price"]
        elif not target in classes:
            await self.bot.send_message(ctx.message.channel, "Sorry, that class doesn't exist.(Check your spelling)")
        elif balance < classes[target]["Price"]:
            await self.bot.send_message(ctx.message.channel, "You don't have enough {}! Maybe if the owner is kind enough he can help you...".format(self.currency_type))
        elif not id in stats:
            await self.bot.send_message(ctx.message.channel, "You are not registered in the database. Please type /register first.")
        elif not stats[id]["Class"] == "Caveman":
            await self.bot.send_message("You already have a class.")

        with open('stats.json', 'w') as f:
            json.dump(stats, f)
        with open('users.json', 'w') as f2:
            json.dump(users, f2)

            

def setup(client):
    client.add_cog(rpg(client))