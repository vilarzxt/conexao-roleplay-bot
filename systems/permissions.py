import discord

# =========================
# 🔒 ACL DINÂMICA
# V1.3.1 - PERMISSIONS ENGINE
# =========================

async def build_ticket_permissions(
    guild: discord.Guild,
    user: discord.Member,
    categoria: str
):

    # =========================
    # 🚨 IDS DE CARGOS
    # (TEMPORÁRIO - FUTURO CONFIG)
    # =========================

    STAFF_ROLE_IDS = {

        "Denúncias": 111111111111111111,
        "Suporte": 222222222222222222,
        "Financeiro": 333333333333333333,
        "Parcerias": 444444444444444444
    }

    # =========================
    # 🔒 BASE ACL
    # =========================

    overwrites = {

        guild.default_role: discord.PermissionOverwrite(
            view_channel=False
        ),

        user: discord.PermissionOverwrite(
            view_channel=True,
            send_messages=True,
            read_message_history=True,
            attach_files=True
        )
    }

    # =========================
    # 👮 STAFF ACL
    # =========================

    role_id = STAFF_ROLE_IDS.get(categoria)

    if role_id:

        role = guild.get_role(role_id)

        if role:

            overwrites[role] = discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                manage_messages=True,
                read_message_history=True
            )

    return overwrites
