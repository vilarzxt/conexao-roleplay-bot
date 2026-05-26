# =========================
# 🔐 PERMISSIONS ENGINE
# V1.3.2 - TICKET SYSTEM
# =========================

from typing import Dict, List, Optional


# =========================
# 🧠 HIERARQUIA BASE (NÍVEIS)
# =========================

ROLE_LEVELS = {

    # 🟢 MONITORIA (TICKETS)
    "aprendiz_monitor": 0,
    "monitor_auxiliar": 1,
    "monitor": 1,
    "sub_lider_monitor": 2,
    "monitor_lider": 2,

    # 🔵 ADMIN JOGO (NÃO É TICKET PADRÃO)
    "aprendiz_admin": 1,
    "admin_auxiliar": 2,
    "administrador": 3,
    "sub_lider_admin": 4,
    "administrador_lider": 4,
    "admin_lider": 4,

    # 🟡 SUPERVISÃO / GERÊNCIA
    "supervisor": 4,
    "supervisor_geral": 5,
    "gerente": 5,
    "gerente_geral": 5,

    # 🟠 COORDENAÇÃO
    "coordenador": 6,
    "coordenador_geral": 7,

    # 🔴 EXECUTIVO
    "diretor": 8,
    "diretor_geral": 9,
    "ceo": 10,

    # 🧠 DEV (EXCEÇÃO MÁXIMA)
    "desenvolvedor_dc": 99
}


# =========================
# 🎫 CATEGORIAS DE TICKET
# =========================

TICKET_RULES: Dict[str, Dict] = {

    # 🚨 DENÚNCIAS
    "denuncia_player": {
        "route": "MONITOR_TEAM",
        "min_level": 0
    },

    "denuncia_organizacao": {
        "route": "MONITOR_TEAM",
        "min_level": 0
    },

    "denuncia_staff": {
        "route": "EXEC_TEAM",
        "min_level": 6  # coordenador+
    },


    # ❓ DÚVIDAS & SUPORTE
    "duvidas_gerais": {
        "route": "MONITOR_TEAM",
        "min_level": 0
    },

    "suporte_tecnico": {
        "route": "TECH_TEAM",
        "min_level": 6  # coordenador+
    },

    "bug_report": {
        "route": "TECH_TEAM",
        "min_level": 6  # coord + dev consult
    },


    # 🏢 ORGANIZAÇÕES
    "organizacoes_acoes": {
        "route": "SUPERVISOR_TEAM",
        "min_level": 5  # supervisor+
    },

    "suporte_organizacional": {
        "route": "SUPERVISOR_TEAM",
        "min_level": 5
    },

    "duvidas_orgs": {
        "route": "SUPERVISOR_TEAM",
        "min_level": 5
    },


    # 💰 FINANCEIRO
    "vip_coins": {
        "route": "COORD_EXEC_TEAM",
        "min_level": 7  # coordenador geral+
    },

    "problemas_financeiros": {
        "route": "COORD_EXEC_TEAM",
        "min_level": 7
    },


    # 🤝 PARCERIAS
    "parceria_criadores": {
        "route": "COORD_TEAM",
        "min_level": 6
    },

    "parceria_projetos": {
        "route": "COORD_TEAM",
        "min_level": 6
    },

    "duvidas_parceria": {
        "route": "COORD_TEAM",
        "min_level": 6
    }
}


# =========================
# 🧠 ROLE GROUPS (TIPOS FUNCIONAIS)
# =========================

MONITOR_TEAM = [
    "aprendiz_monitor",
    "monitor_auxiliar",
    "monitor",
    "sub_lider_monitor",
    "monitor_lider"
]

ADMIN_GAME_TEAM = [
    "aprendiz_admin",
    "admin_auxiliar",
    "administrador",
    "sub_lider_admin",
    "administrador_lider"
]

SUPERVISOR_TEAM = [
    "supervisor",
    "supervisor_geral",
    "gerente",
    "gerente_geral"
]

COORD_TEAM = [
    "coordenador",
    "coordenador_geral"
]

EXEC_TEAM = [
    "diretor",
    "diretor_geral",
    "ceo"
]

DEV_TEAM = [
    "desenvolvedor_dc"
]


# =========================
# 🔐 CORE FUNCTIONS
# =========================

def get_role_level(role_name: str) -> int:
    return ROLE_LEVELS.get(role_name.lower(), -1)


def get_user_highest_level(roles: List[str]) -> int:
    return max([get_role_level(r) for r in roles], default=-1)


def can_access_ticket(user_roles: List[str], ticket_key: str) -> bool:

    rule = TICKET_RULES.get(ticket_key)

    if not rule:
        return False

    user_level = get_user_highest_level(user_roles)

    # 🧠 DEV OVERRIDE
    if "desenvolvedor_dc" in [r.lower() for r in user_roles]:
        return True

    return user_level >= rule["min_level"]


def can_close_ticket(user_roles: List[str], ticket_key: str) -> bool:

    rule = TICKET_RULES.get(ticket_key)

    if not rule:
        return False

    user_level = get_user_highest_level(user_roles)

    # 🔥 ADMIN LÍDER EXCEPTION (pode sempre fechar dentro do escopo permitido)
    if "admin_lider" in [r.lower() for r in user_roles]:
        return True

    if "desenvolvedor_dc" in [r.lower() for r in user_roles]:
        return True

    return user_level >= rule["min_level"]
