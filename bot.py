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

extensions = ['economy', 'test', 'music', 'mafia']
players = {}
currency_type = "<:wood:478383029891498006>"
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

@bot.command(pass_context = True)
async def send(ctx, user : discord.Member):
    await bot.send_message(user, "Don't you dare question my randomness! Type /meme to see for yourself.")
    print("Sent!")
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
async def pfp(ctx, user: discord.Member):
    embed = discord.Embed(title = "{}'s profile picture".format(user.name), colour = discord.Colour.red())
    embed.set_image(url = user.avatar_url)
    embed.set_author(name = "Ghoulbot", icon_url = "https://cdn.discordapp.com/avatars/467177408164921345/cfc1fb121a927ad86af081258a2dd715.webp?size=1024")
    await bot.say(embed = embed)


@bot.command(pass_context = True)
async def meme(ctx):
    memes = ["https://www.happybirthdaycake2015.com/wp-content/uploads/2017/06/Yeahnofuninpostingthingsthatonlyacouple_d805e168786492413db55fa638b2e53f-min.jpg", 
    "https://memegenerator.net/img/instances/49289201.jpg", "https://i.imgflip.com/256b8v.jpg", "https://i.redditmedia.com/AMPuQykI24ov_0WNA7dpO2R-tkFNUDIESl0jXfcJNMU.jpg?fit=crop&crop=faces%2Centropy&arh=2&w=640&s=65895f4af218ab466c655eb57343f786",
    "https://i.redditmedia.com/7dglmuE019cCQ72KW6n1tNHA9XeK-UWLxgBHm1V9kmU.jpg?fit=crop&crop=faces%2Centropy&arh=2&w=640&s=a9cae8ef1d1e2698db0ebff816ecc753", "https://i.redd.it/u4xlofoem5f11.jpg",
    "https://i.redd.it/m09g4wt8u8e11.jpg", "https://i.redd.it/2xnvnwcir3d11.jpg", "https://i.redd.it/tlubfe0w7ti11.jpg", "https://i.redditmedia.com/FYkUQlKnWfnoBbqteq7OaVnberfInkXZWyKcjEeFvS0.jpg?s=058fda9c5d810a633a5a637f7dccdbc4", "https://i.redd.it/r42y3osjla811.jpg",
    "https://i.redditmedia.com/rkrfvVfNc7ZIN6oGVseDwhAIRAYhW-WHchj0r10KMU4.jpg?fit=crop&crop=faces%2Centropy&arh=2&w=640&s=fcef99b16e084726aa7497e33f80d976", 
    "https://i.redditmedia.com/94FuzvGmoJ9h0CfTRYzMVOmoEXny4ZVv7YD0qxQLJZg.jpg?s=c1f32a89c16aa47cc34bfa5c9886566e", "https://i.redd.it/z65636v2av011.jpg",
    "https://i.redd.it/myj047rr74911.jpg", "https://i.redditmedia.com/U0bUinXrLPslufgq5ZtLWIoeK3ktkksJhTdPEsyYZhQ.png?fit=crop&crop=faces%2Centropy&arh=2&w=640&s=f385985d5627537711ef40570038ff28", "https://i.redditmedia.com/dMrwTjgVImKI0zMx-QAuYcrMp8nI-zP1QIM0TnI1B1Q.jpg?fit=crop&crop=faces%2Centropy&arh=2&w=640&s=c882d430ac8283ed89d3537644d0b364",
     "https://i.redditmedia.com/fvB-VWtZsCmBa2WO4hKx6bfzGRZzl9c5hflhbgvaGKI.jpg?s=d403dc5fe8c0ccefef4b6db9eadb829e", "http://memecrunch.com/meme/BI6WW/calc-memes/image.jpg", "https://i.imgur.com/UWbVzuZ.jpg",
     "https://i.imgur.com/63WHqcc.jpg"]
    thing = random.choice(memes)
    embed = discord.Embed(title = "Meme generator", colour = discord.Colour.blue())
    embed.set_image(url = thing)
    await bot.say(embed = embed)
@bot.command(pass_context = True)
async def test(ctx):
    channel = ctx.message.channel
    await bot.send_file(channel, os.getcwd() + r'\LinkCharacters\Assasin.png')

@bot.command(pass_context = True)
async def rank(ctx):
    with open('users.json', 'r') as f1:
        users = json.load(f1)
    first = 0
    firstid = ""
    second = 0
    secondid = ""
    third = 0
    thirdid = ""
    temp = []
    for item in users:
        temp.append(users[item]['balance'])
        
    first = search(temp, users)
    for item in users:
        if users[item]['balance'] == first:
            firstid = item
            break
    temp.remove(first)

    second = search(temp, users)
    for item in users:
        if users[item]['balance'] == second:
            secondid = item
            break
    temp.remove(second)

    third = search(temp, users)
    for item in users:
        if users[item]['balance'] == third:
            thirdid = item
            break
    temp.remove(third)
    server = ctx.message.server
    firstName = server.get_member(firstid).name
    secondName = server.get_member(secondid).name
    thirdName = server.get_member(thirdid).name
    display1 = discord.Embed(title = "Ranking", colour = discord.Colour.green())
    display1.add_field(name = "#1: {}".format(firstName), value = "{} {}".format(first, currency_type), inline = False)
    display1.add_field(name = "#2: {}".format(secondName), value = "{} {}".format(second, currency_type), inline = False)
    display1.add_field(name = "#3: {}".format(thirdName), value = "{} {}".format(third, currency_type), inline = False)
    display1.set_thumbnail(url = "https://poetsandquants.com/wp-content/uploads/2017/11/Rankingillo.jpeg")
    await bot.send_message(ctx.message.channel, embed = display1)
    
def search(listT, users): #returns highest wealth with user's id
    bigNum = 0
    for item in listT:
        if item > bigNum:
            bigNum = item
    return bigNum
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
    embed.add_field(name="/rank", value = "Displays the top three richest people in the discord")
    embed.add_field(name="/bet @person #", value = "Challenges a person to a bet. Winner takes the amount from the loser.")
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

            if(extension == "mafia"):
                bot.load_extension(f"MAFIA.{extension}")
            else:
                bot.load_extension(extension)
        except Exception as error:
            print('{} cannot be loaded because {}'.format(extension, error))
    with open('key.json', 'r') as f:
        keys = json.load(f)
    thing = keys['key']
    bot.run(thing)