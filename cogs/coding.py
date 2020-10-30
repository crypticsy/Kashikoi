import discord
import io, os, sys
import requests 
import urllib.parse
import urllib.request

from contextlib import redirect_stdout
from discord.ext import commands
from os import error



pastebin_key = os.environ['PASTE_KEY']
cg_developer_id = os.environ['CG_DEV_ID']



class Coding(commands.Cog):

    pastebin_key = None
    cg_developer_id = None
    invalid_message = "--- Invalid input detected ---"



    def __init__(self, bot,PASTEBIN_KEY, CG_DEV_ID):
        self.bot = bot
        self.pastebin_key = PASTEBIN_KEY
        self.cg_developer_id = CG_DEV_ID
    
 

    def generate_emb(self, title, description):
        return discord.Embed(title=title, description=description, colour = 0xEDB91D)
        


    def pastebin_link_generator(self, PASTEBIN_KEY, title, content):  # used for posting a new paste
        pastebin_vars = dict(
            api_option='paste',
            api_dev_key= PASTEBIN_KEY,
            api_paste_name=title,
            api_paste_code=content,
            api_paste_expire_date = '1D'
        )
        return urllib.request.urlopen( 'https://pastebin.com/api/api_post.php' , urllib.parse.urlencode(pastebin_vars).encode('utf8')).read()



    def execute_python(self, message, name):
        try:
            if message == "sucks" or message == "suck": return "No you suck @"+name+" 😛"
            elif message == "fuck you" or message == "fu" or message == "f u": return "😒\t https://www.amishrakefight.org/gfy/"
            elif "input()" in message: return "Oops! I can't take inputs yet."

            f = io.StringIO()
            with redirect_stdout(f):
                eval(message)

            return f.getvalue()
            
        except:
            return "Oops! An error occured in my Python circuits."


    
    def generate_CG_profile(self, dev_id, name):
        try:
            data = requests.post('https://www.codingame.com/services/Leaderboards/getGlobalLeaderboard',
                    json = [1,"GENERAL",{"keyword":name,"active":True,"column":"KEYWORD","filter":name},dev_id,True,"global"]
                ).json()['users'][0]
        except:
            raise error

        emb = discord.Embed(title=str(data['pseudo']), description="CodinGame Profile", colour = 0xEDB91D)
        emb.add_field(name = 'Rank', value = str(int(data['rank'])),inline=True)
        emb.add_field(name = 'CodingPoints', value = str(int(data['score'])),inline=True)
        emb.add_field(name = 'Achievements', value = str(int(data['achievements'])),inline=True)
        emb.add_field(name = 'Level', value = str(int(data['codingamer']['level'])),inline=True)
        emb.add_field(name = 'Country', value = data['codingamer']['countryId'],inline=True)
        emb.add_field(name = 'Category', value = data['codingamer']['category'],inline=True)
        emb.add_field(name = 'Profile', value = f"https://www.codingame.com/profile/{data['codingamer']['publicHandle']}",inline=False)

        return emb






    @commands.command(brief="Displays CodinGame profile", description = "Provides a detailed description about the username from CodinGame.com")
    async def codingame(self,ctx, *args):
        wait_message = await ctx.send(embed=self.generate_emb("","Processing CG Profile"))
        try:
            output = self.generate_CG_profile(self.cg_developer_id, ''.join(args))
        except:
            output = self.generate_emb("", "Profile doesn't exist yet")

        await wait_message.delete()
        await ctx.send(embed=output)



    @commands.command(brief="Generates pastebin url", description = "Automatically extracts code and returns a pastebin url having 10m timer for the paste.")
    async def pastebin(self, ctx, *, message):
        await ctx.message.delete()
        pastebin_link = str(self.pastebin_link_generator(self.pastebin_key, "kashikoi", message))
        print(pastebin_link)
        await ctx.send(pastebin_link [2:-1])

        
    
    @commands.command(brief="Execute python script", description = "Executes a python script and returns the Stdout values.")
    async def python(self,ctx, *, message):
        try:
            await ctx.send(embed=self.generate_emb("Output",self.execute_python(message, ctx.message.author.name)))
        except:
            await ctx.send(embed=self.generate_emb("", self.invalid_message))






def setup(bot):
    bot.add_cog(Coding(bot, pastebin_key, cg_developer_id))