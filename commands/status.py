import discord
import psutil
import time

from discord.ext import commands
from discord import app_commands

from config.assets import (
    ASSETS,
    EMBED_COLOR
)

from systems.utils import create_embed

# =========================
# ⏱️ UPTIME
# =========================

START_TIME = time.time()

def get_uptime():

    total = int(
        time.time() - START_TIME
    )

    horas = total // 3600
    minutos = (total % 3600) // 60
    segundos = total % 60

    return (
        f"{horas}h "
        f"{minutos}m "
        f"{segundos}s"
    )

# =========================
# 🖥️ STATUS COMMAND
# V1.3.1
# =========================

@app_commands.command(
    name="status",
    description="Exibe o status do sistema"
)
async def status(
    interaction: discord.Interaction
):

    embed = create_embed(
        title="🖥️ Monitoramento do Sistema",
        color=EMBED_COLOR
    )

    embed.add_field(
        name="⚙️ CPU",
        value=f"{psutil.cpu_percent()}%",
        inline=True
    )

    embed.add_field(
        name="🧠 RAM",
        value=(
            f"{psutil.virtual_memory().percent}%"
        ),
        inline=True
    )

    embed.add_field(
        name="⏱️ Uptime",
        value=get_uptime(),
        inline=False
    )

    embed.set_image(
        url=ASSETS["banner_admin"]
    )

    await interaction.response.send_message(
        embed=embed
    )

# =========================
# 🚀 SETUP
# =========================

async def setup(bot: commands.Bot):

    bot.tree.add_command(status)
