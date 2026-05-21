import os
import discord
from discord import app_commands

# ===== TOKEN (correto e seguro) =====
TOKEN = os.getenv("TOKEN")

if TOKEN is None:
    raise RuntimeError("TOKEN não encontrado. Configure a variável de ambiente TOKEN.")

# ===== INTENTS =====
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# ===== EVENTO ON READY =====
@client.event
async def on_ready():
    await tree.sync()
    print(f"Bot online como: {client.user}")

# ===== SLASH COMMAND: /ping =====
@tree.command(name="ping", description="Verifica a latência e conexão do bot")
async def ping(interaction: discord.Interaction):
    latency = round(client.latency * 1000)
    await interaction.response.send_message(f"🏓 Pong! {latency}ms")

# ===== SLASH COMMAND: /status =====
@tree.command(name="status", description="Mostra status básico do bot")
async def status(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"🟢 Bot ativo\nServidores conectados: {len(client.guilds)}"
    )

# ===== RUN =====
client.run(TOKEN)
