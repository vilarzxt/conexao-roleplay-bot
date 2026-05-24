import discord

from systems.ticket_manager import create_ticket

# =========================
# 🎛️ DROPDOWN DE TICKETS
# V1.3.1 - CATEGORY ROUTER
# =========================

class TicketDropdown(discord.ui.Select):

    def __init__(self):

        options = [

            discord.SelectOption(
                label="Denúncias",
                description="Reportar usuários ou situações",
                emoji="🚨"
            ),

            discord.SelectOption(
                label="Suporte",
                description="Ajuda geral e dúvidas",
                emoji="❓"
            ),

            discord.SelectOption(
                label="Financeiro",
                description="Pagamentos e compras",
                emoji="💰"
            ),

            discord.SelectOption(
                label="Parcerias",
                description="Solicitações comerciais",
                emoji="🤝"
            )
        ]

        super().__init__(
            placeholder="Selecione uma categoria...",
            min_values=1,
            max_values=1,
            options=options
        )

    # =========================
    # ⚙️ CALLBACK PRINCIPAL
    # =========================

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        categoria = self.values[0]

        # ⚙️ chama o core engine
        channel = await create_ticket(
            interaction,
            categoria
        )

        if channel is None:

            await interaction.response.send_message(
                "❌ Erro ao criar ticket.",
                ephemeral=True
            )

            return

        # ✅ resposta ao usuário
        await interaction.response.send_message(
            f"✅ Ticket criado: {channel.mention}",
            ephemeral=True
        )

# =========================
# 🧩 VIEW DO DROPDOWN
# =========================

class TicketView(discord.ui.View):

    def __init__(self):

        super().__init__(timeout=None)

        self.add_item(TicketDropdown())
