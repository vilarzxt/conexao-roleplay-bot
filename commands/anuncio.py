import discord
from discord import app_commands

from config.settings import PROJECT_NAME
from config.assets import ASSETS

# =========================
# 📢 COMMAND: ANÚNCIO
# V1.3.1 - UI INSTITUCIONAL
# =========================

@app_commands.command(
    name="anuncio",
    description="Cria um anúncio institucional"
)
@app_commands.checks.has_permissions(manage_guild=True)
async def anuncio(
    interaction: discord.Interaction,
    titulo: str,
    mensagem: str
):

    user = interaction.user

    # 🎨 embed institucional
    embed = discord.Embed(
        title=f"📢 {titulo}",
        description=mensagem,
        color=0x145A32
    )

    # 🖼️ branding institucional
    embed.set_image(url=ASSETS["banner_global"])
    embed.set_thumbnail(url=ASSETS["logo"])

    embed.set_footer(
        text=f"{PROJECT_NAME} • Anúncio oficial • {user.display_name}"
    )

    await interaction.response.send_message(embed=embed)
