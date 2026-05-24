import asyncio
import discord

# =========================
# ⏰ AUTO CLOSE ENGINE
# V1.3.1 - INACTIVITY MONITOR
# =========================

# 🧠 controle simples em memória
ticket_timers = {}

# =========================
# 🚀 INICIAR MONITORAMENTO
# =========================

async def start_ticket_timer(
    channel: discord.TextChannel,
    timeout: int = 3600
):

    # cancela timer anterior
    await cancel_ticket_timer(channel.id)

    # cria nova task
    task = asyncio.create_task(
        auto_close_ticket(channel, timeout)
    )

    ticket_timers[channel.id] = task

# =========================
# ❌ CANCELAR TIMER
# =========================

async def cancel_ticket_timer(
    channel_id: int
):

    task = ticket_timers.get(channel_id)

    if task:

        task.cancel()

        del ticket_timers[channel_id]

# =========================
# 🔒 FECHAMENTO AUTOMÁTICO
# =========================

async def auto_close_ticket(
    channel: discord.TextChannel,
    timeout: int
):

    try:

        # ⏳ espera inatividade
        await asyncio.sleep(timeout)

        # 📢 aviso final
        await channel.send(
            "⏰ Ticket fechado automaticamente por inatividade."
        )

        # 🗑️ remove canal
        await channel.delete()

    except asyncio.CancelledError:
        # timer reiniciado/cancelado
        return
