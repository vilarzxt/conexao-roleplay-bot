import discord
from discord.ext import commands
from discord import app_commands
import os
import time
import psutil
import logging

# =========================
# 🧪 DEBUG FLAGS
# =========================

print(">>> [BOOT] main.py carregado com sucesso <<<")

# =========================
# 📦 VERSIONAMENTO
# =========================

BASE_VERSION = "1.2.8"
PATCH_VERSION = 4

VERSION = f"{BASE_VERSION}.{PATCH_VERSION}-debug"

UPDATE_TYPE = "Correção"

PROJECT_NAME = "Conexão Roleplay (DEBUG)"

PROJECT_DESCRIPTION = "Versão de teste para validar execução do bot"

# =========================
# ⏱ UPTIME
# =========================

start_time = time.time()

def get_uptime():
    elapsed = int(time.time() - start_time)
    return f"{elapsed//3600}h {(elapsed%3600)//60}m {elapsed%60}s"

# =========================
# LOGGING
# =========================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# =========================
# BOT SETUP
# =========================

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

GUILD_ID = 1465461083757351061

# =========================
# EMBED PADRÃO
# =========================

def setup_embed(embed: discord.Embed):
    return embed

# =========================
# 🔥 TESTE DE SYNC
# =========================

@bot.event
async def setup_hook():
    print(">>> [SETUP_HOOK] iniciado <<<")

    guild = discord.Object(id=GUILD_ID)

    try:
        synced = await bot.tree.sync(guild=guild)

        print(f">>> [SYNC] {len(synced)} comandos sincronizados (GUILD)")
        logging.info(f"{len(synced)} comandos sincronizados")

    except Exception as e:
        print(">>> [SYNC ERROR]", e)
        logging.error(e)

# =========================
# 🔥 READY TEST
# =========================

@bot.event
async def on_ready():
    print(">>> [ON_READY] DISPAROU <<<")
    print(f">>> BOT: {bot.user}")

    logging.info(f"ONLINE COMO {bot.user}")
    logging.info(f"VERSÃO {VERSION}")
    logging.info(f"SERVIDORES {len(bot.guilds)}")
    logging.info(f"COMANDOS {len(bot.tree.get_commands())}")

    await bot.change_presence(
        activity=discord.Game(name=f"{PROJECT_NAME} {VERSION}")
    )

# =========================
# 🧪 TESTE /PING
# =========================

@bot.tree.command(name="ping", description="teste ping")
async def ping(interaction: discord.Interaction):

    print(">>> [COMMAND] /ping usado <<<")

    latency = round(bot.latency * 1000)

    embed = discord.Embed(
        title="PING TESTE",
        description=f"{latency}ms",
        color=0x00ff00
    )

    await interaction.response.send_message(embed=embed)

# =========================
# 🧪 TESTE /INFO
# =========================

@bot.tree.command(name="info", description="teste info")
async def info(interaction: discord.Interaction):

    print(">>> [COMMAND] /info usado <<<")

    embed = discord.Embed(
        title="INFO DEBUG",
        description=PROJECT_DESCRIPTION,
        color=0x00ff00
    )

    embed.add_field(name="Versão", value=VERSION)

    await interaction.response.send_message(embed=embed)

# =========================
# TOKEN
# =========================

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    print(">>> TOKEN AUSENTE <<<")
    raise SystemExit("TOKEN ausente")

print(">>> INICIANDO BOT.RUN <<<")

bot.run(TOKEN)
