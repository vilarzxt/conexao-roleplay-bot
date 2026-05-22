import discord
from discord.ext import commands
import os
import time
import psutil
import logging

# =========================
# 📦 METADATA DO BOT
# =========================

VERSION = "v1.2.7"
PROJECT_NAME = "Conexão Roleplay"

PROJECT_DESCRIPTION = (
    "Bot oficial do projeto Conexão Roleplay, responsável por automação, "
    "monitoramento e informações técnicas do servidor."
)

LAST_UPDATE = {
    "version": VERSION,
    "type": "Correção",
    "description": "Padronização de identidade e textos do sistema",
    "changes": [
        "Padronização do nome do projeto para Conexão Roleplay",
        "Correção de textos e embeds para PT-BR",
        "Uniformização de identidade visual dos comandos",
        "Ajuste de consistência no sistema de informações"
    ]
}

# =========================
# ⏱ UPTIME
# =========================

start_time = time.time()

def get_uptime():
    elapsed = int(time.time() - start_time)
    h = elapsed // 3600
    m = (elapsed % 3600) // 60
    s = elapsed % 60
    return f"{h}h {m}m {s}s"

# =========================
# 📜 LOGGING
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
# ⚙️ GUILD TESTE (RAILWAY)
# =========================

ID_SERVIDOR_TESTE = 1465461083757351061

@bot.event
async def setup_hook():
    guild = discord.Object(id=ID_SERVIDOR_TESTE)

    bot.tree.clear_commands(guild=guild)
    await bot.tree.sync(guild=guild)

    logging.info("Comandos slash sincronizados com sucesso")

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

@bot.tree.command(name="ping", description="Mostra a latência do bot")
async def ping(interaction: discord.Interaction):

    bot_latency = round(bot.latency * 1000)

    status = (
        "🟢 Online" if bot_latency < 120 else
        "🟡 Estável" if bot_latency < 250 else
        "🔴 Lento"
    )

    embed = discord.Embed(
        title="🏓 Sistema de Ping",
        color=discord.Color.blue()
    )

    embed.add_field(name="Latência do Bot", value=f"{bot_latency}ms", inline=True)
    embed.add_field(name="Status", value=status, inline=True)

    await interaction.response.send_message(embed=embed)

# =========================
# 📘 /INFO
# =========================

@bot.tree.command(name="info", description="Informações do bot")
async def info(interaction: discord.Interaction):

    embed = discord.Embed(
        title="📘 Informações do Bot",
        description=PROJECT_DESCRIPTION,
        color=discord.Color.purple()
    )

    embed.add_field(name="Projeto", value=PROJECT_NAME, inline=True)
    embed.add_field(name="Versão", value=VERSION, inline=True)

    embed.add_field(
        name="Última atualização",
        value=LAST_UPDATE["description"],
        inline=False
    )

    embed.add_field(
        name="Tipo",
        value=LAST_UPDATE["type"],
        inline=True
    )

    embed.add_field(
        name="Resumo",
        value="\n".join(f"• {c}" for c in LAST_UPDATE["changes"]),
        inline=False
    )

    await interaction.response.send_message(embed=embed)

# =========================
# 📊 /STATUS
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
        title="📊 Painel do Sistema",
        color=discord.Color.green()
    )

    embed.add_field(name="CPU", value=f"{cpu}%", inline=True)
    embed.add_field(name="RAM", value=f"{ram}%", inline=True)
    embed.add_field(name="Servidores", value=str(servers), inline=True)

    embed.add_field(name="Ping", value=f"{ping}ms", inline=True)
    embed.add_field(name="Estado", value=state, inline=True)
    embed.add_field(name="Uptime", value=uptime, inline=True)

    await interaction.response.send_message(embed=embed)

# =========================
# 🔐 TOKEN (RAILWAY)
# =========================

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    logging.critical("TOKEN não encontrado nas variáveis de ambiente")
    raise SystemExit("TOKEN ausente")

bot.run(TOKEN)
