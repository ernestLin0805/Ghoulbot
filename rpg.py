import discord
from discord.ext import commands
import json
import os
os.chdir(r'C:\Users\ernes\OneDrive\Desktop\GhoulbotBeta')


class rpg:

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context = True)
    async def register(self, ctx):
        with open ('stats.json', 'r') as f:
            stats = json.load(f)
        id = ctx.message.author.id
        if not id in stats:
            stats[id] = {}
            stats[id]['Class'] = 'Caveman'
            stats[id]['Attack'] = 10
            stats[id]['Health'] = 100
            stats[id]['Defense'] = 5
            stats[id]['Picture'] = r'C:\Users\ernes\OneDrive\Pictures\LinkCharacters\LinkDefault.png'
            embed = discord.Embed(title = "{}".format(ctx.message.author.name), description = 'Class: {}'.format(stats[id]['Class']))
            embed.add_field(name = "Attack: ", value = "{}".format(str(stats[id]['Attack'])))
            embed.add_field(name = "Health: ", value = "{}".format(stats[id]['Health']))
            embed.add_field(name = "Defense: ", value = "{}".format(stats[id]['Defense']))
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
    async def buy(self, ctx, className):
        

def setup(client):
    client.add_cog(rpg(client))