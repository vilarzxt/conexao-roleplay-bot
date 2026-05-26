# =========================
# 🧠 IDENTIDADE DO BOT
# CONEXÃO ROLEPLAY
# V1.3.2
# =========================

PROJECT_NAME = "Conexão Roleplay"

VERSION_NAME = "V1.3.2"

VERSION_DESCRIPTION = (
    "Sistema operacional de tickets + "
    "dropdowns contextuais + "
    "roteamento dinâmico + "
    "estabilidade estrutural"
)

VERSION_FULL = (
    f"{VERSION_NAME} | "
    f"{VERSION_DESCRIPTION}"
)

# =========================
# 🌐 IDS DO DISCORD
# =========================

GUILD_ID = 1465461083757351061

# =========================
# ⚙️ COMPORTAMENTO DO BOT
# =========================

PREFIX = "!"

SYNC_GLOBAL = True
SYNC_GUILD = True

# =========================
# 🎫 CONFIGURAÇÕES DE TICKETS
# =========================

TICKET_SYSTEM_ENABLED = True

TICKET_CLOSE_ENABLED = True

TICKET_TRANSCRIPT_ENABLED = True

TICKET_AUTO_CLOSE_ENABLED = True

TICKET_PERSISTENT_VIEWS = True

# =========================
# ⏰ AUTO CLOSE
# =========================

AUTO_CLOSE_OPTIONS = [
    30,
    60,
    120,
    360,
    720,
    1440
]

AUTO_CLOSE_WARNING_1 = 30
AUTO_CLOSE_WARNING_2 = 15

# =========================
# 🎛️ FEATURE FLAGS
# =========================

FEATURES = {

    "tickets": True,

    "moderation": True,

    "logs": True,

    "auto_close": True,

    "transcripts": True,

    "dropdowns": True,

    "routing": True,

    "persistent_views": True
}
