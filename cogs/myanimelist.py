import discord
from jikanpy import Jikan
from discord.ext import commands
from datetime import date
import calendar



class MyAnimeList(commands.Cog):
    jikan = Jikan()



    def __init__(self, bot):
        self.bot = bot

    def myAnimeListGenerator(self, command):
        if command in {"upcoming","airing"}:
            top_anime = self.jikan.top(type='anime', page=1, subtype=command)
            newList =  "        ---Top 20 %s anime---\n" %(command)
            for n,i in enumerate(top_anime['top'][:20]):
                newList += "%d :  %s\n" %(n+1, i['title'])
            return "```"+newList+"```"

        elif command == "today":
            curday = calendar.day_name[date.today().weekday()].lower()
            monday = self.jikan.schedule(day = curday)
            newList =  "        --- Today's anime updates include ---\n"
            for n,i in enumerate(monday[curday]):
                newList += "%d :  %s\n" %(n+1, i['title'])
            return "```"+newList+"```"




    


    @commands.command(brief="Returns top 20 upcoming anime", description = "A command that extracts data from MyAnimeList and dispalys the top 20 upcoming anime.")
    async def upcoming(self,ctx):
        await ctx.message.delete()
        await ctx.send(self.myAnimeListGenerator("upcoming"))


    @commands.command(brief="Returns top 20 airing anime", description = "A command that extracts data from MyAnimeList and dispalys the top 20 airing anime.")
    async def airing(self,ctx):
        await ctx.message.delete()
        await ctx.send(self.myAnimeListGenerator("airing"))


    @commands.command(brief="Returns all anime airing today", description = "A command that extracts and dispalys the anime scheduled to be aired today from MyAnimeList.")
    async def today(self,ctx):
        await ctx.message.delete()
        await ctx.send(self.myAnimeListGenerator("today"))




def setup(bot):
    bot.add_cog(MyAnimeList(bot))