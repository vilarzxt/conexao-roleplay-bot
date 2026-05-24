import discord

from config.settings import PROJECT_NAME
from config.assets import ASSETS

# =========================
# 🎫 TICKET MANAGER
# V1.3.1 - CORE ENGINE
# =========================

async def create_ticket(
    interaction: discord.Interaction,
    categoria: str
):

    guild = interaction.guild
    user = interaction.user

    # 🧠 segurança básica
    if guild is None:
        return None

    # =========================
    # 📂 DEFINIÇÃO DE NOME
    # =========================

    ticket_name = f"ticket-{user.name}".lower()

    # =========================
    # 🔒 PERMISSÕES BASE
    # =========================

    overwrites = {

        guild.default_role: discord.PermissionOverwrite(
            view_channel=False
        ),

        user: discord.PermissionOverwrite(
            view_channel=True,
            send_messages=True,
            read_message_history=True
        )
    }

    # =========================
    # 📁 CRIAÇÃO DO CANAL
    # =========================

    channel = await guild.create_text_channel(
        name=ticket_name,
        overwrites=overwrites,
        reason=f"Ticket criado por {user}"
    )

    # =========================
    # 🎨 EMBED INICIAL
    # =========================

    embed = discord.Embed(
        title="🎫 Ticket Criado",
        description=(
            f"Olá {user.mention}, "
            "seu ticket foi criado com sucesso."
        ),
        color=0x145A32
    )

    embed.add_field(
        name="📂 Categoria",
        value=categoria,
        inline=False
    )

    embed.add_field(
        name="🧠 Sistema",
        value="Core Engine V1.3.1",
        inline=False
    )

    embed.set_thumbnail(url=ASSETS["logo"])
    embed.set_footer(
        text=f"{PROJECT_NAME} • Sistema de Tickets"
    )

    # =========================
    # 📨 ENVIO NO TICKET
    # =========================

    await channel.send(
        content=user.mention,
        embed=embed
    )

    return channel
