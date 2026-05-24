import discord

# =========================
# 🧩 TICKET CONTROL VIEW
# V1.3.1 - INTERACTIVE UI
# =========================

class TicketControls(discord.ui.View):

    def __init__(self):

        super().__init__(timeout=None)

    # =========================
    # 🔒 FECHAR TICKET
    # =========================

    @discord.ui.button(
        label="Fechar Ticket",
        style=discord.ButtonStyle.danger,
        emoji="🔒"
    )
    async def close_ticket(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        await interaction.response.send_message(
            "🔒 Ticket será fechado em breve.",
            ephemeral=True
        )

        await interaction.channel.delete()

    # =========================
    # 👤 ASSUMIR TICKET
    # =========================

    @discord.ui.button(
        label="Assumir",
        style=discord.ButtonStyle.primary,
        emoji="👤"
    )
    async def claim_ticket(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        await interaction.response.send_message(
            f"✅ Ticket assumido por {interaction.user.mention}",
            ephemeral=False
        )

    # =========================
    # 📜 TRANSCRIPT
    # =========================

    @discord.ui.button(
        label="Transcript",
        style=discord.ButtonStyle.secondary,
        emoji="📜"
    )
    async def transcript_ticket(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        await interaction.response.send_message(
            "📜 Sistema de transcript ainda em desenvolvimento.",
            ephemeral=True
        )
