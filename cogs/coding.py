import discord
import io, sys, os
import requests 
import urllib.parse
import urllib.request
from contextlib import redirect_stdout
from discord.ext import commands


pastebin_key = os.environ['PASTE_KEY']



class Coding(commands.Cog):
    pastebin_key = -1

    def __init__(self, bot,PASTEBIN_KEY):
        self.bot = bot
        self.pastebin_key = PASTEBIN_KEY

    def pastebin_link_generator(self, PASTEBIN_KEY, title, content):  # used for posting a new paste
        pastebin_vars = dict(
            api_option='paste',
            api_dev_key= PASTEBIN_KEY,
            api_paste_name=title,
            api_paste_code=content,
            api_paste_expire_date = '10M'
        )
        return urllib.request.urlopen( 'http://pastebin.com/api/api_post.php' , urllib.parse.urlencode(pastebin_vars).encode('utf8')).read()

    def execute_python(self, message, name):
        try:
            if message == "sucks" or message == "suck": 
                return "```No you suck @"+name+" 😛```"
            elif message == "fuck you" or message == "fu" or message == "f u": 
                return "😒 https://www.amishrakefight.org/gfy/"
            elif "input()" in message:
                return "```Oops! I can't take inputs yet.```"

            f = io.StringIO()
            with redirect_stdout(f):
                eval(message)

            return "---------------------------------\n"+f.getvalue()+"---------------------------------"
            
        except:
            return "```Oops! An error occured in my circuits.```"
        



    @commands.command(brief="Generates pastebin url", description = "Automatically extracts code and returns a pastebin url having 10m timer for the paste.")
    async def pastebin(self, ctx, *, message):
        await ctx.message.delete()
        pastebin_link = str(self.pastebin_link_generator(self.pastebin_key, "kashikoi", message))
        await ctx.send(pastebin_link [2:-1])

    
    @commands.command(brief="Execute python script", description = "Executes a python script and returns the Stdout values.")
    async def python(self,ctx, *, message):
        try:
            await ctx.send(self.execute_python(message, ctx.message.author.name))
        except:
            await ctx.send("```--- Invalid input detected ---```")



def setup(bot):
    bot.add_cog(Coding(bot, pastebin_key))