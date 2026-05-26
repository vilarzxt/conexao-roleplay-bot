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

# =========================
# 🎫 TICKET COMMAND
# CONEXÃO ROLEPLAY
# V1.3.2
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
    # 🧠 TICKET PANEL
    # =========================

    embed = create_embed(
        title="🎫 Central Oficial de Atendimento",
        description=(
            "Bem-vindo à Central de Atendimento "
            "da Conexão Roleplay.\n\n"

            "Utilize o sistema abaixo para abrir "
            "um ticket diretamente com o setor "
            "responsável pelo seu atendimento.\n\n"

            "Cada categoria possui uma equipe "
            "especializada para fornecer suporte "
            "mais rápido, organizado e eficiente."
        ),
        color=EMBED_COLOR
    )

    # =========================
    # 📂 CATEGORIAS
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
    # 📌 INFORMAÇÕES
    # =========================

    embed.add_field(
        name="📌 Informações Importantes",
        value=(
            "• Evite abrir múltiplos tickets.\n"
            "• Envie provas sempre que possível.\n"
            "• Aguarde o atendimento da equipe.\n"
            "• Tickets indevidos poderão ser fechados."
        ),
        inline=False
    )

    # =========================
    # ⏰ TEMPO MÉDIO
    # =========================

    embed.add_field(
        name="⏰ Tempo Médio de Resposta",
        value=(
            "O tempo de resposta pode variar "
            "de acordo com a demanda da equipe."
        ),
        inline=False
    )

    # =========================
    # 🖼️ BANNER
    # =========================

    embed.set_image(
        url=ASSETS["banner_ticket"]
    )

    # =========================
    # 🏷️ FOOTER
    # =========================

    embed.set_footer(
        text=(
            f"{TICKET_FOOTER} • "
            f"{VERSION_NAME}"
        )
    )

    # =========================
    # 🚀 RESPONSE
    # =========================

    await interaction.response.send_message(
        embed=embed
    )

# =========================
# 🚀 SETUP
# =========================

async def setup(bot: commands.Bot):

    bot.tree.add_command(ticket)
