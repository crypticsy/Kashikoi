import discord, os
import urllib.parse
import urllib.request
import requests
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



    @commands.command(brief="Generates pastebin url", description = "Automatically extracts code and returns a pastebin url having 10m timer for the paste.")
    async def pastebin(self, ctx, *, message):
        await ctx.message.delete()
        pastebin_link = str(self.pastebin_link_generator(self.pastebin_key, "kashikoi", message))
        await ctx.send(pastebin_link [2:-1])



def setup(bot):
    bot.add_cog(Coding(bot, pastebin_key))