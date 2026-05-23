import discord
from discord.ext import commands
from discord import app_commands
import os
import time
import psutil

# =========================
# 📦 VERSIONAMENTO OFICIAL
# =========================

VERSION_NAME = "V1.3.0.1"
VERSION_DESCRIPTION = "Correção do sistema híbrido global/guild"
VERSION_FULL = f"{VERSION_NAME} | {VERSION_DESCRIPTION}"

PROJECT_NAME = "Conexão Roleplay"

GUILD_ID = 1465461083757351061
GUILD = discord.Object(id=GUILD_ID)

# =========================
# 🖼️ ASSETS OFICIAIS
# =========================

ASSETS = {
    "banner_institucional": "https://i.postimg.cc/ZRKBv2hx/1000038222-1.png",
    "banner_global": "https://i.postimg.cc/nhScwr8R/IMG-20260517-WA0030.jpg",
    "logo": "https://i.postimg.cc/6pnGkC0h/file-0000000071f071f9a14ca207e3220fbd.png",
    "banner_ticket": "https://i.postimg.cc/GhBDjWTV/WA-1779121191958-1.jpg",
    "banner_admin": "https://i.postimg.cc/G2qDMrQm/file-0000000028e871f585091163dcdcd281.png",
    "logo_historica": "https://i.postimg.cc/rFb1XVLW/file-000000006aa861f893b69b785193ffb7-1-1.png"
}

# =========================
# 🤖 BOT
# =========================

intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

# =========================
# ⏱️ UPTIME
# =========================

start_time = time.time()

def uptime():
    t = int(time.time() - start_time)
    return f"{t//3600}h {(t%3600)//60}m {t%60}s"

# =========================
# 🎨 EMBED BASE
# =========================

def embed_base(title, desc=None):
    e = discord.Embed(
        title=title,
        description=desc,
        color=0x145A32
    )

    e.set_thumbnail(url=ASSETS["logo"])

    e.set_footer(
        text=f"{PROJECT_NAME} • {VERSION_NAME}",
        icon_url=ASSETS["logo"]
    )

    return e

# =========================
# 📊 1. PING
# =========================

@bot.tree.command(name="ping")
async def ping(interaction: discord.Interaction):

    e = embed_base("🏓 Latência do Sistema RP")

    e.add_field(
        name="Ping Atual",
        value=f"{round(bot.latency * 1000)}ms",
        inline=False
    )

    e.set_image(url=ASSETS["banner_global"])

    await interaction.response.send_message(embed=e)

# =========================
# 📦 2. INFO
# =========================

@bot.tree.command(name="info")
async def info(interaction: discord.Interaction):

    e = embed_base("📦 Sistema Conexão Roleplay")

    e.add_field(
        name="Versão",
        value=VERSION_FULL,
        inline=False
    )

    e.add_field(
        name="Projeto",
        value=PROJECT_NAME,
        inline=False
    )

    e.add_field(
        name="Arquitetura",
        value="Sistema RP estruturado",
        inline=False
    )

    e.set_image(url=ASSETS["banner_institucional"])

    await interaction.response.send_message(embed=e)

# =========================
# 🖥️ 3. STATUS
# =========================

@bot.tree.command(name="status")
async def status(interaction: discord.Interaction):

    e = embed_base("🖥️ Monitoramento do Sistema")

    e.add_field(
        name="CPU",
        value=f"{psutil.cpu_percent()}%",
        inline=True
    )

    e.add_field(
        name="RAM",
        value=f"{psutil.virtual_memory().percent}%",
        inline=True
    )

    e.add_field(
        name="Uptime",
        value=uptime(),
        inline=False
    )

    e.set_image(url=ASSETS["banner_admin"])

    await interaction.response.send_message(embed=e)

# =========================
# 🎫 4. TICKET
# =========================

@bot.tree.command(name="ticket")
async def ticket(interaction: discord.Interaction):

    e = embed_base("🎫 Central de Suporte")

    e.add_field(
        name="Status",
        value="Sistema operacional",
        inline=False
    )

    e.add_field(
        name="Atendimento",
        value="Abra um ticket para suporte da Staff",
        inline=False
    )

    e.set_image(url=ASSETS["banner_ticket"])

    await interaction.response.send_message(embed=e)

# =========================
# ⚠️ 5. WARN
# =========================

@bot.tree.command(name="warn")
@app_commands.checks.has_permissions(kick_members=True)
async def warn(
    interaction: discord.Interaction,
    usuario: discord.Member,
    motivo: str
):

    e = embed_base("⚠️ Advertência Registrada")

    e.add_field(
        name="Usuário",
        value=usuario.mention,
        inline=False
    )

    e.add_field(
        name="Motivo",
        value=motivo,
        inline=False
    )

    e.add_field(
        name="Moderador",
        value=interaction.user.mention,
        inline=False
    )

    await interaction.response.send_message(embed=e)

