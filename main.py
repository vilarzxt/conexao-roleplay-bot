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
PATCH_VERSION = 3

VERSION = f"{BASE_VERSION}.{PATCH_VERSION}"

if PATCH_VERSION == 0:
    UPDATE_TYPE = "Atualização"
else:
    UPDATE_TYPE = f"Correção da {BASE_VERSION}"

PROJECT_NAME = "Conexão Roleplay"

PROJECT_DESCRIPTION = (
    "Bot oficial do projeto Conexão Roleplay, responsável por automação, "
    "monitoramento, administração e integração dos sistemas do servidor."
)

LAST_UPDATE = {
    "version": VERSION,
    "type": UPDATE_TYPE,
    "description": "Refatoração completa do sistema de slash commands",
    "changes": [
        "Correção do setup_hook",
        "Correção do sync de comandos",
        "Remoção de conflito de registry",
        "Estabilização do CommandTree",
        "Correção de comandos invisíveis"
    ]
}

# =========================
# 🎨 ASSETS
# =========================

BANNER_GLOBAL = "https://i.postimg.cc/nhScwr8R/IMG-20260517-WA0030.jpg"
LOGO_OFICIAL = "https://i.postimg.cc/6pnGkC0h/file-0000000071f071f9a14ca207e3220fbd.png"
BANNER_TICKET = "https://i.postimg.cc/GhBDjWTV/WA-1779121191958-1.jpg"
PAINEL_ADMIN = "https://i.postimg.cc/G2qDMrQm/file-0000000028e871f585091163dcdcd281.png"

EMBED_COLOR = 0x145A32
FOOTER_TEXT = "Conexão Roleplay • Sistema Oficial"

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
    embed.set_thumbnail(url=LOGO_OFICIAL)
    embed.set_footer(text=FOOTER_TEXT, icon_url=LOGO_OFICIAL)
    return embed

# =========================
# 🛡️ SYNC HARDENED
# =========================

@bot.event
async def setup_hook():
    guild = discord.Object(id=GUILD_ID)

    try:
        await bot.wait_until_ready()

        bot.tree.clear_commands(guild=guild)

        synced = await bot.tree.sync(guild=guild)

        logging.info(f"{len(synced)} comandos sincronizados")

        for cmd in synced:
            logging.info(f"/{cmd.name}")

        logging.info("SYNC ESTÁVEL CONCLUÍDO")

    except Exception as e:
        logging.error(f"Erro no sync: {e}")

# =========================
# READY
# =========================

@bot.event
async def on_ready():
    logging.info(f"{PROJECT_NAME} online como {bot.user}")
    logging.info(f"Versão: {VERSION}")
    logging.info(f"Servidores: {len(bot.guilds)}")
    logging.info(f"Comandos carregados: {len(bot.tree.get_commands())}")

    await bot.change_presence(
        activity=discord.Game(name=f"{PROJECT_NAME} • {VERSION}")
    )

# =========================
# 🏓 /PING
# =========================

@bot.tree.command(name="ping", description="Latência do bot")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)

    embed = discord.Embed(
        title="🏓 Ping",
        description=f"{latency}ms",
        color=EMBED_COLOR
    )

    setup_embed(embed)
    await interaction.response.send_message(embed=embed)

# =========================
# 📘 /INFO
# =========================

@bot.tree.command(name="info", description="Informações do sistema")
async def info(interaction: discord.Interaction):

    embed = discord.Embed(
        title="📘 Conexão Roleplay",
        description=PROJECT_DESCRIPTION,
        color=EMBED_COLOR
    )

    embed.add_field("Projeto", PROJECT_NAME, inline=True)
    embed.add_field("Versão", VERSION, inline=True)
    embed.add_field("Tipo", UPDATE_TYPE, inline=True)

    embed.add_field(
        "Atualização",
        LAST_UPDATE["description"],
        inline=False
    )

    embed.add_field(
        "Mudanças",
        "\n".join(f"• {c}" for c in LAST_UPDATE["changes"]),
        inline=False
    )

    setup_embed(embed)
    await interaction.response.send_message(embed=embed)

# =========================
# 📊 /STATUS
# =========================

@bot.tree.command(name="status", description="Status do sistema")
async def status(interaction: discord.Interaction):

    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    ping = round(bot.latency * 1000)

    embed = discord.Embed(
        title="📊 Status do Sistema",
        color=EMBED_COLOR
    )

    embed.add_field("CPU", f"{cpu}%", inline=True)
    embed.add_field("RAM", f"{ram}%", inline=True)
    embed.add_field("Ping", f"{ping}ms", inline=True)
    embed.add_field("Uptime", get_uptime(), inline=True)

    setup_embed(embed)
    await interaction.response.send_message(embed=embed)

