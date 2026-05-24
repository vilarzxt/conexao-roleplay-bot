import discord
from discord import app_commands

from config.assets import ASSETS
from config.settings import PROJECT_NAME

# =========================
# 🏓 COMMAND: PING
# V1.3.1 - ORCHESTRATION LAYER
# =========================

@app_commands.command(name="ping", description="Verifica a latência do bot")
async def ping(interaction: discord.Interaction):

    # 🧠 contexto básico (sem lógica de sistema)
    user = interaction.user

    # ⚙️ cálculo direto permitido (exceção: valor runtime simples do Discord)
    latency_ms = round(interaction.client.latency * 1000)

    # 🎨 resposta padronizada (UI layer only)
    embed = discord.Embed(
        title="🏓 Ping do Sistema",
        description="Medição de latência entre o bot e a API do Discord.",
        color=0x145A32
    )

    embed.add_field(
        name="📶 Latência",
        value=f"{latency_ms}ms",
        inline=False
    )

    embed.add_field(
        name="👤 Usuário",
        value=user.mention,
        inline=False
    )

    embed.set_thumbnail(url=ASSETS["logo"])
    embed.set_footer(text=f"{PROJECT_NAME} • V1.3.1")

    await interaction.response.send_message(embed=embed)
