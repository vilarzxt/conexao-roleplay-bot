import discord
from discord.ext import commands
import os
import time
import psutil
import logging

# =========================
# METADATA DO BOT
# =========================

VERSION = "v1.2.4"
NOME_PROJETO = "Conexão Roleplay Bot"

# 🔥 SERVIDOR DE TESTE (GUILD SYNC)
ID_SERVIDOR_TESTE = 1465461083757351061

ATUALIZACAO_INFO = {
    "versao": VERSION,
    "titulo": "Correção de duplicação + sync por servidor + suporte a prefixo",
    "mudancas": [
        "Correção de duplicação de comandos slash",
        "Sincronização de comandos apenas no servidor de teste",
        "Adição de comandos por prefixo (!)",
        "Padronização de versão e estrutura do bot"
    ]
}

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
# ON READY (SYNC GUILD)
# =========================

@bot.event
async def on_ready():
    logging.info(f"{NOME_PROJETO} online como {bot.user}")
    logging.info(f"Versão: {VERSION}")
    logging.info(f"Servidores: {len(bot.guilds)}")

    try:
        guild = discord.Object(id=ID_SERVIDOR_TESTE)
        synced = await bot.tree.sync(guild=guild)
        logging.info(f"Slash Commands sincronizados: {len(synced)}")
    except Exception as e:
        logging.error(f"Erro ao sincronizar comandos: {e}")

    await bot.change_presence(
        activity=discord.Game(name=f"{NOME_PROJETO} | {VERSION}")
    )

# =========================
# PREFIX COMMANDS (!)
# =========================

@bot.command()
async def ping(ctx):
    start = time.perf_counter()
    msg = await ctx.send("📡 Calculando latência...")
    end = time.perf_counter()

    embed = discord.Embed(
        title="🏓 Ping (Prefixo)",
        color=discord.Color.blue(),
        timestamp=discord.utils.utcnow()
    )

    embed.add_field(name="Bot", value=f"{round(bot.latency * 1000)}ms", inline=True)
    embed.add_field(name="API", value=f"{round((end - start) * 1000)}ms", inline=True)

    await msg.edit(content=None, embed=embed)

@bot.command()
async def info(ctx):

    embed = discord.Embed(
        title="📘 Informações do Bot",
        color=discord.Color.purple()
    )

    embed.add_field(name="Versão", value=VERSION, inline=True)

    embed.add_field(
        name="Atualização",
        value=ATUALIZACAO_INFO["titulo"],
        inline=False
    )

    embed.add_field(
        name="Mudanças",
        value="\n".join(f"• {m}" for m in ATUALIZACAO_INFO["mudancas"]),
        inline=False
    )

    await ctx.send(embed=embed)

@bot.command()
async def status(ctx):

    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent

    embed = discord.Embed(
        title="📊 Status do Sistema",
        color=discord.Color.green()
    )

    embed.add_field(name="CPU", value=f"{cpu}%", inline=True)
    embed.add_field(name="RAM", value=f"{ram}%", inline=True)

    await ctx.send(embed=embed)

# =========================
# SLASH COMMANDS (/)
# =========================

@bot.tree.command(name="ping", description="Mostra o ping do bot")
async def slash_ping(interaction: discord.Interaction):

    embed = discord.Embed(
        title="🏓 Ping (Slash)",
        color=discord.Color.blue()
    )

    embed.add_field(name="Latência", value=f"{round(bot.latency * 1000)}ms")

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="info", description="Informações do bot")
async def slash_info(interaction: discord.Interaction):

    embed = discord.Embed(
        title="📘 Informações do Bot",
        color=discord.Color.purple()
    )

    embed.add_field(name="Versão", value=VERSION, inline=True)

    embed.add_field(
        name="Atualização",
        value=ATUALIZACAO_INFO["titulo"],
        inline=False
    )

    embed.add_field(
        name="Mudanças",
        value="\n".join(f"• {m}" for m in ATUALIZACAO_INFO["mudancas"]),
        inline=False
    )

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="status", description="Status do sistema")
async def slash_status(interaction: discord.Interaction):

    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent

    embed = discord.Embed(
        title="📊 Status do Sistema",
        color=discord.Color.green()
    )

    embed.add_field(name="CPU", value=f"{cpu}%")
    embed.add_field(name="RAM", value=f"{ram}%")

    await interaction.response.send_message(embed=embed)

# =========================
# TOKEN (RAILWAY)
# =========================

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    logging.critical("TOKEN não encontrado")
    raise SystemExit()

bot.run(TOKEN)
