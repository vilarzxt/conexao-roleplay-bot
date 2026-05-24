import discord
from discord import app_commands

from config.settings import PROJECT_NAME, VERSION_FULL
from config.assets import ASSETS

# =========================
# 📦 COMMAND: INFO
# V1.3.1 - ORCHESTRATION LAYER
# =========================

@app_commands.command(
    name="info",
    description="Exibe informações do sistema Conexão Roleplay"
)
async def info(interaction: discord.Interaction):

    # 🧠 contexto básico
    user = interaction.user

    # 🎨 embed informativo (somente camada de apresentação)
    embed = discord.Embed(
        title="📦 Sistema Conexão Roleplay",
        description="Informações gerais do bot e arquitetura atual.",
        color=0x145A32
    )

    # 📌 dados de configuração (CONFIG LAYER)
    embed.add_field(
        name="📛 Projeto",
        value=PROJECT_NAME,
        inline=False
    )

    embed.add_field(
        name="📌 Versão",
        value=VERSION_FULL,
        inline=False
    )

    embed.add_field(
        name="🧠 Arquitetura",
        value="COMMANDS → ORQUESTRAÇÃO | SYSTEMS → EXECUÇÃO | CONFIG → DADOS",
        inline=False
    )

    embed.add_field(
        name="👤 Solicitado por",
        value=user.mention,
        inline=False
    )

    # 🖼️ branding
    embed.set_thumbnail(url=ASSETS["logo"])
    embed.set_image(url=ASSETS["banner_institucional"])

    embed.set_footer(text=f"{PROJECT_NAME} • V1.3.1")

    await interaction.response.send_message(embed=embed)
