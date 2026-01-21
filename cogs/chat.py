import discord
from discord.ext import commands
import random
import json

bottikanava = 1330971805133045791

with open("data/triggers.json", "r") as f:
    trigger_data = json.load(f)
    triggers = trigger_data["triggers"]
    responses = trigger_data["responses"]

class ChatCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.channel.id != bottikanava:
            return

        sisalto = message.content.lower()

        for trigger in triggers:
            if trigger in sisalto:
                response = random.choice(responses)
                await message.channel.send(response)
                break

        
async def setup(bot):
    await bot.add_cog(ChatCog(bot))