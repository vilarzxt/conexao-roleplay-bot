import discord
from discord import app_commands

from config.settings import PROJECT_NAME
from config.assets import ASSETS

# =========================
# 🔓 COMMAND: UNLOCK
# V1.3.1 - CONTROLE DE CANAL
# =========================

@app_commands.command(
    name="unlock",
    description="Desbloqueia o canal atual para mensagens"
)
@app_commands.checks.has_permissions(manage_channels=True)
async def unlock(interaction: discord.Interaction):

    channel = interaction.channel
    moderator = interaction.user

    # 🧠 validação de contexto
    if not isinstance(channel, discord.TextChannel):
        await interaction.response.send_message(
            "❌ Este comando só pode ser usado em canais de texto.",
            ephemeral=True
        )
        return

    # ⚙️ lógica direta de desbloqueio
    overwrite = channel.overwrites_for(interaction.guild.default_role)
    overwrite.send_messages = True

    await channel.set_permissions(
        interaction.guild.default_role,
        overwrite=overwrite
    )

    # 🎨 resposta UI
    embed = discord.Embed(
        title="🔓 Canal Desbloqueado",
        description="O envio de mensagens foi reativado para @everyone.",
        color=0x145A32
    )

    embed.add_field(
        name="📍 Canal",
        value=channel.mention,
        inline=False
    )

    embed.add_field(
        name="🛡️ Moderador",
        value=moderator.mention,
        inline=False
    )

    embed.set_thumbnail(url=ASSETS["logo"])

    embed.set_footer(text=f"{PROJECT_NAME} • Controle de canal")

    await interaction.response.send_message(embed=embed)
