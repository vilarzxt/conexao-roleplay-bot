import discord
from discord.ext import commands
from discord import app_commands

from config.assets import EMBED_COLOR
from systems.utils import create_embed

# =========================
# 👢 KICK COMMAND
# V1.3.1
# =========================

@app_commands.command(
    name="kick",
    description="Expulsa um usuário do servidor"
)
@app_commands.checks.has_permissions(
    kick_members=True
)
async def kick(
    interaction: discord.Interaction,
    usuario: discord.Member,
    motivo: str
):

    await usuario.kick(
        reason=motivo
    )

    embed = create_embed(
        title="👢 Usuário Expulso",
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

    bot.tree.add_command(kick)
