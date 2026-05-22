import discord
from discord.ext import commands
from discord import app_commands
import os
import time
import psutil
import logging

# =========================
# 📦 METADATA DO BOT
# =========================

VERSION = "v1.2.8"
UPDATE_TYPE = "Atualização"

PROJECT_NAME = "Conexão Roleplay"

PROJECT_DESCRIPTION = (
    "Bot oficial do projeto Conexão Roleplay, responsável por automação, "
    "monitoramento, administração e integração dos sistemas do servidor."
)

LAST_UPDATE = {
    "version": VERSION,
    "type": UPDATE_TYPE,
    "description": "Início da fase visual e implementação dos sistemas base",
    "changes": [
        "Implementação da identidade visual da v1.2.8",
        "Adição de banners institucionais",
        "Padronização visual das embeds",
        "Preparação dos sistemas administrativos",
        "Melhoria estrutural dos comandos slash",
        "Atualização da presença do sistema"
    ]
}

# =========================
# 🎨 ASSETS OFICIAIS
# =========================

BANNER_GLOBAL = "https://i.postimg.cc/nhScwr8R/IMG-20260517-WA0030.jpg"

LOGO_OFICIAL = "https://i.postimg.cc/6pnGkC0h/file-0000000071f071f9a14ca207e3220fbd.png"

BANNER_TICKET = "https://i.postimg.cc/GhBDjWTV/WA-1779121191958-1.jpg"

PAINEL_ADMIN = "https://i.postimg.cc/G2qDMrQm/file-0000000028e871f585091163dcdcd281.png"

LOGO_ORIGINAL = "https://i.postimg.cc/rFb1XVLW/file-000000006aa861f893b69b785193ffb7-1-1.png"

# =========================
# 🎨 CONFIG VISUAL
# =========================

EMBED_COLOR = 0x145A32

FOOTER_TEXT = "Conexão Roleplay • Sistema Oficial"

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

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# =========================
# ⚙️ GUILD TESTE
# =========================

ID_SERVIDOR_TESTE = 1465461083757351061

GUILD_TESTE = discord.Object(id=ID_SERVIDOR_TESTE)

# =========================
# 🎨 FUNÇÃO DE PADRONIZAÇÃO
# =========================

def setup_embed(embed: discord.Embed):

    embed.set_thumbnail(url=LOGO_OFICIAL)

    embed.set_footer(
        text=FOOTER_TEXT,
        icon_url=LOGO_OFICIAL
    )

    return embed

# =========================
# 🔄 SYNC SLASH COMMANDS
# =========================

@bot.event
async def setup_hook():

    bot.tree.clear_commands(guild=GUILD_TESTE)

    await bot.tree.sync(guild=GUILD_TESTE)

    logging.info("Comandos slash sincronizados com sucesso")

# =========================
# ✅ READY
# =========================

@bot.event
async def on_ready():

    logging.info(f"{PROJECT_NAME} online como {bot.user}")
    logging.info(f"Versão carregada: {VERSION}")
    logging.info(f"Servidores conectados: {len(bot.guilds)}")

    await bot.change_presence(
        activity=discord.Game(
            name=f"{PROJECT_NAME} • {VERSION}"
        )
    )

# =========================
# 🏓 /PING
# =========================

@bot.tree.command(
    name="ping",
    description="Mostra a latência do sistema",
    guild=GUILD_TESTE
)
async def ping(interaction: discord.Interaction):

    latency = round(bot.latency * 1000)

    status = (
        "🟢 Excelente" if latency < 120 else
        "🟡 Estável" if latency < 250 else
        "🔴 Instável"
    )

    embed = discord.Embed(
        title="🏓 Painel de Latência",
        color=EMBED_COLOR
    )

    embed.add_field(
        name="Latência",
        value=f"{latency}ms",
        inline=True
    )

    embed.add_field(
        name="Estado",
        value=status,
        inline=True
    )

    embed.set_image(url=BANNER_GLOBAL)

    setup_embed(embed)

    await interaction.response.send_message(embed=embed)

