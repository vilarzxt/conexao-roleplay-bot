import discord
from discord import app_commands

from config.settings import PROJECT_NAME
from config.assets import ASSETS

# =========================
# 📜 COMMAND: REGRAS
# V1.3.1 - DOCUMENTAÇÃO INSTITUCIONAL
# =========================

@app_commands.command(
    name="regras",
    description="Exibe as regras oficiais do servidor"
)
async def regras(interaction: discord.Interaction):

    user = interaction.user

    embed = discord.Embed(
        title="📜 Regras Oficiais do Servidor",
        description=(
            "📌 Leia atentamente antes de interagir no servidor.\n\n"
            "1. Respeito é obrigatório entre todos os membros.\n"
            "2. Proibido spam, flood ou conteúdo ofensivo.\n"
            "3. Siga sempre as instruções da staff.\n"
            "4. Uso indevido de canais pode gerar punição.\n"
        ),
        color=0x145A32
    )

    embed.set_thumbnail(url=ASSETS["logo"])
    embed.set_image(url=ASSETS["banner_institucional"])

    embed.set_footer(
        text=f"{PROJECT_NAME} • Regras oficiais • Solicitado por {user.display_name}"
    )

    await interaction.response.send_message(embed=embed)
