import discord
from discord.ext import commands
import json
import os


class test:
    def __init__(self, bot):
        self.bot = bot

    #async def on_message_delete(self, message):
        #await self.bot.send_message(message.channel, "{} is deleted from {}".format(message, message.channel))
    

    @commands.command(pass_context=True)
    async def info(self, ctx, user: discord.Member):
        with open ('stats.json', 'r') as f:
            stats = json.load(f)
        id = user.id
        embed = discord.Embed(title="{}'s info".format(user.name), description = "Here's what I could find.", color=0xff00)
        embed.add_field(name="Name", value=user.name, inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Status", value=user.status, inline=True)
        embed.add_field(name="Highest Role", value=user.top_role, inline=True)
        embed.add_field(name="Joined", value=user.joined_at, inline=True)
        embed.set_thumbnail(url=user.avatar_url)
        await self.bot.send_message(ctx.message.channel, embed=embed)
        if id in stats:
            character = discord.Embed(title = "Class: {}".format(stats[id]['Class']), description = "", colour = discord.Colour.blue())
            character.add_field(name = "Attack: ", value = "{}".format(stats[id]['Attack']))
            character.add_field(name = "Health: ", value = "{}".format(stats[id]['Health']))
            character.add_field(name = "Speed: ", value = "{}".format(stats[id]['Speed']))
            character.set_image(url = stats[id]["Picture"])
            await self.bot.send_message(ctx.message.channel, embed=character)
def setup(bot):
    bot.add_cog(test(bot))