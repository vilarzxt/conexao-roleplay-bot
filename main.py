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

VERSION = "v1.2.8.2"
UPDATE_TYPE = "Correção"

PROJECT_NAME = "Conexão Roleplay"

PROJECT_DESCRIPTION = (
    "Bot oficial do projeto Conexão Roleplay, responsável por automação, "
    "monitoramento, administração e integração dos sistemas do servidor."
)

LAST_UPDATE = {
    "version": VERSION,
    "type": UPDATE_TYPE,
    "description": "Correção do sistema de sincronização slash commands",
    "changes": [
        "Correção do setup_hook",
        "Correção do sync de comandos",
        "Remoção do reset incorreto de comandos",
        "Estabilização da sincronização local",
        "Correção do problema de comandos invisíveis"
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
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

# =========================
# ⚙️ GUILD TESTE
# =========================

ID_SERVIDOR_TESTE = 1465461083757351061

GUILD_TESTE = discord.Object(id=ID_SERVIDOR_TESTE)

# =========================
# 🎨 PADRONIZAÇÃO EMBEDS
# =========================

def setup_embed(embed: discord.Embed):

    embed.set_thumbnail(url=LOGO_OFICIAL)

    embed.set_footer(
        text=FOOTER_TEXT,
        icon_url=LOGO_OFICIAL
    )

    return embed

# =========================
# 🔄 SLASH COMMANDS SYNC
# =========================

@bot.event
async def setup_hook():

    guild = discord.Object(id=ID_SERVIDOR_TESTE)

    try:

        synced = await bot.tree.sync(guild=guild)

        logging.info(
            f"{len(synced)} comandos slash sincronizados"
        )

        for cmd in synced:
            logging.info(f"/{cmd.name}")

    except Exception as e:
        logging.error(e)

# =========================
# ✅ READY
# =========================

@bot.event
async def on_ready():

    logging.info(
        f"{PROJECT_NAME} online como {bot.user}"
    )

    logging.info(
        f"Versão carregada: {VERSION}"
    )

    logging.info(
        f"Servidores conectados: {len(bot.guilds)}"
    )

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

    embed.add_field(name="CPU", value=f"{cpu}%", inline=True)
    embed.add_field(name="RAM", value=f"{ram}%", inline=True)
    embed.add_field(name="Servidores", value=str(servers), inline=True)

    embed.add_field(name="Ping", value=f"{ping}ms", inline=True)
    embed.add_field(name="Estado", value=state, inline=True)
    embed.add_field(name="Uptime", value=uptime, inline=True)

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
            "Bem-vindo ao sistema oficial de tickets "
            "do Conexão Roleplay."
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

    embed.set_image(url=BANNER_TICKET)

    setup_embed(embed)

    await interaction.response.send_message(embed=embed)

# =========================
# 🧹 /LIMPAR
# =========================

@bot.tree.command(
    name="limpar",
    description="Limpa mensagens do canal",
    guild=GUILD_TESTE
)
@app_commands.checks.has_permissions(manage_messages=True)
async def limpar(
    interaction: discord.Interaction,
    quantidade: int
):

    await interaction.response.defer(ephemeral=True)

    deleted = await interaction.channel.purge(
        limit=quantidade
    )

    embed = discord.Embed(
        title="🧹 Limpeza Realizada",
        description=f"{len(deleted)} mensagens removidas.",
        color=EMBED_COLOR
    )

    setup_embed(embed)

    await interaction.followup.send(
        embed=embed,
        ephemeral=True
    )

# =========================
# ⚠️ /WARN
# =========================

@bot.tree.command(
    name="warn",
    description="Aplica advertência",
    guild=GUILD_TESTE
)
@app_commands.checks.has_permissions(kick_members=True)
async def warn(
    interaction: discord.Interaction,
    usuario: discord.Member,
    motivo: str
):

    embed = discord.Embed(
        title="⚠️ Advertência Aplicada",
        color=EMBED_COLOR
    )

    embed.add_field(
        name="Usuário",
        value=usuario.mention,
        inline=True
    )

    embed.add_field(
        name="Motivo",
        value=motivo,
        inline=False
    )

    setup_embed(embed)

    await interaction.response.send_message(embed=embed)

# =========================
# 👢 /KICK
# =========================

@bot.tree.command(
    name="kick",
    description="Expulsa um usuário",
    guild=GUILD_TESTE
)
@app_commands.checks.has_permissions(kick_members=True)
async def kick(
    interaction: discord.Interaction,
    usuario: discord.Member,
    motivo: str
):

    await usuario.kick(reason=motivo)

    embed = discord.Embed(
        title="👢 Usuário Expulso",
        color=EMBED_COLOR
    )

    embed.add_field(
        name="Usuário",
        value=usuario.mention,
        inline=True
    )

    embed.add_field(
        name="Motivo",
        value=motivo,
        inline=False
    )

    setup_embed(embed)

    await interaction.response.send_message(embed=embed)

# =========================
# 🔨 /BAN
# =========================

@bot.tree.command(
    name="ban",
    description="Bane um usuário",
    guild=GUILD_TESTE
)
@app_commands.checks.has_permissions(ban_members=True)
async def ban(
    interaction: discord.Interaction,
    usuario: discord.Member,
    motivo: str
):

    await usuario.ban(reason=motivo)

    embed = discord.Embed(
        title="🔨 Usuário Banido",
        color=EMBED_COLOR
    )

    embed.add_field(
        name="Usuário",
        value=usuario.mention,
        inline=True
    )

    embed.add_field(
        name="Motivo",
        value=motivo,
        inline=False
    )

    setup_embed(embed)

    await interaction.response.send_message(embed=embed)

# =========================
# 🔒 /LOCK
# =========================

@bot.tree.command(
    name="lock",
    description="Bloqueia o canal atual",
    guild=GUILD_TESTE
)
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

    embed = discord.Embed(
        title="🔒 Canal Bloqueado",
        description=f"{interaction.channel.mention} bloqueado.",
        color=EMBED_COLOR
    )

    setup_embed(embed)

    await interaction.response.send_message(embed=embed)

# =========================
# 🔓 /UNLOCK
# =========================

@bot.tree.command(
    name="unlock",
    description="Desbloqueia o canal atual",
    guild=GUILD_TESTE
)
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

    embed = discord.Embed(
        title="🔓 Canal Desbloqueado",
        description=f"{interaction.channel.mention} desbloqueado.",
        color=EMBED_COLOR
    )

    setup_embed(embed)

    await interaction.response.send_message(embed=embed)

# =========================
# 📢 /ANUNCIO
# =========================

@bot.tree.command(
    name="anuncio",
    description="Envia anúncio em embed",
    guild=GUILD_TESTE
)
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

    embed.set_image(url=BANNER_GLOBAL)

    setup_embed(embed)

    await canal.send(embed=embed)

    confirm = discord.Embed(
        title="📢 Anúncio Enviado",
        description=f"Anúncio enviado para {canal.mention}",
        color=EMBED_COLOR
    )

    setup_embed(confirm)

    await interaction.response.send_message(
        embed=confirm,
        ephemeral=True
    )

# =========================
# 📜 /REGRAS
# =========================

@bot.tree.command(
    name="regras",
    description="Mostra as regras do servidor",
    guild=GUILD_TESTE
)
async def regras(interaction: discord.Interaction):

    embed = discord.Embed(
        title="📜 Regras Oficiais",
        description=(
            "Leia atentamente as regras "
            "do Conexão Roleplay."
        ),
        color=EMBED_COLOR
    )

    embed.add_field(
        name="Diretrizes",
        value=(
            "• Respeite todos os membros\n"
            "• Evite spam\n"
            "• Proibido divulgação\n"
            "• Siga as orientações da staff"
        ),
        inline=False
    )

    embed.set_image(url=BANNER_GLOBAL)

    setup_embed(embed)

    await interaction.response.send_message(embed=embed)

# =========================
# 🌐 /SERVIDOR
# =========================

@bot.tree.command(
    name="servidor",
    description="Informações do servidor",
    guild=GUILD_TESTE
)
async def servidor(interaction: discord.Interaction):

    guild = interaction.guild

    embed = discord.Embed(
        title="🌐 Informações do Servidor",
        color=EMBED_COLOR
    )

    embed.add_field(
        name="Nome",
        value=guild.name,
        inline=True
    )

    embed.add_field(
        name="Membros",
        value=str(guild.member_count),
        inline=True
    )

    embed.add_field(
        name="Canais",
        value=str(len(guild.channels)),
        inline=True
    )

    embed.add_field(
        name="Cargos",
        value=str(len(guild.roles)),
        inline=True
    )

    embed.set_image(url=BANNER_GLOBAL)

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
