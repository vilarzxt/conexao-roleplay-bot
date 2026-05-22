import discord
from discord.ext import commands
import os
import time
import psutil
import logging

# =========================
# 📦 METADATA DO BOT
# =========================

VERSION = "v1.2.6"
PROJECT_NAME = "Conexão Alê Bot"

PROJECT_DESCRIPTION = (
    "Bot oficial do projeto Conexão Alê, responsável por automação, "
    "monitoramento e informações técnicas do servidor."
)

LAST_UPDATE = {
    "version": VERSION,
    "type": "Correção + Atualização estrutural",
    "description": "Restauração da arquitetura completa (metadata + telemetry + slash system)",
    "changes": [
        "Reimplementação do metadata system",
        "Padronização total em slash commands",
        "Restauração do uptime system",
        "Melhoria no painel de status",
        "Correção de sync de comandos no Railway"
    ]
}

# =========================
# ⏱ UPTIME TRACKER
# =========================

start_time = time.time()

def get_uptime():
    elapsed = int(time.time() - start_time)
    h = elapsed // 3600
    m = (elapsed % 3600) // 60
    s = elapsed % 60
    return f"{h}h {m}m {s}s"

# =========================
# 📜 LOGGING SYSTEM
# =========================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# =========================
# 🤖 BOT SETUP
# =========================

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# =========================
# ⚙️ BOOT SYSTEM (CRÍTICO)
# =========================

ID_SERVIDOR_TESTE = 1465461083757351061

@bot.event
async def setup_hook():
    guild = discord.Object(id=ID_SERVIDOR_TESTE)

    bot.tree.clear_commands(guild=guild)
    await bot.tree.sync(guild=guild)

    logging.info("Slash commands sincronizados (guild mode)")

@bot.event
async def on_ready():
    logging.info(f"{PROJECT_NAME} online como {bot.user}")
    logging.info(f"Versão: {VERSION}")
    logging.info(f"Servidores conectados: {len(bot.guilds)}")

    await bot.change_presence(
        activity=discord.Game(name=f"{PROJECT_NAME} | v{VERSION}")
    )

# =========================
# 🏓 /PING
# =========================

@bot.tree.command(name="ping", description="Mostra latência do bot")
async def ping(interaction: discord.Interaction):

    bot_latency = round(bot.latency * 1000)

    status = (
        "🟢 Online" if bot_latency < 120 else
        "🟡 Estável" if bot_latency < 250 else
        "🔴 Crítico"
    )

    embed = discord.Embed(
        title="🏓 Ping System",
        color=discord.Color.blue()
    )

    embed.add_field(name="Bot Latency", value=f"{bot_latency}ms", inline=True)
    embed.add_field(name="Status", value=status, inline=True)

    await interaction.response.send_message(embed=embed)

# =========================
# 📘 /INFO (METADATA COMPLETO)
# =========================

@bot.tree.command(name="info", description="Informações do bot e sistema")
async def info(interaction: discord.Interaction):

    embed = discord.Embed(
        title="📘 Bot Information System",
        description=PROJECT_DESCRIPTION,
        color=discord.Color.purple()
    )

    embed.add_field(name="Project", value=PROJECT_NAME, inline=True)
    embed.add_field(name="Version", value=VERSION, inline=True)

    embed.add_field(
        name="Last Update",
        value=LAST_UPDATE["description"],
        inline=False
    )

    embed.add_field(
        name="Type",
        value=LAST_UPDATE["type"],
        inline=True
    )

    embed.add_field(
        name="Changes",
        value="\n".join(f"• {c}" for c in LAST_UPDATE["changes"]),
        inline=False
    )

    await interaction.response.send_message(embed=embed)

# =========================
# 📊 /STATUS (PAINEL TÉCNICO COMPLETO)
# =========================

@bot.tree.command(name="status", description="Painel técnico do sistema")
async def status(interaction: discord.Interaction):

    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    servers = len(bot.guilds)
    ping = round(bot.latency * 1000)
    uptime = get_uptime()

    state = (
        "🟢 Operacional" if ping < 150 else
        "🟡 Instável" if ping < 250 else
        "🔴 Crítico"
    )

    embed = discord.Embed(
        title="📊 System Control Panel",
        color=discord.Color.green()
    )

    embed.add_field(name="CPU", value=f"{cpu}%", inline=True)
    embed.add_field(name="RAM", value=f"{ram}%", inline=True)
    embed.add_field(name="Servers", value=str(servers), inline=True)

    embed.add_field(name="Ping", value=f"{ping}ms", inline=True)
    embed.add_field(name="State", value=state, inline=True)
    embed.add_field(name="Uptime", value=uptime, inline=True)

    await interaction.response.send_message(embed=embed)

# =========================
# 🔐 TOKEN RAILWAY
# =========================

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise SystemExit("TOKEN não encontrado")

bot.run(TOKEN)