# =========================
# 👢 6. KICK
# =========================

@bot.tree.command(name="kick")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(
    interaction: discord.Interaction,
    usuario: discord.Member,
    motivo: str
):

    await usuario.kick(reason=motivo)

    e = embed_base("👢 Usuário Expulso")

    e.add_field(
        name="Usuário",
        value=usuario.mention,
        inline=False
    )

    e.add_field(
        name="Motivo",
        value=motivo,
        inline=False
    )

    await interaction.response.send_message(embed=e)

# =========================
# 🔨 7. BAN
# =========================

@bot.tree.command(name="ban")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(
    interaction: discord.Interaction,
    usuario: discord.Member,
    motivo: str
):

    await usuario.ban(reason=motivo)

    e = embed_base("🔨 Usuário Banido")

    e.add_field(
        name="Usuário",
        value=usuario.mention,
        inline=False
    )

    e.add_field(
        name="Motivo",
        value=motivo,
        inline=False
    )

    await interaction.response.send_message(embed=e)

# =========================
# 🔒 8. LOCK
# =========================

@bot.tree.command(name="lock")
@app_commands.checks.has_permissions(manage_channels=True)
async def lock(interaction: discord.Interaction):

    overwrite = interaction.channel.overwrites_for(
        interaction.guild.default_role
    )

    overwrite.send_messages = False

    await interaction.channel.set_permissions(
        interaction.guild.default_role,
        overwrite=overwrite
    )

    await interaction.response.send_message(
        "🔒 Canal bloqueado"
    )

# =========================
# 🔓 9. UNLOCK
# =========================

@bot.tree.command(name="unlock")
@app_commands.checks.has_permissions(manage_channels=True)
async def unlock(interaction: discord.Interaction):

    overwrite = interaction.channel.overwrites_for(
        interaction.guild.default_role
    )

    overwrite.send_messages = True

    await interaction.channel.set_permissions(
        interaction.guild.default_role,
        overwrite=overwrite
    )

    await interaction.response.send_message(
        "🔓 Canal desbloqueado"
    )

# =========================
# 📢 10. ANÚNCIO
# =========================

@bot.tree.command(name="anuncio")
@app_commands.checks.has_permissions(manage_guild=True)
async def anuncio(
    interaction: discord.Interaction,
    titulo: str,
    mensagem: str
):

    e = embed_base(titulo, mensagem)

    e.set_image(url=ASSETS["banner_global"])

    await interaction.response.send_message(embed=e)

# =========================
# 🧾 11. EMBED
# =========================

@bot.tree.command(name="embed")
async def embed(
    interaction: discord.Interaction,
    titulo: str,
    mensagem: str
):

    e = embed_base(titulo, mensagem)

    await interaction.response.send_message(embed=e)

# =========================
# 📜 12. REGRAS
# =========================

@bot.tree.command(name="regras")
async def regras(interaction: discord.Interaction):

    e = embed_base("📜 Regras Oficiais")

    e.set_image(url=ASSETS["banner_institucional"])

    await interaction.response.send_message(embed=e)

# =========================
# 🌐 13. SERVIDOR
# =========================

@bot.tree.command(name="servidor")
async def servidor(interaction: discord.Interaction):

    g = interaction.guild

    e = embed_base("🌐 Informações do Servidor")

    e.add_field(
        name="Nome",
        value=g.name,
        inline=False
    )

    e.add_field(
        name="Membros",
        value=g.member_count,
        inline=False
    )

    e.set_image(url=ASSETS["banner_global"])

    await interaction.response.send_message(embed=e)

# =========================
# 🔁 SYNC HÍBRIDO
# =========================

@bot.event
async def on_ready():

    print("===================================")
    print("LOGADO:", bot.user)
    print("VERSÃO:", VERSION_FULL)
    print("SESSÃO: SISTEMA RP HÍBRIDO")

    try:

        guild_sync = await bot.tree.sync(guild=GUILD)
        global_sync = await bot.tree.sync()

        print("GUILD SYNC:", len(guild_sync))
        print("GLOBAL SYNC:", len(global_sync))

        print(
            "COMANDOS:",
            [c.name for c in bot.tree.get_commands()]
        )

    except Exception as e:
        print("SYNC ERROR:", e)

    print("BOT PRONTO")
    print("===================================")

# =========================
# 🔑 TOKEN
# =========================

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise SystemExit("TOKEN ausente")

bot.run(TOKEN)
