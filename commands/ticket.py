import discord

from discord.ext import commands
from discord import app_commands

from config.assets import (
    ASSETS,
    EMBED_COLOR,
    TICKET_FOOTER
)

from config.settings import (
    VERSION_NAME,
    TICKET_SYSTEM_ENABLED
)

from systems.utils import create_embed
from systems.views import TicketPanelView


# =========================
# 🎫 TICKET COMMAND
# CONEXÃO ROLEPLAY
# V1.3.2.4
# =========================

@app_commands.command(
    name="ticket",
    description="Realiza o deploy do painel de tickets"
)
async def ticket(
    interaction: discord.Interaction
):

    # =========================
    # 🔒 SYSTEM CHECK
    # =========================

    if not TICKET_SYSTEM_ENABLED:

        await interaction.response.send_message(
            "❌ O sistema de tickets está desativado.",
            ephemeral=True
        )

        return

    # =========================
    # 🧠 PANEL EMBED
    # =========================

    embed = create_embed(
        title="🎫 Central Oficial de Atendimento",

        description=(
            "Bem-vindo à Central de Atendimento "
            "da Conexão Roleplay.\n\n"

            "Selecione abaixo a categoria "
            "do atendimento para abrir "
            "um ticket automaticamente."
        ),

        color=EMBED_COLOR
    )

    # =========================
    # 📂 CATEGORIES
    # =========================

    embed.add_field(
        name="📂 Categorias Disponíveis",

        value=(
            "🚨 Central de Denúncias\n"
            "❓ Dúvidas e Reportes\n"
            "💰 Central Financeira\n"
            "🏢 Central de Organizações\n"
            "🤝 Central de Parceiros"
        ),

        inline=False
    )

    # =========================
    # 📌 INFO
    # =========================

    embed.add_field(
        name="📌 Informações",

        value=(
            "• Evite abrir múltiplos tickets.\n"
            "• Aguarde o atendimento da equipe.\n"
            "• Envie provas quando necessário."
        ),

        inline=False
    )

    # =========================
    # 🖼️ IMAGE
    # =========================

    embed.set_image(
        url=ASSETS["banner_ticket"]
    )

    # =========================
    # 🏷️ FOOTER
    # =========================

    embed.set_footer(
        text=f"{TICKET_FOOTER} • {VERSION_NAME}"
    )

    # =========================
    # 🚀 SEND PANEL
    # =========================

    await interaction.response.send_message(
        embed=embed,
        view=TicketPanelView()
    )


# =========================
# 🚀 SETUP
# =========================

async def setup(bot: commands.Bot):

    bot.tree.add_command(ticket)
