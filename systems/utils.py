import discord

from config.assets import (
    ASSETS,
    EMBED_COLOR,
    FOOTER_TEXT
)

# =========================
# 🎨 EMBED FACTORY
# V1.3.1
# =========================

def create_embed(
    title: str,
    description: str = None,
    color: int = EMBED_COLOR
):

    embed = discord.Embed(
        title=title,
        description=description,
        color=color
    )

    embed.set_thumbnail(
        url=ASSETS["logo"]
    )

    embed.set_footer(
        text=FOOTER_TEXT,
        icon_url=ASSETS["logo"]
    )

    return embed
