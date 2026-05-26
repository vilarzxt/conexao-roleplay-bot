import discord
from systems.dropdowns import TicketSubCategoryView

class TicketCategorySelect(discord.ui.Select):

    def __init__(self):

        options = [

            discord.SelectOption(
                label="Central de Denúncias",
                description="Denúncias contra players, staff ou organizações.",
                emoji="🚨",
                value="denuncias"
            ),

            discord.SelectOption(
                label="Dúvidas e Reportes",
                description="Dúvidas gerais, bugs e suporte técnico.",
                emoji="❓",
                value="duvidas"
            ),

            discord.SelectOption(
                label="Central Financeira",
                description="VIP, coins e problemas financeiros.",
                emoji="💰",
                value="financeiro"
            ),

            discord.SelectOption(
                label="Central de Organizações",
                description="Suporte operacional de organizações.",
                emoji="🏢",
                value="organizacoes"
            ),

            discord.SelectOption(
                label="Central de Parceiros",
                description="Parcerias, criadores e projetos.",
                emoji="🤝",
                value="parcerias"
            )
        ]

        super().__init__(
            placeholder="Selecione a categoria do atendimento...",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="ticket_category_select"
        )

    async def callback(self, interaction: discord.Interaction):

        category = self.values[0]

        # =========================
        # 🚀 ABRE SUBCATEGORIA REAL
        # =========================

        embed = discord.Embed(
            title="📂 Categoria Selecionada",
            description=(
                f"Categoria: `{category}`\n\n"
                "Selecione a subcategoria abaixo para continuar o atendimento."
            ),
            color=discord.Color.blurple()
        )

        await interaction.response.send_message(
            embed=embed,
            view=TicketSubCategoryView(category),
            ephemeral=True
        )
