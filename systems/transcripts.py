# =========================
# 📜 TRANSCRIPT ENGINE
# V1.3.2 - PRODUCTION CORE
# =========================

import discord
import datetime
import html


# =========================
# 🧠 TRANSCRIPT BUILDER
# =========================

class TranscriptBuilder:

    def __init__(self):
        pass


    # =========================
    # 📜 BUILD RAW TEXT TRANSCRIPT
    # =========================

    async def build_text(self, channel: discord.TextChannel, limit: int = 500):

        messages = []

        async for msg in channel.history(limit=limit, oldest_first=True):

            timestamp = msg.created_at.strftime("%Y-%m-%d %H:%M:%S")

            messages.append(
                f"[{timestamp}] {msg.author} ➜ {msg.content}"
            )

        return "\n".join(messages)


    # =========================
    # 🌐 BUILD HTML TRANSCRIPT
    # =========================

    async def build_html(self, channel: discord.TextChannel, limit: int = 500):

        messages_html = []

        async for msg in channel.history(limit=limit, oldest_first=True):

            timestamp = msg.created_at.strftime("%Y-%m-%d %H:%M:%S")

            content = html.escape(msg.content)

            messages_html.append(
                f"""
                <div class="msg">
                    <span class="time">[{timestamp}]</span>
                    <span class="author">{msg.author}</span>
                    <div class="content">{content}</div>
                </div>
                """
            )

        html_output = f"""
        <html>
        <head>
            <meta charset="utf-8">
            <title>Transcript - {channel.name}</title>
            <style>
                body {{
                    font-family: Arial;
                    background: #1e1e1e;
                    color: #fff;
                    padding: 20px;
                }}
                .msg {{
                    margin-bottom: 10px;
                    padding: 10px;
                    background: #2c2c2c;
                    border-radius: 8px;
                }}
                .time {{
                    color: #888;
                    font-size: 12px;
                }}
                .author {{
                    font-weight: bold;
                    color: #2ecc71;
                }}
                .content {{
                    margin-top: 5px;
                }}
            </style>
        </head>
        <body>
            <h2>📜 Transcript - {channel.name}</h2>
            {"".join(messages_html)}
        </body>
        </html>
        """

        return html_output


    # =========================
    # 📤 SEND TRANSCRIPT (STAFF + USER)
    # =========================

    async def send_transcript(
        self,
        channel: discord.TextChannel,
        guild: discord.Guild,
        user: discord.Member
    ):

        text = await self.build_text(channel)
        html_file = await self.build_html(channel)

        timestamp = datetime.datetime.utcnow().strftime("%Y%m%d-%H%M%S")

        txt_file = discord.File(
            fp=bytes(text, "utf-8"),
            filename=f"transcript-{channel.name}-{timestamp}.txt"
        )

        html_file_obj = discord.File(
            fp=bytes(html_file, "utf-8"),
            filename=f"transcript-{channel.name}-{timestamp}.html"
        )


        # =========================
        # 📊 STAFF LOG CHANNEL
        # =========================

        log_channel = discord.utils.get(
            guild.channels,
            name="logs-tickets"
        )

        if log_channel:

            await log_channel.send(
                content=f"📜 Transcript gerado para `{channel.name}`",
                files=[txt_file, html_file_obj]
            )


        # =========================
        # 📨 DM USER COPY
        # =========================

        try:

            await user.send(
                content="📨 Aqui está o transcript do seu atendimento.",
                files=[txt_file]
            )

        except:
            pass
