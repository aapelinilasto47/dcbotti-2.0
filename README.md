# Discord Bot 2.0 (Python)

Tämä on monipuolinen Discord-botti, joka on rakennettu Pythonilla hyödyntäen nykyaikaisia asynkronisia rajapintoja. Projekti esittelee olio-ohjelmointia (OOP), ulkoisten API-rajapintojen integrointia ja käyttäjäystävällistä UI-suunnittelua.
Tein tämän projektin, koska halusin rakentaa aiemmin rakentamani Discord botin uudelleen laadukkaampaa koodia käyttäen.

## Ominaisuudet

* **Urheilutilastot:** Valioliiga-sarjataulukot (integroitu API-Football rajapintaan).
* **Wordle-peli:** Interaktiivinen sanapeli!
* **Hirsipuu:** Klassinen peli dynaamisella viestien päivityksellä.
* **Modulaarinen rakenne:** Hyödyntää Discord.py:n "Cogs"-järjestelmää, mikä tekee koodista helposti laajennettavaa ja ylläpidettävää.

## Teknologiat

* **Kieli:** Python 3.x
* **Kirjasto:** [discord.py](https://github.com/Rapptz/discord.py)
* **Asynkronisuus:** `asyncio` ja `aiohttp` (non-blocking API-pyynnöt).
* **Tietoturva:** `python-dotenv` (salaisuuksien hallinta ympäristömuuttujilla).

## Käyttöönotto

1. Kopioi repo: `git clone https://github.com/sinun-kayttajanimi/projektin-nimi.git`
2. Asenna riippuvuudet: `pip install -r requirements.txt`
3. Luo `.env`-tiedosto ja lisää omat avaimesi:
   ```env
   DISCORD_TOKEN=sinun_token
   API_KEY_FOOTBALL=sinun_api_avain
    ```
4. Käynnistä botti: `python main.py`

## Mitä opin?

* API-integraatiot: HTTP-pyyntöjen, headereiden ja JSON-datan käsittely.

* State Management: Pelin tilan hallinta asynkronisessa ympäristössä.

* UX/UI: Käyttäjäkokemuksen parantaminen Discord-komponenteilla (Embeds, Buttons, Modals).
