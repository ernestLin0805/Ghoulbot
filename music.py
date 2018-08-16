import discord
from discord.ext import commands
import youtube_dl
players = {}
queues = {}
class music:
    def __init__(self, bot):
        self.bot = bot

    def check_queue(self, id):
        if queues[id] != []:
            player = queues[id].pop(0)
            players[id] = player
            player.start()
    @commands.command(pass_context = True)
    async def join(self, ctx):
        channel = ctx.message.author.voice.voice_channel
        await self.bot.join_voice_channel(channel)
    
    @commands.command(pass_context=True)
    async def leave(self, ctx):
        server = ctx.message.server
        voice_client = self.bot.voice_client_in(server)
        await voice_client.disconnect()

    @commands.command(pass_context=True)
    async def play(self, ctx, url):
        self.bot.send_message(ctx.message.channel, "Loading...")
        server = ctx.message.server
        voice_client = self.bot.voice_client_in(server)
        player = await voice_client.create_ytdl_player(url, after = lambda: self.check_queue(server.id))
        players[server.id] = player
        player.start()

    @commands.command(pass_context=True)
    async def pause(self, ctx):
        id = ctx.message.server.id
        players[id].pause()

    @commands.command(pass_context=True)
    async def stop(self, ctx):
        id = ctx.message.server.id
        players[id].stop()

    @commands.command(pass_context=True)
    async def resume(self, ctx):
        id = ctx.message.server.id
        players[id].resume()

    @commands.command(pass_context=True)
    async def helpMusic(self, ctx):
        embed = discord.Embed(title="Music Commands: ", description = "", colour = discord.Colour.blue())
        embed.add_field(name="/join", value="Adds Ghoulbot into your current connected voice channel(You must be in a voice channel)", inline = True)
        embed.add_field(name="/play *youtube_url*", value="Plays music from url. *Must be in voice channel.", inline = True)
        embed.add_field(name="/pause", value = "Pauses current playing music.", inline = True)
        embed.add_field(name = "/resume", value = "Resumes paused music.", inline = True)
        embed.add_field(name = "/stop", value = "Stops current music completely.")
        embed.add_field(name = "/stop *youtube_url*", value = "Queues the youtube video.")
        embed.set_thumbnail(url = "https://yt3.ggpht.com/OgVV66t5vou1LkAbPh7yHbJA73Z2kKHs6-mFaeVFjnlU-pWESAPXFi-5pMASF7Mp1YLfoMdeI38v68U=s900-mo-c-c0xffffffff-rj-k-no")
        await self.bot.send_message(ctx.message.channel, embed = embed)

    @commands.command(pass_context=True)
    async def queue(self, ctx, url):
        server = ctx.message.server
        voice_client = self.bot.voice_client_in(server)
        player = await voice_client.create_ytdl_player(url)

        if server.id in queues:
            queues[server.id].append(player)
        else:
            queues[server.id] = [player]
        await self.bot.send_message(ctx.message.channel, "Video queued.")
def setup(client):
    client.add_cog(music(client))