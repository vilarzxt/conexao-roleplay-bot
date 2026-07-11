import discord
import io

from systems.views import is_staff

# =========================
# 🧩 ACTIONS ENGINE
# V1.3.2.12
# =========================

# =========================
# 🔎 HELPER: OWNER ID FROM TOPIC
# =========================

def get_ticket_owner_id(channel: discord.TextChannel):

    if not channel.topic:
        return None

    try:

        first_part = channel.topic.split(" | ")[0]

        return int(first_part.strip())

    except (ValueError, IndexError):

        return None

# =========================
# 📢 CHAMAR USUÁRIO
# =========================

async def call_ticket_user(
    interaction: discord.Interaction
):

    if not is_staff(interaction):

        return await interaction.response.send_message(

            "❌ Você não tem permissão "
            "para chamar o usuário.",

            ephemeral=True
        )

    channel = interaction.channel
    guild = interaction.guild

    owner_id = get_ticket_owner_id(channel)

    if not owner_id:

        return await interaction.response.send_message(

            "❌ Não foi possível identificar "
            "o autor deste ticket.",

            ephemeral=True
        )

    member = guild.get_member(owner_id)

    if not member:

        return await interaction.response.send_message(

            "❌ Usuário não encontrado no servidor.",

            ephemeral=True
        )

    # =========================
    # 📤 DM COM BOTÃO
    # =========================

    dm_sent = True

    try:

        embed = discord.Embed(

            title="📢 Você foi chamado em um ticket!",

            description=(

                f"A equipe de suporte está aguardando "
                f"sua resposta no ticket **#{channel.name}**!\n\n"

                f"**Servidor:** {guild.name}\n"
                f"**Chamado por:** {interaction.user.mention}\n\n"

                "Por favor, retorne ao ticket "
                "o mais rápido possível."
            ),

            color=discord.Color.red()
        )

        view = discord.ui.View()

        view.add_item(

            discord.ui.Button(

                label="Ir para o Ticket",

                emoji="🎫",

                style=discord.ButtonStyle.link,

                url=channel.jump_url
            )
        )

        await member.send(
            embed=embed,
            view=view
        )

    except discord.Forbidden:

        dm_sent = False

    # =========================
    # 📩 AVISO NO CANAL
    # =========================

    await channel.send(

        f"📢 {member.mention} foi notificado "
        f"no privado por {interaction.user.mention}."
    )

    # =========================
    # ✅ CONFIRMAÇÃO
    # =========================

    if dm_sent:

        await interaction.response.send_message(

            (
                "✅ Usuário chamado com sucesso!\n\n"
                f"Uma mensagem foi enviada para "
                f"{member.mention} no privado."
            ),

            ephemeral=True
        )

    else:

        await interaction.response.send_message(

            (
                "⚠️ Usuário notificado no canal, mas "
                "não foi possível enviar DM "
                "(DM bloqueada)."
            ),

            ephemeral=True
        )

# =========================
# 📄 GERAR TRANSCRIPT (STAFF)
# =========================

async def generate_ticket_transcript(
    interaction: discord.Interaction
):

    if not is_staff(interaction):

        return await interaction.response.send_message(

            "❌ Você não tem permissão "
            "para gerar o transcript.",

            ephemeral=True
        )

    from systems.ticket_manager import ticket_manager

    await interaction.response.defer(ephemeral=True)

    channel = interaction.channel

    html_content = await ticket_manager.transcripts.build_html(channel)

    file = discord.File(

        fp=io.BytesIO(html_content.encode("utf-8")),

        filename=f"transcript-{channel.name}.html"
    )

    await interaction.followup.send(

        "📄 Transcript gerado com sucesso:",

        file=file,

        ephemeral=True
    )

# =========================
# ➕ ADICIONAR MEMBRO
# =========================

