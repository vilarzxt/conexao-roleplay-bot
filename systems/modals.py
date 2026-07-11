import discord

from discord.ui import (
    Modal,
    TextInput
)

# =========================
# 🔒 CLOSE REASON MODAL (OUTROS)
# V1.3.2.12
# =========================

class CloseReasonModal(Modal, title="Fechar Ticket — Outro Motivo"):

    reason = TextInput(

        label="Motivo do fechamento",

        placeholder="Descreva o motivo do fechamento...",

        style=discord.TextStyle.paragraph,

        max_length=300,

        required=True
    )

    async def on_submit(
        self,
        interaction: discord.Interaction
    ):

        from systems.ticket_manager import close_ticket

        await close_ticket(
            interaction=interaction,
            reason=str(self.reason)
        )

# =========================
# ➕ ADD MEMBER MODAL
# =========================

class AddMemberModal(Modal, title="Adicionar Membro ao Ticket"):

    user_id = TextInput(

        label="ID ou @menção do usuário",

        placeholder="Ex: 123456789012345678",

        max_length=50,

        required=True
    )

    async def on_submit(
        self,
        interaction: discord.Interaction
    ):

        from systems.actions import add_member_to_ticket

        await add_member_to_ticket(
            interaction=interaction,
            raw_input=str(self.user_id)
        )

# =========================
# ➖ REMOVE MEMBER MODAL
# =========================

class RemoveMemberModal(Modal, title="Remover Membro do Ticket"):

    user_id = TextInput(

        label="ID ou @menção do usuário",

        placeholder="Ex: 123456789012345678",

        max_length=50,

        required=True
    )

    async def on_submit(
        self,
        interaction: discord.Interaction
    ):

        from systems.actions import remove_member_from_ticket

        await remove_member_from_ticket(
            interaction=interaction,
            raw_input=str(self.user_id)
        )

# =========================
# 📝 PRIVATE NOTE MODAL
# =========================

class PrivateNoteModal(Modal, title="Adicionar Nota Privada"):

    note = TextInput(

        label="Nota (visível apenas para staff)",

        placeholder="Escreva sua anotação...",

        style=discord.TextStyle.paragraph,

        max_length=500,

        required=True
    )

    async def on_submit(
        self,
        interaction: discord.Interaction
    ):

        from systems.actions import add_private_note

        await add_private_note(
            interaction=interaction,
            note=str(self.note)
        )

# =========================
# ✏️ RENAME TICKET MODAL
# =========================

class RenameTicketModal(Modal, title="Renomear Ticket"):

    new_name = TextInput(

        label="Novo nome do canal",

        placeholder="Ex: ticket-urgente",

        max_length=90,

        required=True
    )

    async def on_submit(
        self,
        interaction: discord.Interaction
    ):

        from systems.actions import rename_ticket

        await rename_ticket(
            interaction=interaction,
            new_name=str(self.new_name)
        )
