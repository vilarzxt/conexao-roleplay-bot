import discord

from discord.ui import (
    View,
    Select,
    Button,
    Modal,
    TextInput
)

# =========================
# 🎫 TICKET CATEGORY SELECT
# V1.3.2
# =========================

class TicketCategorySelect(Select):

    def __init__(self):

        options = [

            discord.SelectOption(
                label="Central de Denúncias",
                description=(
                    "Denúncias contra players, "
                    "staff ou organizações."
                ),
                emoji="🚨",
                value="denuncias"
            ),

            discord.SelectOption(
                label="Dúvidas e Reportes",
                description=(
                    "Dúvidas gerais, bugs "
                    "e suporte técnico."
                ),
                emoji="❓",
                value="duvidas"
            ),

            discord.SelectOption(
                label="Central Financeira",
                description=(
                    "VIP, coins e "
                    "problemas financeiros."
                ),
                emoji="💰",
                value="financeiro"
            ),

            discord.SelectOption(
                label="Central de Organizações",
                description=(
                    "Suporte operacional "
                    "de organizações."
                ),
                emoji="🏢",
                value="organizacoes"
            ),

            discord.SelectOption(
                label="Central de Parceiros",
                description=(
                    "Parcerias, criadores "
                    "e projetos."
                ),
                emoji="🤝",
                value="parcerias"
            )
        ]

        super().__init__(

            placeholder=(
                "Selecione a categoria "
                "do atendimento..."
            ),

            min_values=1,
            max_values=1,

            options=options,

            custom_id="ticket_category_select"
        )

    # =========================
    # ⚡ CALLBACK
    # =========================

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        category = self.values[0]

        await interaction.response.send_message(

            (
                f"📂 Categoria selecionada:\n"
                f"`{category}`\n\n"

                "⚠️ O sistema de subcategorias "
                "será carregado pelo "
                "dropdowns.py"
            ),

            ephemeral=True
        )

# =========================
# 🎫 MAIN PANEL VIEW
# =========================

class TicketPanelView(View):

    def __init__(self):

        super().__init__(timeout=None)

        self.add_item(
            TicketCategorySelect()
        )

# =========================
# 🔒 CLOSE TICKET BUTTON
# =========================

class CloseTicketButton(Button):

    def __init__(self):

        super().__init__(

            label="Fechar Ticket",

            emoji="🔒",

            style=discord.ButtonStyle.danger,

            custom_id="close_ticket_button"
        )

    # =========================
    # ⚡ CALLBACK
    # =========================

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.send_message(

            (
                "⚠️ O sistema de fechamento "
                "ainda será conectado "
                "ao ticket_manager."
            ),

            ephemeral=True
        )

# =========================
# ⚙️ MANAGEMENT SELECT
# =========================

class TicketManagementSelect(Select):

    def __init__(self):

        options = [

            discord.SelectOption(
                label="Assumir Ticket",
                emoji="👤",
                value="claim_ticket"
            ),

            discord.SelectOption(
                label="Adicionar Membro",
                emoji="➕",
                value="add_member"
            ),

            discord.SelectOption(
                label="Remover Membro",
                emoji="➖",
                value="remove_member"
            ),

            discord.SelectOption(
                label="Alterar Categoria",
                emoji="🔄",
                value="change_category"
            ),

            discord.SelectOption(
                label="Gerar Transcript",
                emoji="📄",
                value="generate_transcript"
            ),

            discord.SelectOption(
                label="Auto Close",
                emoji="⏰",
                value="auto_close"
            ),

            discord.SelectOption(
                label="Reabrir Ticket",
                emoji="🔓",
                value="reopen_ticket"
            )
        ]

        super().__init__(

            placeholder=(
                "Gerenciamento do ticket..."
            ),

            min_values=1,
            max_values=1,

            options=options,

            custom_id="ticket_management_select"
        )

    # =========================
    # ⚡ CALLBACK
    # =========================

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        action = self.values[0]

        await interaction.response.send_message(

            (
                f"⚙️ Ação selecionada:\n"
                f"`{action}`\n\n"

                "⚠️ O gerenciamento ainda "
                "será conectado aos systems."
            ),

            ephemeral=True
        )

# =========================
# ⚙️ MANAGEMENT VIEW
# =========================

class TicketManagementView(View):

    def __init__(self):

        super().__init__(timeout=None)

        self.add_item(
            TicketManagementSelect()
        )

        self.add_item(
            CloseTicketButton()
        )

# =========================
# ⭐ RATING SELECT
# =========================

class TicketRatingSelect(Select):

    def __init__(self):

        options = [

            discord.SelectOption(
                label="⭐ 1 Estrela",
                value="1"
            ),

            discord.SelectOption(
                label="⭐⭐ 2 Estrelas",
                value="2"
            ),

            discord.SelectOption(
                label="⭐⭐⭐ 3 Estrelas",
                value="3"
            ),

            discord.SelectOption(
                label="⭐⭐⭐⭐ 4 Estrelas",
                value="4"
            ),

            discord.SelectOption(
                label="⭐⭐⭐⭐⭐ 5 Estrelas",
                value="5"
            )
        ]

        super().__init__(

            placeholder=(
                "Avalie o atendimento..."
            ),

            min_values=1,
            max_values=1,

            options=options,

            custom_id="ticket_rating_select"
        )

    # =========================
    # ⚡ CALLBACK
    # =========================

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        rating = self.values[0]

        await interaction.response.send_message(

            (
                f"⭐ Avaliação registrada:\n"
                f"`{rating} estrela(s)`\n\n"

                "⚠️ O sistema de feedback "
                "ainda será conectado "
                "ao storage."
            ),

            ephemeral=True
        )

# =========================
# ⭐ RATING VIEW
# =========================

class TicketRatingView(View):

    def __init__(self):

        super().__init__(timeout=None)

        self.add_item(
            TicketRatingSelect()
        )

# =========================
# 📝 FEEDBACK MODAL
# =========================

class TicketFeedbackModal(Modal):

    def __init__(self):

        super().__init__(
            title="Feedback do Atendimento"
        )

        self.feedback = TextInput(

            label="Comentário (Opcional)",

            placeholder=(
                "Descreva sua experiência "
                "com o atendimento..."
            ),

            required=False,

            style=discord.TextStyle.paragraph,

            max_length=1000
        )

        self.add_item(
            self.feedback
        )

    # =========================
    # ⚡ SUBMIT
    # =========================

    async def on_submit(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.send_message(

            (
                "✅ Feedback enviado "
                "com sucesso."
            ),

            ephemeral=True
        )

# =========================
# 📝 CLOSE REASON MODAL
# =========================

class CloseReasonModal(Modal):

    def __init__(self):

        super().__init__(
            title="Motivo do Fechamento"
        )

        self.reason = TextInput(

            label="Motivo",

            placeholder=(
                "Informe detalhadamente "
                "o motivo do fechamento..."
            ),

            required=True,

            style=discord.TextStyle.paragraph,

            max_length=1000
        )

        self.add_item(
            self.reason
        )

    # =========================
    # ⚡ SUBMIT
    # =========================

    async def on_submit(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.send_message(

            (
                "🔒 Motivo registrado.\n\n"

                "⚠️ O fechamento ainda "
                "será conectado ao "
                "ticket_manager."
            ),

            ephemeral=True
        )
