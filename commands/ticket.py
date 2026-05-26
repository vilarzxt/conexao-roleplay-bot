import discord
from discord.ext import commands
from discord import app_commands

from config.assets import ASSETS, EMBED_COLOR, TICKET_FOOTER
from config.settings import VERSION_NAME, TICKET_SYSTEM_ENABLED

from systems.utils import create_embed
from systems.views import TicketPanelView


# =========================
# 🎫 TICKET COMMAND
# V1.3.2
# =========================

@app_commands.command(
    name="ticket",
    description="Realiza o deploy do painel de tickets"
)
async def ticket(interaction: discord.Interaction):

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
    # 🧠 EMBED
    # =========================

    embed = create_embed(
        title="🎫 Central Oficial de Atendimento",
        description=(
            "Bem-vindo à Central de Atendimento da Conexão Roleplay.\n\n"
            "Utilize o sistema abaixo para abrir um ticket diretamente com o setor responsável.\n\n"
            "Cada categoria possui uma equipe especializada para suporte mais rápido e eficiente."
        ),
        color=EMBED_COLOR
    )

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

    embed.add_field(
        name="📌 Informações",
        value=(
            "• Evite múltiplos tickets.\n"
            "• Envie provas quando possível.\n"
            "• Aguarde atendimento da equipe."
        ),
        inline=False
    )

    embed.add_field(
        name="⏰ Tempo Médio",
        value="O tempo pode variar conforme a demanda da equipe.",
        inline=False
    )

    embed.set_image(url=ASSETS["banner_ticket"])

    embed.set_footer(text=f"{TICKET_FOOTER} • {VERSION_NAME}")

    # =========================
    # 🚀 RESPONSE (CORREÇÃO CRÍTICA)
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
