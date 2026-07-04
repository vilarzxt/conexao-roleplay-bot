import discord

from discord.ui import (
    View,
    Select
)

# =========================
# 🎫 SUBCATEGORY SELECT
# V1.3.2.9
# =========================

class TicketSubCategorySelect(Select):

    def __init__(
        self,
        category: str
    ):

        self.category = category

        options = self.get_options()

        super().__init__(

            placeholder=(
                "Selecione o tipo "
                "do atendimento..."
            ),

            min_values=1,
            max_values=1,

            options=options,

            custom_id=(
                f"ticket_subcategory_"
                f"{category}"
            )
        )

    # =========================
    # 📂 OPTIONS
    # =========================

    def get_options(self):

        # =========================
        # 🚨 DENÚNCIAS
        # =========================

        if self.category == "denuncias":

            return [

                discord.SelectOption(
                    label="Denúncia contra Player",
                    emoji="👤",
                    value="denuncia_player"
                ),

                discord.SelectOption(
                    label="Denúncia contra Staff",
                    emoji="👮",
                    value="denuncia_staff"
                ),

                discord.SelectOption(
                    label="Denúncia contra Organização",
                    emoji="🏢",
                    value="denuncia_organizacao"
                )
            ]

        # =========================
        # ❓ DÚVIDAS
        # =========================

        if self.category == "duvidas":

            return [

                discord.SelectOption(
                    label="Dúvidas Gerais",
                    emoji="❓",
                    value="duvidas_gerais"
                ),

                discord.SelectOption(
                    label="Reporte / Suporte Técnico",
                    emoji="🛠️",
                    value="suporte_tecnico"
                )
            ]

        # =========================
        # 💰 FINANCEIRO
        # =========================

        if self.category == "financeiro":

            return [

                discord.SelectOption(
                    label="VIP ou Problemas com Coins",
                    emoji="💳",
                    value="vip_coins"
                ),

                discord.SelectOption(
                    label="Problemas Financeiros",
                    emoji="⚠️",
                    value="problemas_financeiros"
                )
            ]

        # =========================
        # 🏢 ORGANIZAÇÕES
        # =========================

        if self.category == "organizacoes":

            return [

                discord.SelectOption(
                    label="Marcar Ações",
                    emoji="🎯",
                    value="marcar_acoes"
                ),

                discord.SelectOption(
                    label="Suporte Organizacional",
                    emoji="🏢",
                    value="suporte_org"
                ),

                discord.SelectOption(
                    label="Dúvidas Organizacionais",
                    emoji="❓",
                    value="duvidas_org"
                )
            ]

        # =========================
        # 🤝 PARCERIAS
        # =========================

        if self.category == "parcerias":

            return [

                discord.SelectOption(
                    label="Criadores de Conteúdo",
                    emoji="🎥",
                    value="criadores"
                ),

                discord.SelectOption(
                    label="Projetos / Servidores",
                    emoji="🤝",
                    value="projetos_servidores"
                ),

                discord.SelectOption(
                    label="Dúvidas de Parceria",
                    emoji="❓",
                    value="duvidas_parceria"
                )
            ]

        return []

    # =========================
    # ⚡ CALLBACK
    # =========================

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        from systems.ticket_manager import (
            create_ticket
        )

        subcategory = self.values[0]

        await interaction.response.defer(
            ephemeral=True
        )

        # =========================
        # 🎫 CREATE TICKET
        # =========================

        ticket_channel = await create_ticket(

            interaction=interaction,

            category=self.category,

            subcategory=subcategory
        )

        # =========================
        # 📩 REDIRECT MESSAGE
        # =========================

        if ticket_channel:

            await interaction.followup.send(

                (
                    "✅ Ticket criado com sucesso.\n\n"
                    f"📂 Canal: {ticket_channel.mention}"
                ),

                ephemeral=True
            )

        else:

            await interaction.followup.send(

                (
                    "❌ O sistema não conseguiu "
                    "criar o ticket."
                ),

                ephemeral=True
            )

# =========================
# 🎫 SUBCATEGORY VIEW
# =========================

class TicketSubCategoryView(View):

    def __init__(
        self,
        category: str
    ):

        super().__init__(timeout=None)

        self.add_item(
            TicketSubCategorySelect(
                category
            )
        )
