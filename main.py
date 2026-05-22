import discord
from discord.ext import commands
from discord import app_commands
import os
import time
import psutil
import logging

# =========================
# 🧠 VERSIONAMENTO PADRÃO
# =========================

BASE_VERSION = "1.2.8"
PATCH_VERSION = 4

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
    "description": "Correção de estabilidade e sync de comandos",
    "changes": [
        "Hardening do setup_hook",
        "Correção do sync de slash commands",
        "Estabilização do CommandTree",
        "Correção de comandos invisíveis",
        "Logs de diagnóstico adicionados"
    ]
}

print(">>> MAIN.PY INICIADO <<<")

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
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

GUILD_ID = 1465461083757351061
GUILD_OBJ = discord.Object(id=GUILD_ID)

# =========================
# 🎨 EMBED PADRÃO
# =========================

def setup_embed(embed: discord.Embed):
    embed.set_thumbnail(url=LOGO_OFICIAL)
    embed.set_footer(text=FOOTER_TEXT, icon_url=LOGO_OFICIAL)
    return embed

# =========================
# 🔥 SETUP HOOK (SYNC HARDENED)
# =========================

@bot.event
async def setup_hook():

    print(">>> SETUP_HOOK EXECUTANDO <<<")

    try:
        synced_guild = await bot.tree.sync(guild=GUILD_OBJ)
        print(f">>> SYNC GUILD: {len(synced_guild)} comandos")

        synced_global = await bot.tree.sync()
        print(f">>> SYNC GLOBAL: {len(synced_global)} comandos")

    except Exception as e:
        logging.error(f"SYNC ERROR: {e}")
        print(">>> SYNC FAILED <<<", e)

# =========================
# 🔥 READY
# =========================

@bot.event
async def on_ready():

    print(">>> ON_READY DISPAROU <<<")
    print(f">>> BOT LOGADO COMO: {bot.user}")

    logging.info(f"{PROJECT_NAME} online")
    logging.info(f"Versão: {VERSION}")
    logging.info(f"Servidores: {len(bot.guilds)}")
    logging.info(f"Slash commands: {len(bot.tree.get_commands())}")

    await bot.change_presence(
        activity=discord.Game(name=f"{PROJECT_NAME} • {VERSION}")
    )

# =========================
# 🏓 /PING
# =========================

@bot.tree.command(
    name="ping",
    description="Mostra latência",
    guild=GUILD_OBJ
)
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

@bot.tree.command(
    name="info",
    description="Informações do sistema",
    guild=GUILD_OBJ
)
async def info(interaction: discord.Interaction):

    embed = discord.Embed(
        title="📘 Sistema Conexão Roleplay",
        description=PROJECT_DESCRIPTION,
        color=EMBED_COLOR
    )

    embed.add_field(name="Projeto", value=PROJECT_NAME, inline=True)
    embed.add_field(name="Versão", value=VERSION, inline=True)
    embed.add_field(name="Tipo", value=UPDATE_TYPE, inline=True)

    embed.add_field(
        name="Atualização",
        value=LAST_UPDATE["description"],
        inline=False
    )

    embed.add_field(
        name="Mudanças",
        value="\n".join(f"• {c}" for c in LAST_UPDATE["changes"]),
        inline=False
    )

    setup_embed(embed)
    await interaction.response.send_message(embed=embed)

# =========================
# 📊 /STATUS
# =========================

@bot.tree.command(
    name="status",
    description="Status do sistema",
    guild=GUILD_OBJ
)
async def status(interaction: discord.Interaction):

    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    ping = round(bot.latency * 1000)

    embed = discord.Embed(
        title="📊 Status",
        color=EMBED_COLOR
    )

    embed.add_field(name="CPU", value=f"{cpu}%", inline=True)
    embed.add_field(name="RAM", value=f"{ram}%", inline=True)
    embed.add_field(name="Ping", value=f"{ping}ms", inline=True)
    embed.add_field(name="Uptime", value=get_uptime(), inline=True)

    setup_embed(embed)
    await interaction.response.send_message(embed=embed)

# =========================
# 🎫 /TICKET
# =========================

@bot.tree.command(
    name="ticket",
    description="Sistema de tickets",
    guild=GUILD_OBJ
)
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

@bot.tree.command(
    name="limpar",
    description="Limpa mensagens",
    guild=GUILD_OBJ
)
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

@bot.tree.command(
    name="warn",
    description="Advertência",
    guild=GUILD_OBJ
)
@app_commands.checks.has_permissions(kick_members=True)
async def warn(interaction: discord.Interaction, usuario: discord.Member, motivo: str):

    embed = discord.Embed(
        title="⚠️ Warn",
        description=f"{usuario.mention} advertido",
        color=EMBED_COLOR
    )

    embed.add_field(name="Motivo", value=motivo, inline=False)

    setup_embed(embed)
    await interaction.response.send_message(embed=embed)

# =========================
# 👢 /KICK
# =========================

@bot.tree.command(
    name="kick",
    description="Expulsar usuário",
    guild=GUILD_OBJ
)
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, usuario: discord.Member, motivo: str):

    await usuario.kick(reason=motivo)
    await interaction.response.send_message(f"👢 {usuario.mention} expulso")

# =========================
# 🔨 /BAN
# =========================

@bot.tree.command(
    name="ban",
    description="Banir usuário",
    guild=GUILD_OBJ
)
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, usuario: discord.Member, motivo: str):

    await usuario.ban(reason=motivo)
    await interaction.response.send_message(f"🔨 {usuario.mention} banido")

# =========================
# 🔒 /LOCK
# =========================

@bot.tree.command(
    name="lock",
    description="Bloquear canal",
    guild=GUILD_OBJ
)
@app_commands.checks.has_permissions(manage_channels=True)
async def lock(interaction: discord.Interaction):

    overwrite = interaction.channel.overwrites_for(interaction.guild.default_role)
    overwrite.send_messages = False

    await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)

    await interaction.response.send_message("🔒 Canal bloqueado")

# =========================
# 🔓 /UNLOCK
# =========================

@bot.tree.command(
    name="unlock",
    description="Desbloquear canal",
    guild=GUILD_OBJ
)
@app_commands.checks.has_permissions(manage_channels=True)
async def unlock(interaction: discord.Interaction):

    overwrite = interaction.channel.overwrites_for(interaction.guild.default_role)
    overwrite.send_messages = True

    await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)

    await interaction.response.send_message("🔓 Canal desbloqueado")

# =========================
# 📢 /ANUNCIO
# =========================

@bot.tree.command(
    name="anuncio",
    description="Fazer anúncio",
    guild=GUILD_OBJ
)
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

@bot.tree.command(
    name="regras",
    description="Regras do servidor",
    guild=GUILD_OBJ
)
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

@bot.tree.command(
    name="servidor",
    description="Info servidor",
    guild=GUILD_OBJ
)
async def servidor(interaction: discord.Interaction):

    guild = interaction.guild

    embed = discord.Embed(
        title="🌐 Servidor",
        color=EMBED_COLOR
    )

    embed.add_field(name="Nome", value=guild.name, inline=True)
    embed.add_field(name="Membros", value=guild.member_count, inline=True)

    setup_embed(embed)
    await interaction.response.send_message(embed=embed)

# =========================
# 🔐 TOKEN
# =========================

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    logging.critical("TOKEN ausente")
    raise SystemExit("TOKEN ausente")

print(">>> START BOT.RUN <<<")

bot.run(TOKEN)