# =========================
# 📘 /INFO
# =========================

@bot.tree.command(
    name="info",
    description="Informações do sistema",
    guild=GUILD_TESTE
)
async def info(interaction: discord.Interaction):

    embed = discord.Embed(
        title="📘 Sistema Oficial do Conexão Roleplay",
        description=PROJECT_DESCRIPTION,
        color=EMBED_COLOR
    )

    embed.add_field(
        name="Projeto",
        value=PROJECT_NAME,
        inline=True
    )

    embed.add_field(
        name="Versão",
        value=VERSION,
        inline=True
    )

    embed.add_field(
        name="Tipo",
        value=UPDATE_TYPE,
        inline=True
    )

    embed.add_field(
        name="Última atualização",
        value=LAST_UPDATE["description"],
        inline=False
    )

    embed.add_field(
        name="Alterações",
        value="\n".join(
            f"• {change}"
            for change in LAST_UPDATE["changes"]
        ),
        inline=False
    )

    embed.set_image(url=BANNER_GLOBAL)

    setup_embed(embed)

    await interaction.response.send_message(embed=embed)

# =========================
# 📊 /STATUS
# =========================

@bot.tree.command(
    name="status",
    description="Painel técnico do sistema",
    guild=GUILD_TESTE
)
async def status(interaction: discord.Interaction):

    cpu = psutil.cpu_percent(interval=1)

    ram = psutil.virtual_memory().percent

    ping = round(bot.latency * 1000)

    servers = len(bot.guilds)

    uptime = get_uptime()

    state = (
        "🟢 Operacional" if ping < 150 else
        "🟡 Instável" if ping < 250 else
        "🔴 Crítico"
    )

    embed = discord.Embed(
        title="📊 Painel Técnico",
        color=EMBED_COLOR
    )

    embed.add_field(
        name="CPU",
        value=f"{cpu}%",
        inline=True
    )

    embed.add_field(
        name="RAM",
        value=f"{ram}%",
        inline=True
    )

    embed.add_field(
        name="Servidores",
        value=str(servers),
        inline=True
    )

    embed.add_field(
        name="Ping",
        value=f"{ping}ms",
        inline=True
    )

    embed.add_field(
        name="Estado",
        value=state,
        inline=True
    )

    embed.add_field(
        name="Uptime",
        value=uptime,
        inline=True
    )

    embed.set_image(url=PAINEL_ADMIN)

    setup_embed(embed)

    await interaction.response.send_message(embed=embed)

# =========================
# 🎫 /TICKET
# =========================

@bot.tree.command(
    name="ticket",
    description="Painel inicial do sistema de tickets",
    guild=GUILD_TESTE
)
async def ticket(interaction: discord.Interaction):

    embed = discord.Embed(
        title="🎫 Central de Atendimento",
        description=(
            "Bem-vindo ao sistema oficial de tickets do "
            "Conexão Roleplay."
        ),
        color=EMBED_COLOR
    )

    embed.add_field(
        name="Categorias disponíveis",
        value=(
            "• Suporte\n"
            "• Denúncias\n"
            "• Administração\n"
            "• Organizações\n"
            "• Atendimento interno"
        ),
        inline=False
    )

    embed.add_field(
        name="Sistema",
        value="Painel em desenvolvimento • v1.2.8",
        inline=False
    )

    embed.set_image(url=BANNER_TICKET)

    setup_embed(embed)

    await interaction.response.send_message(embed=embed)

# =========================
# 🔐 TOKEN
# =========================

TOKEN = os.getenv("TOKEN")

if not TOKEN:

    logging.critical(
        "TOKEN não encontrado nas variáveis de ambiente"
    )

    raise SystemExit("TOKEN ausente")

bot.run(TOKEN)
