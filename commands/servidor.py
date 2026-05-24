import discord

from discord.ext import commands
from discord import app_commands

from config.assets import (
    ASSETS,
    EMBED_COLOR
)

from systems.utils import create_embed

# =========================
# 🌐 SERVIDOR COMMAND
# V1.3.1
# =========================

@app_commands.command(
    name="servidor",
    description="Exibe informações do servidor"
)
async def servidor(
    interaction: discord.Interaction
):

    guild = interaction.guild

    embed = create_embed(
        title="🌐 Informações do Servidor",
        color=EMBED_COLOR
    )

    embed.add_field(
        name="🏷️ Nome",
        value=guild.name,
        inline=False
    )

    embed.add_field(
        name="👥 Membros",
        value=str(guild.member_count),
        inline=False
    )

    embed.add_field(
        name="🆔 ID",
        value=str(guild.id),
        inline=False
    )

    embed.set_image(
        url=ASSETS["banner_global"]
    )

    await interaction.response.send_message(
        embed=embed
    )

# =========================
# 🚀 SETUP
# =========================

async def setup(bot: commands.Bot):

    bot.tree.add_command(servidor)
