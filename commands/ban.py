import discord

from discord.ext import commands
from discord import app_commands

from config.assets import (
    EMBED_COLOR
)

from systems.utils import create_embed

# =========================
# 🔨 BAN COMMAND
# V1.3.1
# =========================

@app_commands.command(
    name="ban",
    description="Bane um usuário do servidor"
)
@app_commands.checks.has_permissions(
    ban_members=True
)
async def ban(
    interaction: discord.Interaction,
    usuario: discord.Member,
    motivo: str
):

    await usuario.ban(
        reason=motivo
    )

    embed = create_embed(
        title="🔨 Usuário Banido",
        color=EMBED_COLOR
    )

    embed.add_field(
        name="👤 Usuário",
        value=usuario.mention,
        inline=False
    )

    embed.add_field(
        name="📝 Motivo",
        value=motivo,
        inline=False
    )

    embed.add_field(
        name="🛡️ Moderador",
        value=interaction.user.mention,
        inline=False
    )

    await interaction.response.send_message(
        embed=embed
    )

# =========================
# 🚀 SETUP
# =========================

async def setup(bot: commands.Bot):

    bot.tree.add_command(ban)
