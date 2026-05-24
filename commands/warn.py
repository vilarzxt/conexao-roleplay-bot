import discord
from discord import app_commands

from config.settings import PROJECT_NAME
from config.assets import ASSETS

# =========================
# ⚠️ COMMAND: WARN
# V1.3.1 - MODERAÇÃO BÁSICA
# =========================

@app_commands.command(
    name="warn",
    description="Aplica uma advertência em um usuário"
)
@app_commands.checks.has_permissions(kick_members=True)
async def warn(
    interaction: discord.Interaction,
    usuario: discord.Member,
    motivo: str
):

    moderator = interaction.user

    # 🎨 embed de registro de punição
    embed = discord.Embed(
        title="⚠️ Advertência Aplicada",
        color=0x145A32
    )

    embed.add_field(
        name="👤 Usuário",
        value=usuario.mention,
        inline=False
    )

    embed.add_field(
        name="📌 Motivo",
        value=motivo,
        inline=False
    )

    embed.add_field(
        name="🛡️ Moderador",
        value=moderator.mention,
        inline=False
    )

    embed.set_thumbnail(url=ASSETS["logo"])

    embed.set_footer(text=f"{PROJECT_NAME} • Sistema