# =========================
# 🎫 /TICKET
# =========================

@bot.tree.command(name="ticket", description="Sistema de tickets")
async def ticket(interaction: discord.Interaction):

    embed = discord.Embed(
        title="🎫 Tickets",
        description="Sistema oficial de atendimento",
        color=EMBED_COLOR
    )

    setup_embed(embed)
    await interaction.response.send_message(embed=embed)

# =========================
# 🧹 /LIMPAR
# =========================

@bot.tree.command(name="limpar", description="Limpa mensagens")
@app_commands.checks.has_permissions(manage_messages=True)
async def limpar(interaction: discord.Interaction, quantidade: int):

    await interaction.response.defer(ephemeral=True)

    deleted = await interaction.channel.purge(limit=quantidade)

    await interaction.followup.send(
        f"🧹 {len(deleted)} mensagens removidas",
        ephemeral=True
    )

# =========================
# ⚠️ /WARN
# =========================

@bot.tree.command(name="warn", description="Advertência")
@app_commands.checks.has_permissions(kick_members=True)
async def warn(interaction: discord.Interaction, usuario: discord.Member, motivo: str):

    embed = discord.Embed(
        title="⚠️ Warn",
        description=f"{usuario.mention} advertido",
        color=EMBED_COLOR
    )

    embed.add_field("Motivo", motivo, inline=False)

    setup_embed(embed)
    await interaction.response.send_message(embed=embed)

# =========================
# 👢 /KICK
# =========================

@bot.tree.command(name="kick", description="Expulsar usuário")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, usuario: discord.Member, motivo: str):

    await usuario.kick(reason=motivo)
    await interaction.response.send_message(f"👢 {usuario.mention} expulso")

# =========================
# 🔨 /BAN
# =========================

@bot.tree.command(name="ban", description="Banir usuário")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, usuario: discord.Member, motivo: str):

    await usuario.ban(reason=motivo)
    await interaction.response.send_message(f"🔨 {usuario.mention} banido")

# =========================
# 🔒 /LOCK
# =========================

@bot.tree.command(name="lock", description="Bloquear canal")
@app_commands.checks.has_permissions(manage_channels=True)
async def lock(interaction: discord.Interaction):

    overwrite = interaction.channel.overwrites_for(interaction.guild.default_role)
    overwrite.send_messages = False

    await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)

    await interaction.response.send_message("🔒 Canal bloqueado")

# =========================
# 🔓 /UNLOCK
# =========================

@bot.tree.command(name="unlock", description="Desbloquear canal")
@app_commands.checks.has_permissions(manage_channels=True)
async def unlock(interaction: discord.Interaction):

    overwrite = interaction.channel.overwrites_for(interaction.guild.default_role)
    overwrite.send_messages = True

    await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)

    await interaction.response.send_message("🔓 Canal desbloqueado")

# =========================
# 📢 /ANUNCIO
# =========================

@bot.tree.command(name="anuncio", description="Fazer anúncio")
@app_commands.checks.has_permissions(manage_guild=True)
async def anuncio(interaction: discord.Interaction, canal: discord.TextChannel, titulo: str, mensagem: str):

    embed = discord.Embed(
        title=titulo,
        description=mensagem,
        color=EMBED_COLOR
    )

    setup_embed(embed)

    await canal.send(embed=embed)
    await interaction.response.send_message("📢 enviado", ephemeral=True)

# =========================
# 📜 /REGRAS
# =========================

@bot.tree.command(name="regras", description="Regras do servidor")
async def regras(interaction: discord.Interaction):

    embed = discord.Embed(
        title="📜 Regras",
        description="Regras do servidor",
        color=EMBED_COLOR
    )

    setup_embed(embed)
    await interaction.response.send_message(embed=embed)

# =========================
# 🌐 /SERVIDOR
# =========================

@bot.tree.command(name="servidor", description="Info servidor")
async def servidor(interaction: discord.Interaction):

    guild = interaction.guild

    embed = discord.Embed(
        title="🌐 Servidor",
        color=EMBED_COLOR
    )

    embed.add_field("Nome", guild.name, inline=True)
    embed.add_field("Membros", guild.member_count, inline=True)

    setup_embed(embed)
    await interaction.response.send_message(embed=embed)

# =========================
# TOKEN
# =========================

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    logging.critical("TOKEN ausente")
    raise SystemExit("TOKEN ausente")

bot.run(TOKEN)
