import discord

from discord.ui import (
    View,
    Select
)

# =========================
# 🎫 SUBCATEGORY SELECT
# V1.3.2.12
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

        import traceback

        try:

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

        except Exception as e:

            print("❌ ERRO NO CALLBACK DE SUBCATEGORIA:", flush=True)

            traceback.print_exc()

            try:

                if interaction.response.is_done():

                    await interaction.followup.send(
                        f"❌ Erro: {e}",
                        ephemeral=True
                    )

                else:

                    await interaction.response.send_message(
                        f"❌ Erro: {e}",
                        ephemeral=True
                    )

            except:
                pass

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

    # =========================
    # ⚠️ ERROR HANDLER
    # =========================

    async def on_error(
        self,
        interaction: discord.Interaction,
        error: Exception,
        item
    ):

        import traceback

        print("❌ ERRO NA VIEW DE SUBCATEGORIA:", flush=True)

        traceback.print_exc()

        try:

            if interaction.response.is_done():

                await interaction.followup.send(
                    f"❌ Erro: {error}",
                    ephemeral=True
                )

            else:

                await interaction.response.send_message(
                    f"❌ Erro: {error}",
                    ephemeral=True
                )

        except:
            pass

# =========================
# ⏰ AUTO CLOSE SELECT
# V1.3.2.12
# =========================

class TicketAutoCloseSelect(Select):

    def __init__(self):

        options = [

            discord.SelectOption(
                label="30 minutos",
                emoji="⏰",
                value="1800"
            ),

            discord.SelectOption(
                label="1 hora",
                emoji="⏰",
                value="3600"
            ),

            discord.SelectOption(
                label="2 horas",
                emoji="⏰",
                value="7200"
            ),

            discord.SelectOption(
                label="4 horas",
                emoji="⏰",
                value="14400"
            ),

            discord.SelectOption(
                label="8 horas",
                emoji="⏰",
                value="28800"
            ),

            discord.SelectOption(
                label="12 horas",
                emoji="⏰",
                value="43200"
            ),

            discord.SelectOption(
                label="24 horas",
                emoji="⏰",
                value="86400"
            )
        ]

        super().__init__(

            placeholder="Selecione o tempo de inatividade...",

            min_values=1,
            max_values=1,

            options=options,

            custom_id="ticket_autoclose_select"
        )

    # =========================
    # ⚡ CALLBACK
    # =========================

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        from systems.views import is_staff
        from systems.actions import get_ticket_owner_id

        if not is_staff(interaction):

            return await interaction.response.send_message(

                "❌ Você não tem permissão "
                "para configurar o auto-close.",

                ephemeral=True
            )

        channel = interaction.channel
        guild = interaction.guild

        owner_id = get_ticket_owner_id(channel)

        owner = guild.get_member(owner_id) if owner_id else None

        if not owner:

            return await interaction.response.send_message(

                "❌ Não foi possível identificar "
                "o autor deste ticket.",

                ephemeral=True
            )

        timeout_seconds = int(self.values[0])

        auto_close_manager = interaction.client.auto_close_manager

        await auto_close_manager.start_timer(

            channel=channel,
            user=owner,
            timeout_seconds=timeout_seconds
        )

        hours = timeout_seconds / 3600

        label = (

            f"{int(timeout_seconds / 60)} minutos"

            if timeout_seconds < 3600 else

            f"{hours:g} horas"
        )

        await channel.send(

            f"⏰ Fechamento automático configurado "
            f"por {interaction.user.mention}: "
            f"o ticket será fechado após **{label}** "
            f"de inatividade do usuário."
        )

        await interaction.response.send_message(

            f"✅ Auto-close configurado para {label}.",

            ephemeral=True
        )

# =========================
# ⏰ AUTO CLOSE VIEW
# =========================

class TicketAutoCloseView(View):

    def __init__(self):

        super().__init__(timeout=None)

        self.add_item(
            TicketAutoCloseSelect()
        )

# =========================
# 📁 CHANGE CATEGORY SELECT
# V1.3.2.12
# =========================

class TicketChangeCategorySelect(Select):

    def __init__(self):

        options = [

            discord.SelectOption(
                label="Central de Denúncias",
                emoji="🚨",
                value="denuncias"
            ),

            discord.SelectOption(
                label="Dúvidas e Reportes",
                emoji="❓",
                value="duvidas"
            ),

            discord.SelectOption(
                label="Central Financeira",
                emoji="💰",
                value="financeiro"
            ),

            discord.SelectOption(
                label="Central de Organizações",
                emoji="🏢",
                value="organizacoes"
            ),

            discord.SelectOption(
                label="Central de Parceiros",
                emoji="🤝",
                value="parcerias"
            )
        ]

        super().__init__(

            placeholder="Selecione a nova categoria...",

            min_values=1,
            max_values=1,

            options=options,

            custom_id="ticket_change_category_select"
        )

    # =========================
    # ⚡ CALLBACK
    # =========================

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        from systems.views import is_staff

        if not is_staff(interaction):

            return await interaction.response.send_message(

                "❌ Você não tem permissão "
                "para alterar a categoria.",

                ephemeral=True
            )

        from systems.ticket_manager import change_ticket_category

        new_category = self.values[0]

        success = await change_ticket_category(

            channel=interaction.channel,

            new_category=new_category
        )

        if not success:

            return await interaction.response.send_message(

                "❌ Não foi possível alterar "
                "a categoria deste ticket.",

                ephemeral=True
            )

        await interaction.channel.send(

            f"📁 Categoria alterada para "
            f"`{new_category}` por "
            f"{interaction.user.mention}."
        )

        await interaction.response.send_message(

            f"✅ Categoria alterada para `{new_category}`.",

            ephemeral=True
        )

# =========================
# 📁 CHANGE CATEGORY VIEW
# =========================

class TicketChangeCategoryView(View):

    def __init__(self):

        super().__init__(timeout=None)

        self.add_item(
            TicketChangeCategorySelect()
        )
