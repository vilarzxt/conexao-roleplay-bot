import discord

from systems.ticket_manager import create_ticket
from systems.templates import build_ticket_embed
from systems.views import TicketControls
from systems.auto_close import start_ticket_timer

# =========================
# 🔀 TICKET ROUTER
# V1.3.1 - FLOW COORDINATOR
# =========================

async def open_ticket_flow(
    interaction: discord.Interaction,
    categoria: str
):

    # =========================
    # 🎫 CRIAÇÃO DO TICKET
    # =========================

    channel = await create_ticket(
        interaction,
        categoria
    )

    if channel is None:
        return None

    # =========================
    # 🎨 TEMPLATE
    # =========================

    embed = build_ticket_embed(
        categoria,
        interaction.user
    )

    # =========================
    # 🧩 CONTROLES
    # =========================

    view = TicketControls()

    # =========================
    # 📨 ENVIO PRINCIPAL
    # =========================

    await channel.send(
        embed=embed,
        view=view
    )

    # =========================
    # ⏰ AUTO CLOSE
    # =========================

    await start_ticket_timer(channel)

    return channel
