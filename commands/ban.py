import discord
from discord import app_commands

from config.settings import PROJECT_NAME
from config.assets import ASSETS

# =========================
# 🔨 COMMAND: BAN
# V1.3.1 - MODERAÇÃO CRÍTICA
# =========================

@app_commands.command(
    name="ban",
    description="Bane um usuário do servidor"
)
@app_commands.checks.has_permissions(ban_members=True)
async def ban(
    interaction: discord.Interaction,
    usuario: discord.Member,
    motivo: str
):

    moderator = interaction.user

    # 🧠 validação de segurança
    if usuario == moderator:
        await interaction.response.send_message(
            "❌ Você não pode banir a si mesmo.",
            ephemeral=True
        )
        return

    if usuario.top_role >= moderator.top_role:
        await interaction.response.send_message(
            "❌ Você não pode banir alguém com cargo igual ou superior ao seu.",
            ephemeral=True
        )
        return

    # ⚙️ execução real do ban
    await usuario.ban(reason=motivo)

    # 🎨 resposta visual (UI LAYER ONLY)
    embed = discord.Embed(
        title="🔨 Usuário Banido",
        color=0x145A32
    )

    embed.add_field(
        name="👤 Usuário",
        value=usuario.mention,
        inline=False
    )

    embed.add_field(
        name="📌 Motivo",
        value=motivo,
        inline=False
    )

    embed.add_field(
        name="🛡️ Moderador",
        value=moderator.mention,
        inline=False
    )

    embed.set_thumbnail(url=ASSETS["logo"])

    embed.set_footer(text=f"{PROJECT_NAME} • Sistema de moderação")

    await interaction.response.send_message(embed=embed)
