import discord

from discord.ext import commands
from discord import app_commands

from config.assets import (
    ASSETS,
    EMBED_COLOR
)

from systems.utils import create_embed

# =========================
# 🏓 PING COMMAND
# V1.3.1
# =========================

@app_commands.command(
    name="ping",
    description="Exibe a latência do bot"
)
async def ping(
    interaction: discord.Interaction
):

    latency = round(
        interaction.client.latency * 1000
    )

    embed = create_embed(
        title="🏓 Latência do Sistema",
        color=EMBED_COLOR
    )

    embed.add_field(
        name="📡 Ping Atual",
        value=f"{latency}ms",
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

    bot.tree.add_command(ping)
