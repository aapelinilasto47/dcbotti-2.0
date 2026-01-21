import discord
from discord.ext import commands
from discord import app_commands
import random

with open("data/lolchamp.txt", "r") as f:
    lol_champions = [line.strip() for line in f]

class UtilityCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='coinflip')
    async def coinflip(self, interaction: discord.Interaction):
        """Flips a coin and returns heads or tails."""
        result = random.choice(['Heads', 'Tails'])
        await interaction.response.send_message(f'You flipped: {result}')

    @app_commands.command(name='roll')
    async def roll(self, interaction: discord.Interaction):
        """Rolls a six-sided die."""
        result = random.randint(1, 6)
        await interaction.response.send_message(f'You rolled a: {result}')

    @app_commands.command(name='randomnumber')
    async def randomnumber(self, interaction: discord.Interaction, start: int, end: int):
        """Generates a random number between start and end (inclusive)."""
        result = random.randint(start, end)
        await interaction.response.send_message(f'Random number between {start} and {end}: {result}')

    @app_commands.command(name='randomlol')
    async def randomlol(self, interaction: discord.Interaction):
        """Selects a random League of Legends champion."""
        champion = random.choice(lol_champions)
        await interaction.response.send_message(f'Your random League of Legends champion is: {champion}')

async def setup(bot):
    await bot.add_cog(UtilityCog(bot))