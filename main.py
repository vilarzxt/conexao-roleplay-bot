import discord
from discord.ext import commands
from discord import app_commands
import os
import time
import psutil
import logging

# =========================
# 📦 VERSIONAMENTO
# =========================

VERSION = "1.2.9.9 - debug sync"

PROJECT_NAME = "Conexão Roleplay"

PROJECT_DESCRIPTION = (
    "Bot oficial do projeto Conexão Roleplay, responsável por automação, "
    "administração, monitoramento e integração de sistemas."
)

# =========================
# 🎨 ASSETS
# =========================

LOGO = "https://i.postimg.cc/6pnGkC0h/file-0000000071f071f9a14ca207e3220fbd.png"
EMBED_COLOR = 0x145A32

# =========================
# ⏱ UPTIME
# =========================

start_time = time.time()

def uptime():
    t = int(time.time() - start_time)
    return f"{t//3600}h {(t%3600)//60}m {t%60}s"

# =========================
# LOGGING
# =========================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# =========================
# BOT
# =========================

intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

GUILD_ID = 1465461083757351061

# =========================
# EMBED BASE
# =========================

def embed_base(embed: discord.Embed):
    embed.set_thumbnail(url=LOGO)
    embed.set_footer(text="Conexão Roleplay • Sistema Oficial", icon_url=LOGO)
    return embed

# =========================
# 🧠 COMANDOS SLASH
# =========================

@bot.tree.command(name="ping", description="Latência do bot")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"🏓 {round(bot.latency*1000)}ms")


@bot.tree.command(name="info", description="Informações do sistema")
async def info(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Info",
        description=PROJECT_DESCRIPTION,
        color=EMBED_COLOR
    )
    embed_base(embed)
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="status", description="Status do sistema")
async def status(interaction: discord.Interaction):
    embed = discord.Embed(title="Status", color=EMBED_COLOR)
    embed.add_field(name="CPU", value=f"{psutil.cpu_percent(interval=0.5)}%")
    embed.add_field(name="RAM", value=f"{psutil.virtual_memory().percent}%")
    embed.add_field(name="Uptime", value=uptime())
    embed_base(embed)
    await interaction.response.send_message(embed=embed)


# =========================
# 🚀 READY + SYNC CORRETO
# =========================

@bot.event
async def on_ready():
    print("===================================")
    print("LOGADO:", bot.user)
    print("VERSION:", VERSION)
    print("REGISTRANDO COMANDOS...")

    guild = discord.Object(id=GUILD_ID)

    try:
        synced = await bot.tree.sync(guild=guild)

        print("SYNC RESULT:", len(synced))
        print("COMANDOS INTERNOS:", [cmd.name for cmd in bot.tree.get_commands()])

    except Exception as e:
        print("ERRO NO SYNC:", e)

    print("BOT PRONTO E OPERACIONAL")
    print("===================================")


# =========================
# TOKEN
# =========================

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise SystemExit("TOKEN ausente")

bot.run(TOKEN)
