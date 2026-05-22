import discord
from discord.ext import commands
from discord import app_commands
import os
import time
import psutil
import logging

# =========================
# 📦 VERSIONAMENTO
# =========================

BASE_VERSION = "1.2.9"
PATCH_VERSION = 9

VERSION = f"{BASE_VERSION}.{PATCH_VERSION}"

UPDATE_TYPE = "Correções de estabilidade, interactions e sync otimizado"

PROJECT_NAME = "Conexão Roleplay"

PROJECT_DESCRIPTION = (
    "Bot oficial do projeto Conexão Roleplay, responsável por automação, "
    "administração, monitoramento e integração de sistemas."
)

# =========================
# 🎨 ASSETS
# =========================

LOGO = "https://i.postimg.cc/6pnGkC0h/file-0000000071f071f9a14ca207e3220fbd.png"
EMBED_COLOR = 0x145A32

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
# BOT
# =========================

intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

GUILD_ID = 1465461083757351061

# =========================
# EMBED BASE
# =========================

def embed_base(embed: discord.Embed):
    embed.set_thumbnail(url=LOGO)
    embed.set_footer(
        text="Conexão Roleplay • Sistema Oficial",
        icon_url=LOGO
    )
    return embed

# =========================
# 🛡️ SYNC OTIMIZADO
# =========================

@bot.event
async def setup_hook():
    print(">>> [SYNC] INICIANDO <<<")

    try:
        guild = discord.Object(id=GUILD_ID)

        # SYNC GUILD (rápido e estável para desenvolvimento/produção controlada)
        synced = await bot.tree.sync(guild=guild)

        print(f">>> [SYNC GUILD] {len(synced)} comandos")
        print(">>> [SYNC FINALIZADO] <<<")

    except Exception as e:
        print(f">>> [SYNC ERROR] {e}")

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
# ❌ HANDLER GLOBAL DE ERRO
# =========================

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    try:
        if interaction.response.is_done():
            await interaction.followup.send(f"❌ Erro: {str(error)}", ephemeral=True)
        else:
            await interaction.response.send_message(f"❌ Erro: {str(error)}", ephemeral=True)
    except:
        print(f"[ERROR HANDLER FAIL] {error}")

# =========================
# 📌 COMANDOS SLASH
# =========================

@bot.tree.command(name="ping", description="Latência do bot")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"🏓 {round(bot.latency * 1000)}ms")


@bot.tree.command(name="info", description="Informações do sistema")
async def info(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Info",
        description=PROJECT_DESCRIPTION,
        color=EMBED_COLOR
    )
    embed_base(embed)
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="status", description="Status do sistema")
async def status(interaction: discord.Interaction):
    embed = discord.Embed(title="Status", color=EMBED_COLOR)

    embed.add_field(name="CPU", value=f"{psutil.cpu_percent(interval=0.5)}%")
    embed.add_field(name="RAM", value=f"{psutil.virtual_memory().percent}%")
    embed.add_field(name="Uptime", value=uptime())

    embed_base(embed)
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="ticket", description="Sistema de tickets")
async def ticket(interaction: discord.Interaction):
    await interaction.response.send_message("🎫 Sistema de tickets ativo")


@bot.tree.command(name="limpar", description="Limpa mensagens")
@app_commands.checks.has_permissions(manage_messages=True)
async def limpar(interaction: discord.Interaction, quantidade: int):
    await interaction.response.defer(ephemeral=True)
    await interaction.channel.purge(limit=quantidade)
    await interaction.followup.send("🧹 Mensagens removidas")


@bot.tree.command(name="warn", description="Advertência")
@app_commands.checks.has_permissions(kick_members=True)
async def warn(interaction: discord.Interaction, usuario: discord.Member, motivo: str):
    await interaction.response.send_message(
        f"⚠️ {usuario.mention} advertido: {motivo}"
    )


@bot.tree.command(name="kick", description="Expulsar usuário")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, usuario: discord.Member, motivo: str):
    await interaction.response.defer()
    await usuario.kick(reason=motivo)
    await interaction.followup.send("👢 Usuário expulso")


@bot.tree.command(name="ban", description="Banir usuário")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, usuario: discord.Member, motivo: str):
    await interaction.response.defer()
    await usuario.ban(reason=motivo)
    await interaction.followup.send("🔨 Usuário banido")


@bot.tree.command(name="lock", description="Trancar canal")
@app_commands.checks.has_permissions(manage_channels=True)
async def lock(interaction: discord.Interaction):
    await interaction.channel.set_permissions(
        interaction.guild.default_role,
        send_messages=False
    )
    await interaction.response.send_message("🔒 Canal bloqueado")


@bot.tree.command(name="unlock", description="Destrancar canal")
@app_commands.checks.has_permissions(manage_channels=True)
async def unlock(interaction: discord.Interaction):
    await interaction.channel.set_permissions(
        interaction.guild.default_role,
        send_messages=True
    )
    await interaction.response.send_message("🔓 Canal liberado")


@bot.tree.command(name="anuncio", description="Fazer anúncio")
@app_commands.checks.has_permissions(manage_guild=True)
async def anuncio(
    interaction: discord.Interaction,
    canal: discord.TextChannel,
    titulo: str,
    mensagem: str
):
    embed = discord.Embed(
        title=titulo,
        description=mensagem,
        color=EMBED_COLOR
    )
    embed_base(embed)

    await canal.send(embed=embed)
    await interaction.response.send_message("📢 Anúncio enviado", ephemeral=True)


@bot.tree.command(name="regras", description="Regras do servidor")
async def regras(interaction: discord.Interaction):
    await interaction.response.send_message("📜 Regras do servidor")


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
