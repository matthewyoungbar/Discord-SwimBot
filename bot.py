import requests
import urllib.parse
from discord.ext import commands

TOKEN = open("token.txt").read().strip()

bot = commands.Bot(command_prefix='!')

@bot.command()
async def ping(ctx):
    await ctx.send('pong!')

@bot.command()
async def collegeswimming(ctx, *args):
    base = 'https://www.collegeswimming.com'
    url = base + '/api/search/?q=' + urllib.parse.quote(' '.join(args))
    results = [obj for obj in requests.get(url).json() if 'swimmer' in obj['id']]
    if len(results) == 1:
        await ctx.send(base + results[0]['url'])
    elif len(results) > 1:
        swimmers = ""
        for swimmer in results:
            swimmers += f"{swimmer['name']} - "
            if swimmer['team'] != '':
                swimmers += f"{swimmer['team']}, "
            swimmers += f"{swimmer['location']}\n"
        await ctx.send("There were multiple results. Please provide a more specific search.\n```\n" + swimmers + '```')
    elif len(results) == 0:
        await ctx.send("There were no results. Either your search is too broard or too narrow.")

@bot.command()
async def cs(ctx, *args):
    await collegeswimming(ctx, *args)

bot.run(TOKEN)