async def add_member_to_ticket(
    interaction: discord.Interaction,
    raw_input: str
):

    if not is_staff(interaction):

        return await interaction.response.send_message(

            "❌ Você não tem permissão "
            "para adicionar membros.",

            ephemeral=True
        )

    guild = interaction.guild
    channel = interaction.channel

    clean_id = (

        raw_input
        .replace("<@", "")
        .replace("!", "")
        .replace(">", "")
        .strip()
    )

    try:

        member = guild.get_member(int(clean_id))

    except ValueError:

        member = None

    if not member:

        return await interaction.response.send_message(

            "❌ Usuário não encontrado. "
            "Envie o ID ou @menção correto.",

            ephemeral=True
        )

    await channel.set_permissions(

        member,

        view_channel=True,
        send_messages=True,
        read_message_history=True,
        attach_files=True,
        embed_links=True
    )

    await channel.send(

        f"➕ {member.mention} foi adicionado "
        f"ao ticket por {interaction.user.mention}."
    )

    await interaction.response.send_message(

        f"✅ {member.mention} adicionado com sucesso.",

        ephemeral=True
    )

# =========================
# ➖ REMOVER MEMBRO
# =========================

async def remove_member_from_ticket(
    interaction: discord.Interaction,
    raw_input: str
):

    if not is_staff(interaction):

        return await interaction.response.send_message(

            "❌ Você não tem permissão "
            "para remover membros.",

            ephemeral=True
        )

    guild = interaction.guild
    channel = interaction.channel

    clean_id = (

        raw_input
        .replace("<@", "")
        .replace("!", "")
        .replace(">", "")
        .strip()
    )

    try:

        member = guild.get_member(int(clean_id))

    except ValueError:

        member = None

    if not member:

        return await interaction.response.send_message(

            "❌ Usuário não encontrado. "
            "Envie o ID ou @menção correto.",

            ephemeral=True
        )

    await channel.set_permissions(
        member,
        overwrite=None
    )

    await channel.send(

        f"➖ {member.mention} foi removido "
        f"do ticket por {interaction.user.mention}."
    )

    await interaction.response.send_message(

        f"✅ {member.mention} removido com sucesso.",

        ephemeral=True
    )

# =========================
# 📝 NOTA PRIVADA
# =========================

async def add_private_note(
    interaction: discord.Interaction,
    note: str
):

    if not is_staff(interaction):

        return await interaction.response.send_message(

            "❌ Você não tem permissão "
            "para adicionar notas.",

            ephemeral=True
        )

    guild = interaction.guild
    channel = interaction.channel

    log_channel = discord.utils.get(
        guild.channels,
        name="logs-tickets"
    )

    if not log_channel:

        return await interaction.response.send_message(

            "❌ Canal `logs-tickets` não encontrado. "
            "A nota não pôde ser salva.",

            ephemeral=True
        )

    embed = discord.Embed(

        title="📝 Nota Privada",

        description=note,

        color=discord.Color.dark_grey()
    )

    embed.add_field(
        name="🎫 Ticket",
        value=channel.mention,
        inline=True
    )

    embed.add_field(
        name="👤 Autor",
        value=interaction.user.mention,
        inline=True
    )

    await log_channel.send(embed=embed)

    await interaction.response.send_message(

        "✅ Nota privada registrada com sucesso.",

        ephemeral=True
    )

# =========================
# ✏️ RENOMEAR TICKET
# =========================

async def rename_ticket(
    interaction: discord.Interaction,
    new_name: str
):

    if not is_staff(interaction):

        return await interaction.response.send_message(

            "❌ Você não tem permissão "
            "para renomear este ticket.",

            ephemeral=True
        )

    channel = interaction.channel

    clean_name = (

        new_name
        .lower()
        .replace(" ", "-")
    )

    try:

        await channel.edit(name=clean_name)

    except discord.HTTPException as e:

        return await interaction.response.send_message(

            f"❌ Erro ao renomear: {e}",

            ephemeral=True
        )

    await interaction.response.send_message(

        f"✅ Ticket renomeado para `{clean_name}`.",

        ephemeral=True
    )
