import discord

from discord.ext import commands
from discord import app_commands

from config.assets import (
    EMBED_COLOR
)

from systems.utils import create_embed

# =========================
# 🧾 EMBED COMMAND
# V1.3.1
# =========================

@app_commands.command(
    name="embed",
    description="Cria uma embed personalizada"
)
async def embed(
    interaction: discord.Interaction,
    titulo: str,
    mensagem: str
):

    custom_embed = create_embed(
        title=titulo,
        description=mensagem,
        color=EMBED_COLOR
    )

    await interaction.response.send_message(
        embed=custom_embed
    )

# =========================
# 🚀 SETUP
# =========================

async def setup(bot: commands.Bot):

    bot.tree.add_command(embed)
