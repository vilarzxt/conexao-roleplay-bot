import discord
from datetime import datetime

# =========================
# 📜 TRANSCRIPT ENGINE
# V1.3.1 - AUDITORIA DE TICKETS
# =========================

async def generate_transcript(
    channel: discord.TextChannel
):

    messages = []

    # =========================
    # 📥 COLETA DE MENSAGENS
    # =========================

    async for message in channel.history(
        limit=None,
        oldest_first=True
    ):

        timestamp = message.created_at.strftime(
            "%d/%m/%Y %H:%M"
        )

        content = (
            f"[{timestamp}] "
            f"{message.author}: "
            f"{message.content}"
        )

        messages.append(content)

    # =========================
    # 📄 TEXTO FINAL
    # =========================

    transcript_text = "\n".join(messages)

    return transcript_text

# =========================
# 📤 ENVIO DE LOG
# =========================

async def send_transcript_log(
    log_channel: discord.TextChannel,
    ticket_channel: discord.TextChannel,
    transcript: str
):

    # =========================
    # 📦 EMBED DE LOG
    # =========================

    embed = discord.Embed(
        title="📜 Transcript Gerado",
        description=(
            f"Ticket: {ticket_channel.name}"
        ),
        color=0x145A32,
        timestamp=datetime.utcnow()
    )

    embed.add_field(
        name="📂 Canal",
        value=ticket_channel.mention,
        inline=False
    )

    # =========================
    # 📄 ENVIO DO ARQUIVO
    # =========================

    file = discord.File(
        fp=bytes(transcript, "utf-8"),
        filename=f"{ticket_channel.name}.txt"
    )

    await log_channel.send(
        embed=embed,
        file=file
    )
