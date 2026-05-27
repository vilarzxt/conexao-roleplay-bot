# =========================
# 🎫 TICKET MANAGER ENGINE
# V1.3.2.8
# =========================

import discord
import datetime

from systems.permissions import can_close_ticket
from systems.transcripts import TranscriptBuilder
from systems.router import TicketRouter

from systems.views import (
    TicketManagementView
)

# =========================
# 🧠 CORE MANAGER
# =========================

class TicketManager:

    def __init__(self, bot):

        self.bot = bot
        self.router = TicketRouter(bot)
        self.transcripts = TranscriptBuilder()

    # =========================
    # 🎫 CREATE TICKET
    # =========================

    async def create_ticket(

        self,
        interaction: discord.Interaction,
        category: str,
        subcategory: str

    ):

        guild = interaction.guild
        user = interaction.user

        # =========================
        # 📂 CATEGORY
        # =========================

        category_channel = discord.utils.get(
            guild.categories,
            name="TICKETS"
        )

        # =========================
        # 📁 AUTO CREATE CATEGORY
        # =========================

        if not category_channel:

            category_channel = await guild.create_category(
                name="TICKETS"
            )

        # =========================
        # 🏷️ CHANNEL NAME
        # =========================

        clean_name = (
            user.name
            .lower()
            .replace(" ", "-")
        )

        channel_name = (
            f"ticket-{clean_name}"
        )

        # =========================
        # 🚫 DUPLICATE CHECK
        # =========================

        existing_channel = discord.utils.get(
            guild.channels,
            name=channel_name
        )

        if existing_channel:

            return existing_channel

        # =========================
        # 🔐 PERMISSIONS
        # =========================

        overwrites = {

            guild.default_role: discord.PermissionOverwrite(
                view_channel=False
            ),

            user: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True,
                attach_files=True,
                embed_links=True
            )
        }

        # =========================
        # 🎫 CREATE CHANNEL
        # =========================

        ticket_channel = await guild.create_text_channel(

            name=channel_name,

            category=category_channel,

            overwrites=overwrites,

            topic=(
                f"Ticket de {user} | "
                f"{category} | "
                f"{subcategory}"
            )
        )

        # =========================
        # 📌 OPEN EMBED
        # =========================

        embed = discord.Embed(

            title="🎫 Ticket Criado",

            description=(

                f"Olá {user.mention}.\n\n"

                "Seu ticket foi criado "
                "com sucesso.\n\n"

                f"📂 Categoria: `{category}`\n"
                f"📌 Subcategoria: `{subcategory}`"
            ),

            color=0x5865F2,

            timestamp=datetime.datetime.utcnow()
        )

        embed.add_field(

            name="📋 Informações",

            value=(

                "• Descreva seu problema.\n"
                "• Envie provas se necessário.\n"
                "• Aguarde a equipe responsável."
            ),

            inline=False
        )

        embed.set_footer(
            text="Conexão Roleplay • Sistema de Tickets"
        )

        # =========================
        # 📩 SEND PANEL
        # =========================

        await ticket_channel.send(

            content=user.mention,

            embed=embed,

            view=TicketManagementView()
        )

        # =========================
        # ✅ RETURN CHANNEL
        # =========================

        return ticket_channel

    # =========================
    # 🔒 CLOSE TICKET FLOW
    # =========================

    async def close_ticket(
        self,
        interaction: discord.Interaction,
        reason: str = "Não informado",
        rating: int = None,
        feedback: str = None
    ):

        channel = interaction.channel
        user = interaction.user
        guild = interaction.guild

        # =========================
        # 🔐 PERMISSION CHECK
        # =========================

        roles = [

            r.name.lower().replace(" ", "_")

            for r in user.roles
        ]

        if not can_close_ticket(
            roles,
            "generic"
        ):

            return await interaction.response.send_message(

                "❌ Você não tem permissão "
                "para fechar este ticket.",

                ephemeral=True
            )

        # =========================
        # 📌 FEEDBACK EMBED
        # =========================

        embed = discord.Embed(

            title="🔒 Ticket Encerrado",

            color=0xE74C3C,

            timestamp=datetime.datetime.utcnow()
        )

        embed.add_field(
            name="👤 Fechado por",
            value=user.mention,
            inline=False
        )

        embed.add_field(
            name="📌 Motivo",
            value=reason,
            inline=False
        )

        if rating is not None:

            embed.add_field(
                name="⭐ Avaliação",
                value=f"{rating}/5",
                inline=True
            )

        if feedback:

            embed.add_field(
                name="📝 Feedback",
                value=feedback,
                inline=False
            )

        # =========================
        # 📤 DM USER
        # =========================

        try:

            await user.send(

                embed=discord.Embed(

                    title="📨 Seu ticket foi encerrado",

                    description=(

                        f"Seu atendimento em "
                        f"`{channel.name}` "
                        f"foi finalizado.\n\n"

                        f"📌 Motivo: {reason}\n"

                        f"⭐ Avaliação: "
                        f"{rating if rating else 'Não informado'}"
                    ),

                    color=0x2ECC71
                )
            )

        except:
            pass

        # =========================
        # 📜 TRANSCRIPT
        # =========================

        try:

            await self.transcripts.send_transcript(

                channel=channel,
                guild=guild,
                user=user
            )

        except Exception as e:

            print(
                f"[TRANSCRIPT ERROR] {e}"
            )

        # =========================
        # 📊 LOG CHANNEL
        # =========================

        log_channel = discord.utils.get(
            guild.channels,
            name="logs-tickets"
        )

        if log_channel:

            await log_channel.send(
                embed=embed
            )

        # =========================
        # 🧹 FINALIZAÇÃO
        # =========================

        await interaction.response.send_message(

            "🔒 Ticket encerrado "
            "com sucesso.",

            ephemeral=True
        )

        await channel.delete(
            reason="Ticket fechado via sistema"
        )

# =========================
# 🚀 GLOBAL INSTANCE
# =========================

ticket_manager = None

# =========================
# 🚀 SETUP MANAGER
# =========================

def setup_ticket_manager(bot):

    global ticket_manager

    ticket_manager = TicketManager(bot)

    return ticket_manager

# =========================
# 🎫 GLOBAL CREATE FUNCTION
# =========================

async def create_ticket(

    interaction: discord.Interaction,
    category: str,
    subcategory: str

):

    if not ticket_manager:

        return None

    return await ticket_manager.create_ticket(

        interaction=interaction,

        category=category,

        subcategory=subcategory
    )
