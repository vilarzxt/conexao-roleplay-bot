import discord
from discord import app_commands

from config.settings import PROJECT_NAME
from config.assets import ASSETS

# ⚙️ SYSTEM (camada de execução real)
# Esse import vai existir quando criarmos o system
# from systems.status import get_system_status

# =========================
# 🖥️ COMMAND: STATUS
# V1.3.1 - SYSTEM DRIVEN
# =========================

@app_commands.command(
    name="status",
    description="Exibe o status do sistema (CPU, RAM e uptime)"
)
async def status(interaction: discord.Interaction):

    user = interaction.user

    # ⚙️ CHAMADA DE SYSTEM (futuro real)
    # system_data = get_system_status()

    # 🔧 fallback temporário (até system existir)
    import psutil
    import time

    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    uptime = int(time.time())

    # 🎨 UI LAYER ONLY
    embed = discord.Embed(
        title="🖥️ Status do Sistema",
        description="Monitoramento em tempo real do bot.",
        color=0x145A32
    )

    embed.add_field(
        name="🧠 CPU",
        value=f"{cpu}%",
        inline=True
    )

    embed.add_field(
        name="💾 RAM",
        value=f"{ram}%",
        inline=True
    )

    embed.add_field(
        name="⏱️ Uptime (raw)",
        value=f"{uptime}",
        inline=False
    )

    embed.add_field(
        name="👤 Solicitado por",
        value=user.mention,
        inline=False
    )

    embed.set_thumbnail(url=ASSETS["logo"])
    embed.set_image(url=ASSETS["banner_admin"])

    embed.set_footer(text=f"{PROJECT_NAME} • V1.3.1")

    await interaction.response.send_message(embed=embed)
