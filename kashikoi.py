import sys, os, re, requests
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


def is_website(i):
    try:
        val = requests.get("https://"+i)
        return val.status_code < 400
    except:
        return False

@kashikoi.event
async def on_message(message): 
    curmes  = str(message.content)
    links = []
    pattern = r"\w+\.[a-zA-Z]+$"
    for i in curmes.lower().split():
        if re.search(r"^http",i) == None and re.search(pattern, i) != None:
            links += re.findall(pattern, i)

    if not message.author.bot and len(links) != 0:
        await message.channel.send('\t'.join(["https://"+x for x in links if is_website(x)]))

    await kashikoi.process_commands(message)
    
    


kashikoi.run(token)