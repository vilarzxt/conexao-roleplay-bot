import os
import time
import discord
from discord.ext import commands

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise RuntimeError("TOKEN não encontrado. Configure a variável de ambiente TOKEN.")

# ===== CONFIG VISUAL PADRÃO =====
BOT_COLOR = discord.Color.gold()

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# =========================
# ON READY + SYNC SLASH
# =========================
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot online como: {bot.user}")

# =========================
# /PING
# =========================
@bot.tree.command(name="ping", description="Verifica a latência e resposta do sistema do bot")
async def ping(interaction: discord.Interaction):

    start = time.time()
    latency = round(bot.latency * 1000)
    api_latency = round((time.time() - start) * 1000)

    embed = discord.Embed(
        title="🏓 Conectividade do Sistema",
        description="Medição de desempenho entre bot e API do Discord.",
        color=BOT_COLOR
    )

    embed.add_field(name="📡 Latência", value=f"{latency}ms", inline=True)
    embed.add_field(name="⚡ Resposta", value=f"{api_latency}ms", inline=True)
    embed.add_field(name="🟢 Status", value="Operacional", inline=True)

    embed.set_footer(text="Conexão Roleplay • Diagnóstico")

    await interaction.response.send_message(embed=embed)

# =========================
# /STATUS
# =========================
@bot.tree.command(name="status", description="Mostra status geral do bot e servidores ativos")
async def status(interaction: discord.Interaction):

    embed = discord.Embed(
        title="📊 Status do Sistema",
        description="Visão geral da infraestrutura do bot.",
        color=BOT_COLOR
    )

    embed.add_field(name="🌐 Servidores", value=str(len(bot.guilds)), inline=True)
    embed.add_field(name="📡 Ping", value=f"{round(bot.latency * 1000)}ms", inline=True)
    embed.add_field(name="⚙️ Estado", value="Online", inline=True)

    embed.set_footer(text="Atualização em tempo real")

    await interaction.response.send_message(embed=embed)

# =========================
# /INFO
# =========================
@bot.tree.command(name="info", description="Informações gerais do bot Conexão Roleplay")
async def info(interaction: discord.Interaction):

    embed = discord.Embed(
        title="🤖 Conexão Roleplay Bot",
        description="Sistema modular para automação e suporte da comunidade RP.",
        color=BOT_COLOR
    )

    embed.add_field(name="📌 Versão", value="V1", inline=True)
    embed.add_field(name="🌐 Servidores", value=str(len(bot.guilds)), inline=True)
    embed.add_field(name="📡 Ping", value=f"{round(bot.latency * 1000)}ms", inline=True)

    embed.add_field(
        name="🧠 Função",
        value="Automação, suporte e monitoramento de servidores.",
        inline=False
    )

    embed.set_footer(text="Conexão Roleplay • Sistema Oficial")

    await bot.start(TOKEN)
