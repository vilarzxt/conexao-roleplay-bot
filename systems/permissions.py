# =========================
# 🔐 PERMISSIONS ENGINE
# V1.3.2.13 - TICKET SYSTEM
# =========================

from typing import Dict, List, Optional


# =========================
# 🧪 ALIASES DE CARGO (SERVIDOR DE TESTE)
# =========================
# Mapeia o nome do cargo do servidor atual
# para o nome oficial usado em ROLE_LEVELS.
#
# 🔁 QUANDO FOR PARA PRODUÇÃO: troque apenas
# este dicionário (ou esvazie ele, se os
# cargos reais já baterem com os nomes oficiais).
# =========================

ROLE_ALIASES: Dict[str, str] = {

    "ceo_cnx": "ceo",

    "diretor": "diretor_geral",

    "moderador": "desenvolvedor_dc"
}


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

def resolve_role(role_name: str) -> str:

    key = role_name.lower()

    return ROLE_ALIASES.get(key, key)


def resolve_roles(user_roles: List[str]) -> List[str]:

    return [
        resolve_role(r)
        for r in user_roles
    ]


def get_role_level(role_name: str) -> int:

    resolved = resolve_role(role_name)

    return ROLE_LEVELS.get(resolved, -1)


def get_user_highest_level(roles: List[str]) -> int:

    return max(
        [get_role_level(r) for r in roles],
        default=-1
    )


def can_access_ticket(user_roles: List[str], ticket_key: str) -> bool:

    rule = TICKET_RULES.get(ticket_key)

    if not rule:
        return False

    resolved = resolve_roles(user_roles)

    user_level = get_user_highest_level(user_roles)

    # 🧠 DEV OVERRIDE
    if "desenvolvedor_dc" in resolved:
        return True

    return user_level >= rule["min_level"]


def can_close_ticket(user_roles: List[str], ticket_key: str) -> bool:

    rule = TICKET_RULES.get(ticket_key)

    if not rule:
        return False

    resolved = resolve_roles(user_roles)

    user_level = get_user_highest_level(user_roles)

    # 🔥 ADMIN LÍDER EXCEPTION
    if "admin_lider" in resolved:
        return True

    if "desenvolvedor_dc" in resolved:
        return True

    return user_level >= rule["min_level"]


# =========================
# 🎫 STAFF CHECK (GERENCIAMENTO GERAL)
# =========================
# Usado pelos botões do painel de ticket
# (Fechar, Atender, Configurações) — não
# depende de categoria específica, apenas
# se a pessoa tem QUALQUER cargo reconhecido
# como staff (nível >= 0).
# =========================

def is_ticket_staff(user_roles: List[str]) -> bool:

    resolved = resolve_roles(user_roles)

    # 🧠 DEV OVERRIDE
    if "desenvolvedor_dc" in resolved:
        return True

    user_level = get_user_highest_level(user_roles)

    return user_level >= 0
