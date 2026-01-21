import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.load_extension("cogs.games")
        await self.load_extension("cogs.chat")
        await self.load_extension("cogs.utility")
        await self.load_extension("cogs.sports")

        await self.tree.sync()
        print("Commands synced!")

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")

bot = MyBot()
bot.run(os.getenv("DISCORD_TOKEN"))