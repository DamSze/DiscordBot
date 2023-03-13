import requests
import discord
import random
from discord.ext import commands
from discord.ext.commands import parameter as param

class Pokemon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="info about pokemon", help='Information about pokemons, e.g hp, moves, type \n\n'
                                                 'Usage: !pokemon [name]')
    async def pokemon(self, ctx, name: str = param(default=None, description='(optional): name of pokemon to be searched')):
        if name is None:
            name = random.randint(0, 898)
        else:
            name = name.lower()
        poke_info = requests.get('https://pokeapi.co/api/v2/pokemon/'+str(name))
        poke_info = poke_info.json()
        if name is not str:
            name = poke_info['forms'][0]['name']


        thumbnail = poke_info['sprites']['front_default']
        height = self.getHeight(poke_info)
        weight = self.getWeight(poke_info)
        type = self.getTypes(poke_info)
        ability = self.getAbb(poke_info)
        stats = self.getStats(poke_info)
        moves = self.getMoves(poke_info)

        embed = discord.Embed(title=name.capitalize(), color=discord.Color.green())
        embed.add_field(name='Height', value=height)
        embed.add_field(name='Weight', value=weight)
        embed.add_field(name='Type', value=type)
        embed.add_field(name='Abilities', value=ability)
        embed.add_field(name='Stats', value=stats)
        embed.add_field(name=f"Moves[{moves['moves_num']}]", value=moves['moves'])
        embed.set_thumbnail(url=thumbnail)
        await ctx.send(embed=embed)

    @pokemon.error
    async def pokemon_error(self, ctx, error):
        embed = discord.Embed(description='❌POKEMON NOT FOUND❌', color=discord.Color.red())
        await ctx.send(embed=embed)

    def getTypes(self, poke_info):
        types = [type['type']['name'] for type in poke_info['types']]
        type_str = ''
        for type in types:
            type_str += type + ',\n'
        return type_str[:-2]

    def getHeight(self, poke_info):
        height_cm = poke_info['height'] * 10
        height = str(height_cm) + ' cm' if not height_cm > 1000 else str(height_cm / 1000) + ' m'
        return height

    def getWeight(self, poke_info):
        weight_g = poke_info['weight'] * 100
        weight = str(weight_g) + ' g' if not weight_g > 1000 else str(weight_g / 1000) + ' kg'
        return weight

    def getAbb(self, poke_info):
        abilities = poke_info['abilities']
        abilities_str = ''
        for ability in abilities:
            abilities_str += ability['ability']['name'] + ',\n'
        return abilities_str[:-2]

    def getStats(self, poke_info):
        stats = poke_info['stats']
        stats_str = ''
        for stat in stats:
            name = stat['stat']['name']
            val = stat['base_stat']
            stats_str += f'{name.capitalize()}[{val}], '
        return stats_str

    def getMoves(self, poke_info):
        moves = poke_info['moves']
        moves_str = ''
        for i in range(0,5):
            name = moves[i]['move']['name']
            moves_str += f'{name.capitalize()}, '
        dict_stat = {'moves_num': str(len(moves)), 'moves': moves_str}
        return dict_stat






async def setup(bot):
    await bot.add_cog(Pokemon(bot))
