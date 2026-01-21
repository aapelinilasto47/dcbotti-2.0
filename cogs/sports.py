import discord
from discord.ext import commands
from discord import app_commands
import random
import aiohttp
import os
import requests
import json

class SportsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = os.getenv("API_KEY_FOOTBALL")
        self.headers = {
            "x-apisports-key": self.api_key
        }

    @app_commands.command(name="plstandings", description="Get league tables for a specific league and season.")
    async def plstandings(self, interaction: discord.Interaction, season: int):
        await interaction.response.defer()
        url = f"https://v3.football.api-sports.io/standings"
        params = {
            "league": 39,  # Premier League ID
            "season": season
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers, params=params) as resp:
                if resp.status != 200:
                    await interaction.followup.send("Failed to retrieve data from the API.", ephemeral=True)
                    return
                data = await resp.json()

                if data.get("errors"):
                    await interaction.followup.send("Error from API: " + str(data["errors"]), ephemeral=True)
                    return
                
                standings = data["response"][0]["league"]["standings"][0]
                embed = discord.Embed(title=f"Premier League Standings {season}", color=discord.Color.blue())
                for team in standings:
                    position = team["rank"]
                    name = team["team"]["name"]
                    points = team["points"]
                    embed.add_field(name=f"{position}. {name}", value=f"Points: {points}", inline=False)

                await interaction.followup.send(embed=embed)

    

async def setup(bot):
    await bot.add_cog(SportsCog(bot))