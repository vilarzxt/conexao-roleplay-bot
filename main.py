import discord
from discord.ext import commands
import os
import time
import psutil
import logging

# =========================
# METADADOS
# =========================

VERSION = "v1.2.3"
PROJECT_NAME = "Conexão Roleplay Bot"

# =========================
# LOGGING
# =========================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# =========================
# INTENTS
# =========================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# =========================
# ON READY + SYNC SLASH
# =========================

@bot.event
async def on_ready():
    logging.info(f"{PROJECT_NAME} online como {bot.user}")
    logging.info(f"Versão: {VERSION}")
    logging.info(f"Servidores: {len(bot.guilds)}")

    try:
        synced = await bot.tree.sync()
        logging.info(f"Slash Commands sincronizados: {len(synced)}")
    except Exception as e:
        logging.error(f"Erro ao sincronizar comandos: {e}")

    await bot.change_presence(
        activity=discord.Game(name=f"{PROJECT_NAME} | {VERSION}"),
        status=discord.Status.online
    )

# =========================
# SLASH COMMAND: PING
# =========================

@bot.tree.command(name="ping", description="Mostra a latência do bot")
async def ping(interaction: discord.Interaction):

    start = time.perf_counter()
    await interaction.response.send_message("📡 Calculando latência...")
    end = time.perf_counter()

    bot_latency = round(bot.latency * 1000)
    api_latency = round((end - start) * 1000)

    status = (
        "🟢 Excelente" if bot_latency < 100 else
        "🟡 Estável" if bot_latency < 200 else
        "🔴 Alta"
    )

    embed = discord.Embed(
        title="🏓 Ping do Sistema",
        color=discord.Color.blue(),
        timestamp=discord.utils.utcnow()
    )

    embed.add_field(name="🤖 Bot", value=f"`{bot_latency}ms`", inline=True)
    embed.add_field(name="📡 API", value=f"`{api_latency}ms`", inline=True)
    embed.add_field(name="📊 Status", value=status, inline=True)

    embed.set_footer(text=f"{PROJECT_NAME} • {VERSION}")

    await interaction.edit_original_response(content=None, embed=embed)

# =========================
# SLASH COMMAND: INFO
# =========================

@bot.tree.command(name="info", description="Informações do bot")
async def info(interaction: discord.Interaction):

    embed = discord.Embed(
        title="📘 Informações do Bot",
        description="Sistema oficial da Conexão Roleplay",
        color=discord.Color.purple(),
        timestamp=discord.utils.utcnow()
    )

    embed.add_field(name="🤖 Bot", value=str(interaction.client.user), inline=True)
    embed.add_field(name="📦 Versão", value=VERSION, inline=True)
    embed.add_field(name="🌐 Servidores", value=str(len(interaction.client.guilds)), inline=True)

    embed.add_field(
        name="🆕 Atualização",
        value="Migração completa para Slash Commands (v1.2.3)",
        inline=False
    )

    embed.add_field(
        name="⚙️ Ambiente",
        value="GitHub → Railway Deploy",
        inline=False
    )

    embed.set_footer(text=f"{PROJECT_NAME} • System Info")

    await interaction.response.send_message(embed=embed)

# =========================
# SLASH COMMAND: STATUS
# =========================

@bot.tree.command(name="status", description="Status do sistema do bot")
async def status(interaction: discord.Interaction):

    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent

    embed = discord.Embed(
        title="📊 Status do Sistema",
        color=discord.Color.green(),
        timestamp=discord.utils.utcnow()
    )

    embed.add_field(name="🧠 CPU", value=f"{cpu}%", inline=True)
    embed.add_field(name="💾 RAM", value=f"{ram}%", inline=True)
    embed.add_field(name="📡 Ping", value=f"{round(bot.latency * 1000)}ms", inline=True)

    embed.add_field(
        name="🧾 Estado geral",
        value="🟢 Operacional",
        inline=False
    )

    embed.set_footer(text=f"{PROJECT_NAME} • Monitoring")

    await interaction.response.send_message(embed=embed)

# =========================
# TOKEN (RAILWAY)
# =========================

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    logging.critical("TOKEN não encontrado (variável de ambiente)")
    raise SystemExit("TOKEN ausente")

# =========================
# RUN
# =========================

bot.run(TOKEN)
