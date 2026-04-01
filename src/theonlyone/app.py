import discord
from discord.ext import commands
import os
intents = discord.Intents.default()
intents.message_content = True
import os
from dotenv import load_dotenv
load_dotenv()
token = os.getenv("TOKEN")

class App(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=['$', '!'], intents=intents)
    async def setup_hook(self):
        caminho_atual = os.path.dirname(os.path.abspath(__file__))
        pasta_commands = os.path.join(caminho_atual, 'commands')
        for filename in os.listdir(pasta_commands):
            if filename.endswith(".py"):
                await self.load_extension(f'commands.{filename[:-3]}')
                print(f"Comando {filename} carregado!")                
bot = App()
@bot.event
async def on_ready():
    print(f"BOT {bot.user} está rodando!")
    
bot.run(token)