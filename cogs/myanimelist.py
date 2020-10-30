import calendar
import discord
import random

from jikanpy import Jikan
from discord.ext import commands
from datetime import date



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
    
 

    def generate_emb(self, title, description):
        return discord.Embed(title=title, description=description, colour = 0x36D2D2)



    def myAnimeListGenerator(self, command):
        try:
            newList, animelist = "", []
            check = {"upcoming","airing"}

            if command in check:
                animelist = self.jikan.top(type='anime', page=1, subtype=command)['top'][:20]
                
            elif command == "today":
                curday = calendar.day_name[date.today().weekday()].lower()
                animelist = self.jikan.schedule(day = curday)[curday]

            title =  f" Top 20 {command} Anime " if command in check else " Todays anime updates include "
            for n,i in enumerate(animelist):
                newList += str(n+1).rjust(len(str(len(animelist))),"-") + f" : {i['title']}\n"

            return self.generate_emb(title, newList)        

        except:
            return self.generate_emb("","Oops! An error occured in MyAnimeList circuits.")



    def recommendme(self, message):
        try:
            title = ""
            if message.lower() in self.anime_genre:
                data = self.jikan.genre( type = 'anime', genre_id = self.anime_genre[message.lower()] )
                recommendation = data['anime'][random.randint(0,len(data['anime'])-1)]
                title = "Here's an anime that might interest you ;)"
                
                emb =  discord.Embed(title=title, colour = 0x36D2D2)
                emb.add_field(name = 'Name', value = recommendation['title'], inline=False)
                emb.add_field(name = 'No. of Episodes', value = str(recommendation['episodes']), inline=False)
                synopsis = recommendation['synopsis'] if len(recommendation['synopsis']) < 1024 else recommendation['synopsis'][:1021]+"..."
                emb.add_field(name = 'Synopsis', value = synopsis, inline=False)

                return emb
            
            else:
                if message.lower() == "help": title = ""
                else: title = "I couldn't understand you."
                newlist = "Here's a list of genre's that I know of: \n\n" +' - '.join(self.anime_genre.keys())
                return self.generate_emb(title, newlist)
        
        except:
            return self.generate_emb("", "Oops! An error occured in MyAnimeList circuits.")






    @commands.command(brief="Returns top 20 airing anime", description = "A command that extracts the recent anime list from MyAnimeList and dispalys the top 20 airing animes from the list.")
    async def airing(self,ctx):
        await ctx.message.delete()
        await ctx.send(embed=self.myAnimeListGenerator("airing"))



    @commands.command(brief="Returns top 20 upcoming anime", description = "A command that extracts the recent anime list from MyAnimeList and dispalys the top 20 upcoming animes from the list.")
    async def upcoming(self,ctx):
        await ctx.message.delete()
        await ctx.send(embed=self.myAnimeListGenerator("upcoming"))



    @commands.command(brief="Returns anime scheduled to air episodes today", description = "A command that extracts and dispalys the anime whose episodes are scheduled to be aired today according to MyAnimeList.")
    async def today(self,ctx):
        await ctx.message.delete()
        await ctx.send(embed=self.myAnimeListGenerator("today"))


    @commands.command(brief="Recommends an anime for a given genre", description = "A command that extracts and displays the details of a random anime for a given genre from MyAnimeList.")
    async def recommend(self,ctx, *args):
        await ctx.send(embed=self.recommendme(''.join(args)))




def setup(bot):
    bot.add_cog(MyAnimeList(bot))