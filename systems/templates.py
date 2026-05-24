import discord

from config.assets import ASSETS
from config.settings import PROJECT_NAME

# =========================
# 📂 TICKET TEMPLATES
# V1.3.1 - CATEGORY ENGINE
# =========================

TICKET_TEMPLATES = {

    # =========================
    # 🚨 DENÚNCIAS
    # =========================

    "Denúncias": {

        "title": "🚨 Central de Denúncias",

        "description": (
            "Descreva detalhadamente a denúncia.\n\n"
            "📌 Envie provas sempre que possível."
        ),

        "color": 0xB03A2E
    },

    # =========================
    # ❓ SUPORTE
    # =========================

    "Suporte": {

        "title": "❓ Central de Suporte",

        "description": (
            "Explique sua dúvida ou problema.\n\n"
            "📌 Nossa equipe responderá em breve."
        ),

        "color": 0x145A32
    },

    # =========================
    # 💰 FINANCEIRO
    # =========================

    "Financeiro": {

        "title": "💰 Atendimento Financeiro",

        "description": (
            "Informe detalhes relacionados "
            "ao pagamento ou compra."
        ),

        "color": 0xB9770E
    },

    # =========================
    # 🤝 PARCERIAS
    # =========================

    "Parcerias": {

        "title": "🤝 Central de Parcerias",

        "description": (
            "Envie sua proposta comercial "
            "ou solicitação de parceria."
        ),

        "color": 0x1F618D
    }
}

# =========================
# 🎨 GERADOR DE EMBED
# =========================

def build_ticket_embed(
    categoria: str,
    usuario: discord.Member
):

    template = TICKET_TEMPLATES.get(categoria)

    # fallback de segurança
    if not template:

        template = {

            "title": "🎫 Ticket",

            "description": "Ticket criado.",

            "color": 0x145A32
        }

    # =========================
    # 🎨 EMBED
    # =========================

    embed = discord.Embed(
        title=template["title"],
        description=template["description"],
        color=template["color"]
    )

    embed.add_field(
        name="👤 Usuário",
        value=usuario.mention,
        inline=False
    )

    embed.add_field(
        name="📂 Categoria",
        value=categoria,
        inline=False
    )

    embed.set_thumbnail(url=ASSETS["logo"])

    embed.set_footer(
        text=f"{PROJECT_NAME} • Sistema de Tickets"
    )

    return embed
