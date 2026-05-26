# =========================
# ⚡ TICKET EVENTS ENGINE
# V1.3.2 - PRODUCTION CORE
# =========================

from systems.auto_close import AutoCloseManager


# =========================
# 🧠 GLOBAL REFERENCE
# =========================

auto_close_manager: AutoCloseManager = None


# =========================
# 🚀 INITIALIZER
# =========================

def init_events(bot, auto_close: AutoCloseManager):

    global auto_close_manager
    auto_close_manager = auto_close


# =========================
# 📩 MESSAGE HANDLER
# =========================

async def handle_message(message):

    # =========================
    # ❌ IGNORA BOTS
    # =========================

    if message.author.bot:
        return

    # =========================
    # ❌ IGNORA DM
    # =========================

    if not message.guild:
        return

    # =========================
    # 🎫 CHANNEL CHECK
    # =========================

    channel = message.channel

    if not hasattr(channel, "id"):
        return

    # =========================
    # ⛔ SEM AUTO-CLOSE ATIVO
    # =========================

    if not auto_close_manager:
        return

    if not auto_close_manager.is_active(channel.id):
        return

    # =========================
    # 🔄 RESET TIMER
    # =========================

    try:
        await auto_close_manager.reset_timer(channel)

    except Exception as e:
        print(f"[TICKET_EVENTS ERROR] {e}")
