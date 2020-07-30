import pandas
import requests
import urllib.parse
import os
from discord.ext import commands

TOKEN = os.environ.get("SWIMBOT_TOKEN")
records = pandas.read_csv('records.csv', quotechar="'")
bot = commands.Bot(command_prefix='!')

stroke_shortnames = {
    'Butterfly': ['fly', 'fl'],
    'Backstroke': ['back', 'bk'],
    'Breaststroke': ['breastroke', 'breast', 'br'],
    'Freestyle': ['free', 'fr'],
    'IM': ['i.m.', 'individual medley'],
    'Medley Relay': [],
    'Free Relay': ['freestyle relay', 'fr relay']
}

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
        await ctx.send("There were no meaningful results. Either your search is too broard or too narrow.")

@bot.command()
async def cs(ctx, *args):
    await collegeswimming(ctx, *args)

@bot.command()
async def record(ctx, *args):
    if len(args) < 2:
        return

    if args[0].isnumeric():
        distance = args[0]
        stroke = ' '.join(args[1:])
        for strokename, shortnames in stroke_shortnames.items():
            if stroke.lower() == strokename.lower() or stroke.lower() in shortnames:
                stroke = strokename
                results = records[(records['dist'] == distance) & (records['stroke'] == stroke)][['team', 'name', 'time', 'year']]
                await ctx.send('```\n' + results.to_string(index=False) + '```')
                break
        else: # no break, so invalid stroke name
            await ctx.send('Invalid event.')
    else:
        first, last = args
        results = records[records['name'].str.contains(last)][['dist', 'stroke', 'time', 'year']]
        if len(results) == 0:
            await ctx.send('Name not found.')
        else:
            await ctx.send('```\n' + results.to_string(index=False) + '```')

bot.run(TOKEN)
