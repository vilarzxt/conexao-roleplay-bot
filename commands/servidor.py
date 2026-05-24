import discord
from discord import app_commands

from config.settings import PROJECT_NAME
from config.assets import ASSETS

# =========================
# 🌐 COMMAND: SERVIDOR
# V1.3.1 - INFO DINÂMICA DO GUILD
# =========================

@app_commands.command(
    name="servidor",
    description="Exibe informações do servidor"
)
async def servidor(interaction: discord.Interaction):

    guild = interaction.guild
    user = interaction.user

    # 🧠 validação básica de contexto
    if guild is None:
        await interaction.response.send_message(
            "❌ Este comando só pode ser usado dentro de um servidor.",
            ephemeral=True
        )
        return

    # 🎨 embed informativo
    embed = discord.Embed(
        title="🌐 Informações do Servidor",
        color=0x145A32
    )

    embed.add_field(
        name="📛 Nome",
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

    embed.add_field(
        name="👤 Solicitado por",
        value=user.mention,
        inline=False
    )

    embed.set_thumbnail(url=ASSETS["logo"])
    embed.set_image(url=ASSETS["banner_global"])

    embed.set_footer(text=f"{PROJECT_NAME} • Informações do servidor")

    await interaction.response.send_message(embed=embed)
