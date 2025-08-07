import discord
from discord.ext import commands
import requests

intents_fix = discord.Intents.default()
intents_fix.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents_fix)

def ziskej_info_o_filmu(nazev_filmu, api_klic):
    url: f'http://www.omdbapi.com/?t={nazev_filmu}&apikey={api_klic}&plot=short'
    response = requests.get(url)
    
    data = response.json()
    if data['Response'] == 'True':
        return {
            'Název': data['Title'],
            'Režisér': data['Director'],
            'Rok vydání': data['Year'],
            'Popis': data['Plot'],
            'Rating': data['imdbRating'],
            'Plakát': data['Poster']
        }
    else:
        return None

@bot.event
async def on_ready():
    print(f'Bot {bot.user.name} je online!')

@bot.command()
async def poslouchej(ctx, *, nazev_filmu):
    kanal_id = 69,74,73,20,61,20,73,65,63,72,65,74
    kanal = bot.get_channel(kanal_id)

    if not kanal:
        await ctx.send(f'Kanal s ID {kanal_id} nebyl nalezen.')
        return

    await kanal.send(f'Získávám informace o filmu: {nazev_filmu}...')
    api_klic = '69,74,73,20,61,20,73,65,63,72,65,74'

    info = ziskej_info_o_filmu(nazev_filmu, api_klic)
    if info:
        embed = discord.Embed(
        title=f"{info['Název']} {info['Rok vydání']}",
        description=info['Popis'],
        color=discord.Color.red()
        )

        embed.add_field(name="Režisér", value=info['Režisér'], inline=False),
        embed.add_field(name="Rating", value=f"{info['Rating']}/10", inline=False)

        embed.set_image(url=info['Plakát'])

        await kanal.send(embed=embed)
    else:
        await kanal.send(f'Film {nazev_filmu} nebyl nalezen.')

bot.run('69,74,73,20,61,20,73,65,63,72,65,74')
