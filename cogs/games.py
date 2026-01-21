import discord
from discord.ext import commands
import random
from discord import app_commands
import asyncio
import json

bottikanava = 1330971805133045791

with open("data/words.json", "r") as f:
            sanalista = json.load(f)

class SlotMachineView(discord.ui.View):
    def __init__(self, author):
        super().__init__(timeout=30)
        self.author = author
        self.hedelmat = ["🍒", "🍋", "🍊", "🍉", "⭐", "7️⃣"]

    @discord.ui.button(label="Spin", style=discord.ButtonStyle.green)
    async def spin_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.author:
            await interaction.response.send_message("This is not your game!", ephemeral=True)
            return
        
        rullat = [random.choice(self.hedelmat) for _ in range(3)]
        tulos = " ".join(rullat)
        
        if rullat[0] == rullat[1] == rullat[2]:
            voitto = "🎉 You win! 🎉"
        else:
            voitto = "😞 You lose. Try again!"

        await interaction.response.edit_message(content=f"Result: \n\n{tulos}\n\n{voitto}", view=self)

class Wordle:
    def __init__(self, interaction, bot, sana):
        self.interaction = interaction
        self.bot = bot
        self.sana = sana.lower()
        self.yritykset = []
        self.max_yritykset = 6
        self.vaarat_kirjaimet = set()

    def muodosta_lauta(self):
        teksti = ""
        for yritys in self.yritykset:
            teksti += "\n" + yritys + "\n"
        for _ in range(self.max_yritykset - len(self.yritykset)):
            teksti += "⬜⬜⬜⬜⬜\n"

        if self.vaarat_kirjaimet:
            teksti += "\nWrong letters: " + " ".join(sorted(self.vaarat_kirjaimet)).upper()
        return teksti
    
    async def pelaa(self):
        await self.interaction.response.send_message(self.muodosta_lauta())
        peliviesti = await self.interaction.original_response()

        while len(self.yritykset) < self.max_yritykset:
            def check(m):
                return m.author == self.interaction.user and m.channel == self.interaction.channel
            
            try:
                vastaus = await self.bot.wait_for('message', check=check, timeout=600.0)
                arvaus = vastaus.content.lower()

                try:
                    await vastaus.delete()
                except:
                    pass

                if len(arvaus) != 5 or not arvaus.isalpha() or arvaus not in sanalista["words"]:
                    continue

                tulos_emojit = []
                for i in range(5):
                    if arvaus[i] == self.sana[i]:
                        tulos_emojit.append("🟩")
                    elif arvaus[i] in self.sana:
                        tulos_emojit.append("🟨")
                    else:
                        tulos_emojit.append("⬜")
                        self.vaarat_kirjaimet.add(arvaus[i])

                self.yritykset.append(arvaus.upper() + "\n" + "".join(tulos_emojit))

                await peliviesti.edit(content=self.muodosta_lauta())

                if arvaus == self.sana:
                    await self.interaction.followup.send(f"🎉 Congratulations! You've guessed the word: {self.sana.upper()} 🎉")
                    return
                
            except asyncio.TimeoutError:
                await self.interaction.followup.send(f"⏰ Sorry, time ran out.")
                return
            
        await self.interaction.followup.send(f"😞 You've used all attempts! The word was: {self.sana.upper()}")

class Hirsipuu:
    def __init__(self, interaction, bot, sana):
        self.interaction = interaction
        self.bot = bot
        self.sana = sana.lower()
        self.oikeat = set()
        self.vaarat = []
        self.max_yritykset = 6

    def muodosta_lauta(self):
        teksti = "Word: "
        for kirjain in self.sana:
            if kirjain in self.oikeat:
                teksti += kirjain.upper() + " "
            else:
                teksti += "- "
        teksti += "\nWord length: " + str(len(self.sana))
        teksti += f"\nWrong guesses: {' '.join(self.vaarat).upper()} ({len(self.vaarat)}/{self.max_yritykset})"
        return teksti
    
    async def pelaa(self):
        await self.interaction.response.send_message(self.muodosta_lauta())
        peliviesti = await self.interaction.original_response()

        while len(self.vaarat) < self.max_yritykset:
            def check(m):
                return m.author != self.interaction.user and m.channel == self.interaction.channel
            
            try:
                vastaus = await self.bot.wait_for('message', check=check, timeout=600.0)
                arvaus = vastaus.content.lower()

                try:
                    await vastaus.delete()
                except:
                    pass

                if len(arvaus) != 1 or not arvaus.isalpha():
                    continue

                if arvaus in self.oikeat or arvaus in self.vaarat:
                    continue

                if arvaus in self.sana:
                    self.oikeat.add(arvaus)
                else:
                    self.vaarat.append(arvaus)

                await peliviesti.edit(content=self.muodosta_lauta())

                if all(kirjain in self.oikeat for kirjain in self.sana):
                    await self.interaction.followup.send(f"🎉 Congratulations! You've guessed the word: {self.sana.upper()} 🎉")
                    return
                
            except asyncio.TimeoutError:
                await self.interaction.followup.send(f"⏰ Sorry, time ran out.")
                return
            
        await self.interaction.followup.send(f"😞 You've used all attempts! The word was: {self.sana.upper()}")
        


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="slots", description="Play a slot machine game.")
    async def slots(self, interaction: discord.Interaction):
        if interaction.channel.id != bottikanava:
            await interaction.response.send_message("This command can only be used in the designated bot channel.", ephemeral=True)
            return
        view = SlotMachineView(interaction.user)
        await interaction.response.send_message("Spinning the slot machine...", view=view)

    @app_commands.command(name="botwordle", description="Play a Wordle game against the bot.")
    async def botwordle(self, interaction: discord.Interaction):
        if interaction.channel.id != bottikanava:
            await interaction.response.send_message("This command can only be used in the designated bot channel.", ephemeral=True)
            return
        sana = random.choice(sanalista["words"])
        wordle_peli = Wordle(interaction, self.bot, sana)
        await wordle_peli.pelaa()

    @app_commands.command(name="hangman", description="Play a Hangman game.")
    async def hangman(self, interaction: discord.Interaction, sana: str):
        if interaction.channel.id != bottikanava:
            await interaction.response.send_message("This command can only be used in the designated bot channel.", ephemeral=True)
            return
        sana = sana.lower()
        if not sana.isalpha() or len(sana) < 3:
            await interaction.response.send_message("Please provide a valid word (at least 3 letters, alphabetic only).", ephemeral=True)
            return
        hirsipuu_peli = Hirsipuu(interaction, self.bot, sana)
        await hirsipuu_peli.pelaa()

async def setup(bot):
    await bot.add_cog(Games(bot))
