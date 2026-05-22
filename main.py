import discord
from discord.ext import commands
from discord import app_commands
import os
import time
import psutil
import logging

# =========================
# 📦 VERSIONAMENTO PADRÃO
# =========================

BASE_VERSION = "1.2.8"
PATCH_VERSION = 7

VERSION = f"{BASE_VERSION}.{PATCH_VERSION}"

UPDATE_TYPE = (
    "Atualização"
    if PATCH_VERSION == 0
    else f"Correção da {BASE_VERSION}"
)

PROJECT_NAME = "Conexão Roleplay"

PROJECT_DESCRIPTION = (
    "Bot oficial do projeto Conexão Roleplay, responsável por automação, "
    "administração, monitoramento e integração de sistemas."
)

LAST_UPDATE = {
    "version": VERSION,
    "type": UPDATE_TYPE,
    "description": "Estabilização completa do sistema de slash commands",
    "changes": [
        "Reforço do setup_hook de sync",
        "Correção de cache de comandos no Discord",
        "Melhoria de estabilidade do CommandTree",
        "Ajustes de deploy em ambiente Railway/Host",
        "Padronização de logs de boot"
    ]
}

# =========================
# 🎨 ASSETS
# =========================

LOGO = "https://i.postimg.cc/6pnGkC0h/file-0000000071f071f9a14ca207e3220fbd.png"

EMBED_COLOR = 0x145A32
FOOTER_TEXT = "Conexão Roleplay • Sistema Oficial"

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

def embed_base(embed: discord.Embed):
    embed.set_thumbnail(url=LOGO)
    embed.set_footer(text=FOOTER_TEXT, icon_url=LOGO)
    return embed

# =========================
# 🛡️ SYNC FORTE
# =========================

@bot.event
async def setup_hook():
    try:
        print(">>> [SYNC] INICIANDO <<<")

        guild = discord.Object(id=GUILD_ID)

        await bot.wait_until_ready()

        # limpa cache guild
        bot.tree.clear_commands(guild=guild)

        # sync guild (rápido e confiável)
        synced = await bot.tree.sync(guild=guild)

        print(f">>> [SYNC] {len(synced)} comandos sincronizados")

        for cmd in synced:
            print(f" - /{cmd.name}")

        print(">>> [SYNC] FINALIZADO <<<")

    except Exception as e:
        logging.error(f"Erro no sync: {e}")

# =========================
# READY
# =========================

@bot.event
async def on_ready():
    print(">>> ON_READY <<<")
    print(f">>> BOT: {bot.user}")
    print(f">>> VERSION: {VERSION}")

    await bot.change_presence(
        activity=discord.Game(name=f"{PROJECT_NAME} {VERSION}")
    )

# =========================
# 13 COMANDOS SLASH
# =========================

# 1
@bot.tree.command(name="ping", description="Latência do bot")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"🏓 {round(bot.latency*1000)}ms")

# 2
@bot.tree.command(name="info", description="Informações do sistema")
async def info(interaction: discord.Interaction):
    embed = discord.Embed(title="Info", description=PROJECT_DESCRIPTION, color=EMBED_COLOR)
    embed_base(embed)
    await interaction.response.send_message(embed=embed)

# 3
@bot.tree.command(name="status", description="Status do sistema")
async def status(interaction: discord.Interaction):
    embed = discord.Embed(title="Status", color=EMBED_COLOR)
    embed.add_field(name="CPU", value=f"{psutil.cpu_percent()}%")
    embed.add_field(name="RAM", value=f"{psutil.virtual_memory().percent}%")
    embed.add_field(name="Uptime", value=uptime())
    embed_base(embed)
    await interaction.response.send_message(embed=embed)

# 4
@bot.tree.command(name="ticket", description="Sistema de tickets")
async def ticket(interaction: discord.Interaction):
    await interaction.response.send_message("🎫 Sistema de tickets ativo")

# 5
@bot.tree.command(name="limpar", description="Limpa mensagens")
@app_commands.checks.has_permissions(manage_messages=True)
async def limpar(interaction: discord.Interaction, quantidade: int):
    await interaction.channel.purge(limit=quantidade)
    await interaction.response.send_message("🧹 Limpo", ephemeral=True)

# 6
@bot.tree.command(name="warn", description="Advertência")
@app_commands.checks.has_permissions(kick_members=True)
async def warn(interaction: discord.Interaction, usuario: discord.Member, motivo: str):
    await interaction.response.send_message(f"⚠️ {usuario} advertido: {motivo}")

# 7
@bot.tree.command(name="kick", description="Expulsar usuário")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, usuario: discord.Member, motivo: str):
    await usuario.kick(reason=motivo)
    await interaction.response.send_message("👢 Kick aplicado")

# 8
@bot.tree.command(name="ban", description="Banir usuário")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, usuario: discord.Member, motivo: str):
    await usuario.ban(reason=motivo)
    await interaction.response.send_message("🔨 Ban aplicado")

# 9
@bot.tree.command(name="lock", description="Trancar canal")
@app_commands.checks.has_permissions(manage_channels=True)
async def lock(interaction: discord.Interaction):
    overwrite = interaction.channel.overwrites_for(interaction.guild.default_role)
    overwrite.send_messages = False
    await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
    await interaction.response.send_message("🔒 Canal bloqueado")

# 10
@bot.tree.command(name="unlock", description="Destrancar canal")
@app_commands.checks.has_permissions(manage_channels=True)
async def unlock(interaction: discord.Interaction):
    overwrite = interaction.channel.overwrites_for(interaction.guild.default_role)
    overwrite.send_messages = True
    await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
    await interaction.response.send_message("🔓 Canal liberado")

# 11
@bot.tree.command(name="anuncio", description="Fazer anúncio")
@app_commands.checks.has_permissions(manage_guild=True)
async def anuncio(interaction: discord.Interaction, canal: discord.TextChannel, titulo: str, mensagem: str):
    embed = discord.Embed(title=titulo, description=mensagem, color=EMBED_COLOR)
    embed_base(embed)
    await canal.send(embed=embed)
    await interaction.response.send_message("📢 Enviado", ephemeral=True)

# 12
@bot.tree.command(name="regras", description="Regras do servidor")
async def regras(interaction: discord.Interaction):
    await interaction.response.send_message("📜 Regras do servidor")

# 13
@bot.tree.command(name="servidor", description="Info servidor")
async def servidor(interaction: discord.Interaction):
    g = interaction.guild
    await interaction.response.send_message(f"🌐 {g.name} | {g.member_count} membros")

# =========================
# TOKEN
# =========================

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise SystemExit("TOKEN ausente")

bot.run(TOKEN)
