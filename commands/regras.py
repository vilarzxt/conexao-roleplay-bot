import discord

from discord.ext import commands
from discord import app_commands

from config.assets import (
    ASSETS,
    EMBED_COLOR
)

from systems.utils import create_embed

# =========================
# 📜 REGRAS COMMAND
# V1.3.1
# =========================

@app_commands.command(
    name="regras",
    description="Exibe as regras oficiais"
)
async def regras(
    interaction: discord.Interaction
):

    embed = create_embed(
        title="📜 Regras Oficiais",
        description=(
            "Respeite todos os membros.\n"
            "Evite spam, flood ou toxicidade.\n"
            "Siga as orientações da Staff.\n"
            "Utilize os canais corretamente."
        ),
        color=EMBED_COLOR
    )

    embed.set_image(
        url=ASSETS["banner_institucional"]
    )

    await interaction.response.send_message(
        embed=embed
    )

# =========================
# 🚀 SETUP
# =========================

async def setup(bot: commands.Bot):

    bot.tree.add_command(regras)
