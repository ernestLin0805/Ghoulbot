import discord
from discord.ext import commands
import asyncio
import json
import os
import chalk
import random
import youtube_dl

bot = commands.Bot(command_prefix='/')
bot.remove_command('help')

extensions = ['economy', 'test', 'music', 'rpg']
players = {}

@bot.event
async def on_ready():
    print("I'm in")


@bot.command(pass_context=True)
async def kick(ctx, user: discord.Member):
    if user.top_role.id == "394313823244255242":#That's the owner
        await ctx.bot.say("Nice try, {}, but you can't kick the owner.".format(ctx.message.author.name))
    elif ctx.message.author.server_permissions.administrator == True and ctx.message.author.top_role.id != user.top_role.id:#Checks if the kicker has the same role as the victim and if he/she has permission
        embed = discord.Embed(title="{} has been kicked from the server by {}!".format(user.name, ctx.message.author.name))
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.bot.say(embed=embed)
    else:
        await ctx.bot.say("Sorry. You don't have the permission to kick {}".format(user.name))

@bot.command(pass_context=True)
async def clear(ctx, amount=100):
    if ctx.message.author.server_permissions.administrator == True:
        try:
            channel = ctx.message.channel
            messages = []
            async for message in bot.logs_from(channel, limit=int(amount+1)):
                messages.append(message)
            await bot.delete_messages(messages)
            await bot.say("Messages deleted.")
        except Exception as error:
            await bot.say("{}".format(error))
    else:
        await bot.say("You don't have permission.")

@bot.command(pass_context = True)
async def test(ctx):
    channel = ctx.message.channel
    await bot.send_file(channel, os.getcwd() + r'\LinkCharacters\Assasin.png')

@bot.event
async def on_message_delete(message):
    try:
        fmt = '{0.author.name} has deleted the message:\n"{0.content}" \nfrom {0.channel}'
        await bot.send_message(discord.Object(id='467451291980005376'), fmt.format(message))
    except Exception as error:
        await bot.say("{}".format(error))


@bot.event
async def on_member_remove(member):
    await bot.say("{} has left the discord".format(member.name))

@bot.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(
        colour = discord.Colour.orange()
    )

    embed.set_author(name="Help")
    embed.add_field(name="/info", value="Reveals info about a specific user(mention the person after the command)", inline = True)
    embed.add_field(name="/kick", value = "Kicks a designated person(mention after command). You must have permission.")
    embed.add_field(name="/clear #", value = "Clears a certain number of messages.")
    embed.add_field(name="/registerBank", value = "Register into the bank database.")
    embed.add_field(name="/balance", value = "Checks your current balance.")
    embed.add_field(name="/gambleEasy #", value = "Gambles a certain amount with a 40 percent chance to win. If you win you get win 3/2 of your bet.")
    embed.add_field(name="/gambleMedium #", value = "Gambles a certain amount with a 20 percent chance to win. If you win you get win double of your bet.")
    embed.add_field(name="/gambleHard #", value = "Gambles a certain amount with a 10 percent chance to win. If you win you get win triple of your bet.")
    embed.add_field(name="/gambleInsane #", value = "Gambles a certain amount with a 1 percent chance to win. If you win you get win ten times of your bet amount.")
    embed.add_field(name="/helpMusic", value = "Displays commands for music bot")
    embed.add_field(name="/register", value = "Register into the rpg database.")
    await bot.say(embed=embed)

if __name__ == '__main__':
    for extension in extensions:
        try:
            if(extension == 'rpg'):
                bot.load_extension(f"RPG.{extension}")
            else:
                bot.load_extension(extension)
        except Exception as error:
            print('{} cannot be loaded because {}'.format(extension, error))
    with open('key.json', 'r') as f:
        keys = json.load(f)
    thing = keys['key']
    bot.run(thing)