import discord
from discord.ext import commands
from discord import app_commands

from config.assets import EMBED_COLOR
from systems.utils import create_embed

# =========================
# 🔒 LOCK COMMAND
# V1.3.1
# =========================

@app_commands.command(
    name="lock",
    description="Bloqueia o canal atual"
)
@app_commands.checks.has_permissions(
    manage_channels=True
)
async def lock(
    interaction: discord.Interaction
):

    overwrite = interaction.channel.overwrites_for(
        interaction.guild.default_role
    )

    overwrite.send_messages = False

    await interaction.channel.set_permissions(
        interaction.guild.default_role,
        overwrite=overwrite
    )

    embed = create_embed(
        title="🔒 Canal Bloqueado",
        description=(
            f"O canal foi bloqueado por "
            f"{interaction.user.mention}"
        ),
        color=EMBED_COLOR
    )

    await interaction.response.send_message(
        embed=embed
    )

# =========================
# 🚀 SETUP
# =========================

async def setup(bot: commands.Bot):

    bot.tree.add_command(lock)
