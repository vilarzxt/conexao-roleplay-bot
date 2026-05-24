import discord
from discord import app_commands

from config.settings import PROJECT_NAME
from config.assets import ASSETS

# =========================
# 🧾 COMMAND: EMBED
# V1.3.1 - UI GENERATOR
# =========================

@app_commands.command(
    name="embed",
    description="Cria um embed personalizado"
)
async def embed(
    interaction: discord.Interaction,
    titulo: str,
    mensagem: str
):

    user = interaction.user

    # 🎨 UI LAYER ONLY
    e = discord.Embed(
        title=titulo,
        description=mensagem,
        color=0x145A32
    )

    e.set_thumbnail(url=ASSETS["logo"])
    e.set_footer(text=f"{PROJECT_NAME} • Criado por {user.display_name}")

    await interaction.response.send_message(embed=e)
