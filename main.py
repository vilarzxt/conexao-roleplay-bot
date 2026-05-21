import os
import discord
from discord.ext import commands

# =========================
# TOKEN
# =========================
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise RuntimeError("TOKEN não encontrado. Configure a variável de ambiente TOKEN.")

# =========================
# CONFIG
# =========================
BOT_COLOR = discord.Color.gold()

GUILD_ID = 1465461083757351061
GUILD = discord.Object(id=GUILD_ID)

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# =========================
# SETUP HOOK (SYNC LIMPO)
# =========================
async def setup_hook():
    # DEV MODE: sincroniza apenas no servidor
    await bot.tree.sync(guild=GUILD)

    # opcional: mantém global sem interferir
    await bot.tree.sync()

bot.setup_hook = setup_hook

# =========================
# READY
# =========================
@bot.event
async def on_ready():
    print(f"Bot online como: {bot.user}")

# =========================
# /PING
# =========================
@bot.tree.command(name="ping", description="Verifica latência do bot", guild=GUILD)
async def ping(interaction: discord.Interaction):

    embed = discord.Embed(
        title="🏓 Ping",
        description="Teste de conectividade do sistema.",
        color=BOT_COLOR
    )

    embed.add_field(name="Status", value="Online", inline=True)
    embed.add_field(name="Ping", value=f"{round(bot.latency * 1000)}ms", inline=True)

    await interaction.response.send_message(embed=embed)

# =========================
# /STATUS
# =========================
@bot.tree.command(name="status", description="Status do sistema", guild=GUILD)
async def status(interaction: discord.Interaction):

    embed = discord.Embed(
        title="📊 Status do Bot",
        description="Sistema operacional",
        color=BOT_COLOR
    )

    embed.add_field(name="Servidores", value=str(len(bot.guilds)), inline=True)
    embed.add_field(name="Ping", value=f"{round(bot.latency * 1000)}ms", inline=True)

    await interaction.response.send_message(embed=embed)

# =========================
# /INFO
# =========================
@bot.tree.command(name="info", description="Informações do bot", guild=GUILD)
async def info(interaction: discord.Interaction):

    embed = discord.Embed(
        title="🤖 Conexão Roleplay",
        description="Bot em desenvolvimento V1.2",
        color=BOT_COLOR
    )

    embed.add_field(name="Versão", value="V1.2", inline=True)
    embed.add_field(name="Modo", value="Guild Dev Mode", inline=True)

    await interaction.response.send_message(embed=embed)

# =========================
# RUN
# =========================
bot.run(TOKEN)
