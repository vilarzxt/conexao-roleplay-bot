import discord
from discord import app_commands

from config.settings import PROJECT_NAME
from config.assets import ASSETS

# =========================
# 👢 COMMAND: KICK
# V1.3.1 - MODERAÇÃO INTERMEDIÁRIA
# =========================

@app_commands.command(
    name="kick",
    description="Expulsa um usuário do servidor"
)
@app_commands.checks.has_permissions(kick_members=True)
async def kick(
    interaction: discord.Interaction,
    usuario: discord.Member,
    motivo: str
):

    moderator = interaction.user

    # 🧠 segurança básica
    if usuario == moderator:
        await interaction.response.send_message(
            "❌ Você não pode expulsar a si mesmo.",
            ephemeral=True
        )
        return

    if usuario.top_role >= moderator.top_role:
        await interaction.response.send_message(
            "❌ Você não pode expulsar alguém com cargo igual ou superior ao seu.",
            ephemeral=True
        )
        return

    # ⚙️ execução real
    await usuario.kick(reason=mot
