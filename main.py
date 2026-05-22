import discord
from discord.ext import commands
import os
import time
import psutil
import logging

# =========================
# METADATA
# =========================

VERSION = "v1.2.5"
NOME_PROJETO = "Conexão Alê Bot"

PROJETO_DESC = (
    "Bot oficial do projeto Conexão Alê, responsável por automação, "
    "informações do sistema e suporte no servidor."
)

ATUALIZACAO_INFO = {
    "titulo": "Painel técnico + separação de comandos + melhoria de estrutura",
    "tipo": "Correção + Atualização",
    "mudancas": [
        "Separação clara entre info, ping e status",
        "Implementação de painel técnico completo",
        "Melhoria na estrutura de embeds",
        "Padronização de sistema do bot"
    ]
}

# =========================
# UPTIME
# =========================

start_time = time.time()

def uptime():
    t = int(time.time() - start_time)
    h = t // 3600
    m = (t % 3600) // 60
    s = t % 60
    return f"{h}h {m}m {s}s"

# =========================
# LOGGING
# =========================

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

# =========================
# BOT SETUP
# =========================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# =========================
# READY
# =========================

@bot.event
async def on_ready():
    logging.info(f"{NOME_PROJETO} online como {bot.user}")
    logging.info(f"Versão: {VERSION}")

    await bot.change_presence(
        activity=discord.Game(name=f"{NOME_PROJETO} | v{VERSION}")
    )

# =========================
# 🏓 PING
# =========================

@bot.command()
async def ping(ctx):

    start = time.perf_counter()
    msg = await ctx.send("📡 Calculando latência...")
    end = time.perf_counter()

    bot_latency = round(bot.latency * 1000)
    api_latency = round((end - start) * 1000)

    status = (
        "🟢 Online" if bot_latency < 100 else
        "🟡 Estável" if bot_latency < 200 else
        "🔴 Lento"
    )

    embed = discord.Embed(
        title="🏓 Ping do Bot",
        color=discord.Color.blue(),
        timestamp=discord.utils.utcnow()
    )

    embed.add_field(name="🤖 Latência do Bot", value=f"{bot_latency}ms", inline=True)
    embed.add_field(name="📡 Latência da API", value=f"{api_latency}ms", inline=True)
    embed.add_field(name="⚙️ Classificação", value=status, inline=True)

    await msg.edit(content=None, embed=embed)

# =========================
# 📘 INFO
# =========================

@bot.command()
async def info(ctx):

    embed = discord.Embed(
        title="📘 Informações do Bot",
        description=PROJETO_DESC,
        color=discord.Color.purple(),
        timestamp=discord.utils.utcnow()
    )

    embed.add_field(name="Projeto", value="Conexão Alê", inline=True)
    embed.add_field(name="Versão", value=VERSION, inline=True)

    embed.add_field(
        name="🆕 Última atualização",
        value=ATUALIZACAO_INFO["titulo"],
        inline=False
    )

    embed.add_field(
        name="Tipo",
        value=ATUALIZACAO_INFO["tipo"],
        inline=True
    )

    embed.add_field(
        name="Mudanças",
        value="\n".join(f"• {m}" for m in ATUALIZACAO_INFO["mudancas"]),
        inline=False
    )

    await ctx.send(embed=embed)

# =========================
# 📊 STATUS (PAINEL TÉCNICO)
# =========================

@bot.command()
async def status(ctx):

    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    servidores = len(bot.guilds)
    ping = round(bot.latency * 1000)

    estado = (
        "🟢 Online" if ping < 150 else
        "🟡 Instável" if ping < 250 else
        "🔴 Crítico"
    )

    embed = discord.Embed(
        title="📊 Painel Técnico",
        color=discord.Color.green(),
        timestamp=discord.utils.utcnow()
    )

    embed.add_field(name="🧠 CPU", value=f"{cpu}%", inline=True)
    embed.add_field(name="💾 RAM", value=f"{ram}%", inline=True)
    embed.add_field(name="🌐 Servidores", value=str(servidores), inline=True)

    embed.add_field(name="📡 Ping", value=f"{ping}ms", inline=True)
    embed.add_field(name="⚙️ Estado", value=estado, inline=True)
    embed.add_field(name="⏱ Uptime", value=uptime(), inline=True)

    embed.add_field(
        name="🧾 Sistema",
        value="Monitoramento ativo e contínuo",
        inline=False
    )

    await ctx.send(embed=embed)

# =========================
# TOKEN (RAILWAY)
# =========================

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    logging.critical("TOKEN não encontrado")
    raise SystemExit()

bot.run(TOKEN)
