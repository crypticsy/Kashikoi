import discord
from jikanpy import Jikan
from discord.ext import commands
from datetime import date
import calendar
import random



class MyAnimeList(commands.Cog):
    jikan = Jikan()
    anime_genre = { "action" : 1, "adventure" : 2, "cars" : 3, "comedy" : 4, 
                    "dementia" : 5, "demons" : 6, "mystery" : 7, "drama" : 8,
                    "ecchi" : 9, "fantasy" : 10, "game" : 11, "hentai" : 12,
                    "historical" : 13, "horror" : 14, "kids" : 15, "magic" : 16,
                    "martialarts" : 17, "mecha" : 18, "music" : 19, "parody" : 20,
                    "samurai" : 21, "romance" : 22, "school" : 23, "scifi" : 24,
                    "shoujo" : 25, "shoujoai" : 26, "shounen" : 27, "shounenai" : 28,
                    "space" : 29, "sports" : 30, "superpower" : 31, "vampire" : 32,
                    "yaoi": 33, "yuri" : 34, "harem" : 35, "sliceOflife" : 36,
                    "supernatural" : 37, "military" : 38, "police" : 39, "psychological" : 40,
                    "thriller" : 41, "seinen" : 42, "josei": 43 }



    def __init__(self, bot):
        self.bot = bot


    def myAnimeListGenerator(self, command):
        try:
            if command in {"upcoming","airing"}:
                top_anime = self.jikan.top(type='anime', page=1, subtype=command)
                newList =  "        --- Top 20 %s anime ---\n" %(command)
                for n,i in enumerate(top_anime['top'][:20]):
                    newList += "%d :  %s\n" %(n+1, i['title'])
                return "```"+newList+"```"

            elif command == "today":
                curday = calendar.day_name[date.today().weekday()].lower()
                today = self.jikan.schedule(day = curday)
                newList =  "        --- Today's anime updates include ---\n"
                for n,i in enumerate(today[curday]):
                    newList += "%d :  %s\n" %(n+1, i['title'])
                return "```"+newList+"```"

        except:
            return "```Oops! An error occured in my circuits.```"




    def recommendme(self, message):
        try:
            if message.lower() in self.anime_genre:
                data = self.jikan.genre( type = 'anime', genre_id = self.anime_genre[message.lower()] )
                recommendation = data['anime'][random.randint(0,len(data['anime'])-1)]
                newlist = "Here's an anime that might interest you ;)\n\nName : " + recommendation['title'] + "\nNo. of Episodes : " + str(recommendation['episodes']) + "\n\nSynopsis : "+ recommendation['synopsis']
            
            else:
                if message.lower() == "help":newlist = ""
                else: newlist = "I couldn't understand you.\n\n"
                newlist += "Here's a list of genre's that I know of: \n" +' - '.join(self.anime_genre.keys())

            return "```"+newlist+"```"
        
        except:
            return "```Oops! An error occured in my circuits.```"




    @commands.command(brief="Returns top 20 airing anime", description = "A command that extracts the recent anime list from MyAnimeList and dispalys the top 20 airing animes from the list.")
    async def airing(self,ctx):
        await ctx.message.delete()
        await ctx.send(self.myAnimeListGenerator("airing"))


    @commands.command(brief="Returns top 20 upcoming anime", description = "A command that extracts the recent anime list from MyAnimeList and dispalys the top 20 upcoming animes from the list.")
    async def upcoming(self,ctx):
        await ctx.message.delete()
        await ctx.send(self.myAnimeListGenerator("upcoming"))


    @commands.command(brief="Returns anime whose episodes are scheduled to air today", description = "A command that extracts and dispalys the anime whose episodes are scheduled to be aired today from MyAnimeList.")
    async def today(self,ctx):
        await ctx.message.delete()
        await ctx.send(self.myAnimeListGenerator("today"))


    @commands.command(brief="Recommends an anime for a given genre", description = "A command that extracts and displays the details of a random anime for a given genre from MyAnimeList.")
    async def recommend(self,ctx, *args):
        await ctx.send(self.recommendme(''.join(args)))




def setup(bot):
    bot.add_cog(MyAnimeList(bot))