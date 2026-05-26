# =========================
# 🎫 TICKET MANAGER ENGINE
# V1.3.2 - FINAL (REFATORADO)
# =========================

import discord
import datetime

from systems.permissions import can_close_ticket
from systems.transcripts import TranscriptBuilder
from systems.router import TicketRouter


# =========================
# 🧠 CORE MANAGER
# =========================

class TicketManager:

    def __init__(self, bot):

        self.bot = bot
        self.router = TicketRouter(bot)
        self.transcripts = TranscriptBuilder()


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

        roles = [r.name.lower().replace(" ", "_") for r in user.roles]

        if not can_close_ticket(roles, "generic"):

            return await interaction.response.send_message(
                "❌ Você não tem permissão para fechar este ticket.",
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
        # 📤 DM USER (NOTIFICAÇÃO)
        # =========================

        try:

            await user.send(
                embed=discord.Embed(
                    title="📨 Seu ticket foi encerrado",
                    description=(
                        f"Seu atendimento em `{channel.name}` foi finalizado.\n\n"
                        f"📌 Motivo: {reason}\n"
                        f"⭐ Avaliação: {rating if rating else 'Não informado'}"
                    ),
                    color=0x2ECC71
                )
            )

        except:
            pass


        # =========================
        # 📜 TRANSCRIPT ENGINE (UNIFICADO)
        # =========================

        try:

            await self.transcripts.send_transcript(
                channel=channel,
                guild=guild,
                user=user
            )

        except Exception as e:

            print(f"[TRANSCRIPT ERROR] {e}")


        # =========================
        # 📊 FEEDBACK LOG (STAFF)
        # =========================

        log_channel = discord.utils.get(
            guild.channels,
            name="logs-tickets"
        )

        if log_channel:

            await log_channel.send(embed=embed)


        # =========================
        # 🧹 FINALIZAÇÃO
        # =========================

        await interaction.response.send_message(
            "🔒 Ticket encerrado com sucesso.",
            ephemeral=True
        )

        await channel.delete(reason="Ticket fechado via sistema")
