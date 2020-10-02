import sys,os
import discord
from discord.ext import commands



token = os.environ['BOT_TOKEN']
kashikoi = commands.Bot(command_prefix = "!")



# Load all existing cogs by default
for filename in os.listdir(os.path.join(sys.path[0])+"/cogs"):
    if filename.endswith('.py'):
        kashikoi.load_extension(f'cogs.{filename[:-3]}')






@kashikoi.event
async def on_ready():
    print(f'Logged in as: {kashikoi.user.name}')
    print(f'With ID: {kashikoi.user.id}')
    await kashikoi.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="!help"))


@kashikoi.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name='general')
    if channel is not None:
        await channel.send(f'Hey {member.mention}, Welcome to {member.guild.name}!') #Greet a new member


@kashikoi.event
async def on_message(message): 
    curmes  = str(message.content)
    curmesLower = curmes.lower()

    if not message.author.bot and curmesLower.find(".com") != -1 and curmesLower.find("http") == -1:            # to turn .com message to links
        allwords = curmes.split()
        links = []
        for i in allwords:
            if i.find(".com") != -1:links.append( "https://"+i.replace(",","") )
        await message.channel.send('\t'.join(links))

    await kashikoi.process_commands(message)
    


kashikoi.run(token)