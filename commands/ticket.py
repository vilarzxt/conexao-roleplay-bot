import discord

from discord.ext import commands
from discord import app_commands

from config.assets import (
    ASSETS,
    EMBED_COLOR
)

from systems.utils import create_embed

# =========================
# 🎫 TICKET COMMAND
# V1.3.1
# =========================

@app_commands.command(
    name="ticket",
    description="Abre o painel de tickets"
)
async def ticket(
    interaction: discord.Interaction
):

    embed = create_embed(
        title="🎫 Central de Suporte",
        description=(
            "Utilize o sistema de tickets "
            "para entrar em contato com "
            "a equipe administrativa."
        ),
        color=EMBED_COLOR
    )

    embed.add_field(
        name="📂 Atendimento",
        value=(
            "Selecione a categoria "
            "correspondente ao seu suporte."
        ),
        inline=False
    )

    embed.set_image(
        url=ASSETS["banner_ticket"]
    )

    await interaction.response.send_message(
        embed=embed
    )

# =========================
# 🚀 SETUP
# =========================

async def setup(bot: commands.Bot):

    bot.tree.add_command(ticket)
