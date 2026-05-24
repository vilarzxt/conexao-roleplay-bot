import discord
from discord import app_commands

from config.settings import PROJECT_NAME
from config.assets import ASSETS

# ⚙️ SYSTEM LAYER (core do ticket)
# ainda vamos implementar, mas o command já depende dele
# from systems.tickets.ticket_manager import open_ticket

# =========================
# 🎫 COMMAND: TICKET
# V1.3.1 - SYSTEM DRIVEN ENTRYPOINT
# =========================

@app_commands.command(
    name="ticket",
    description="Abre o painel de suporte (sistema de tickets)"
)
async def ticket(interaction: discord.Interaction):

    user = interaction.user

    # 🧠 validação de contexto mínima
    if interaction.guild is None:
        await interaction.response.send_message(
            "❌ Este comando só pode ser usado em servidores.",
            ephemeral=True
        )
        return

    # ⚙️ FUTURO SYSTEM CALL (quando ticket_manager existir)
    # await open_ticket(interaction)

    # 🎨 UI LAYER (painel inicial do sistema)
    embed = discord.Embed(
        title="🎫 Central de Atendimento",
        description=(
            "Selecione uma categoria para abrir um ticket.\n\n"
            "📌 O sistema irá direcionar automaticamente seu atendimento."
        ),
        color=0x145A32
    )

    embed.add_field(
        name="🚨 Denúncias",
        value="Reportar usuários ou comportamentos",
        inline=False
    )

    embed.add_field(
        name="❓ Suporte",
        value="Ajuda geral e dúvidas",
        inline=False
    )

    embed.add_field(
        name="💰 Financeiro",
        value="Assuntos relacionados a pagamentos",
        inline=False
    )

    embed.add_field(
        name="🤝 Parcerias",
        value="Solicitações de parceria",
        inline=False
    )

    embed.set_thumbnail(url=ASSETS["logo"])
    embed.set_image(url=ASSETS["banner_ticket"])

    embed.set_footer(text=f"{PROJECT_NAME} • Sistema de Tickets V1.3.1")

    await interaction.response.send_message(embed=embed)
