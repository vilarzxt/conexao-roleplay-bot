import discord

from discord.ext import commands
from discord import app_commands

from config.assets import (
    ASSETS,
    EMBED_COLOR
)

from systems.utils import create_embed

# =========================
# 📢 ANUNCIO COMMAND
# V1.3.1
# =========================

@app_commands.command(
    name="anuncio",
    description="Cria um anúncio oficial"
)
@app_commands.checks.has_permissions(
    manage_guild=True
)
async def anuncio(
    interaction: discord.Interaction,
    titulo: str,
    mensagem: str
):

    embed = create_embed(
        title=titulo,
        description=mensagem,
        color=EMBED_COLOR
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

    bot.tree.add_command(anuncio)
