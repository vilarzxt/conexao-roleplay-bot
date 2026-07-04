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
# V1.3.2.9
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

        from systems.dropdowns import (
            TicketSubCategoryView
        )

        category = self.values[0]

        embed = discord.Embed(

            title="📂 Categoria Selecionada",

            description=(
                f"Categoria: `{category}`\n\n"

                "Selecione abaixo a "
                "subcategoria do atendimento."
            ),

            color=discord.Color.blurple()
        )

        await interaction.response.send_message(

            embed=embed,

            view=TicketSubCategoryView(
                category
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

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.send_message(

            "⚠️ Sistema de fechamento em desenvolvimento.",

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

            placeholder="Gerenciamento do ticket...",

            min_values=1,
            max_values=1,

            options=options,

            custom_id="ticket_management_select"
        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        action = self.values[0]

        await interaction.response.send_message(

            f"⚙️ Ação selecionada:\n`{action}`",

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
