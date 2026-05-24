import discord
from discord.ext import commands
import os
import asyncio

from config.settings import PREFIX, GUILD_ID

# =========================
# 🤖 INTENTS
# =========================

intents = discord.Intents.default()

intents.members = True
intents.message_content = True

# =========================
# 🤖 BOT CORE
# =========================

bot = commands.Bot(
    command_prefix=PREFIX,
    intents=intents,
    help_command=None
)

# =========================
# 📦 COMMAND LOADER
# =========================

COMMAND_FILES = [

    "commands.ping",
    "commands.info",
    "commands.status",
    "commands.ticket",
    "commands.embed",
    "commands.anuncio",
    "commands.regras",
    "commands.servidor",
    "commands.warn",
    "commands.kick",
    "commands.ban",
    "commands.lock",
    "commands.unlock"
]

# =========================
# 🚀 SETUP HOOK
# =========================

async def setup_hook():

    for command in COMMAND_FILES:

        try:

            module = __import__(
                command,
                fromlist=["setup"]
            )

            if hasattr(module, "setup"):
                await module.setup(bot)

            print(f"[OK] {command}")

        except Exception as e:

            print(f"[ERRO] {command}")
            print(e)

# =========================
# 🔁 READY EVENT
# =========================

@bot.event
async def on_ready():

    print("========================")
    print("BOT ONLINE")
    print(bot.user)

    try:

        guild = discord.Object(id=GUILD_ID)

        guild_sync = await bot.tree.sync(
            guild=guild
        )

        global_sync = await bot.tree.sync()

        print(f"GUILD SYNC: {len(guild_sync)}")
        print(f"GLOBAL SYNC: {len(global_sync)}")

    except Exception as e:

        print("SYNC ERROR:")
        print(e)

    print("========================")

# =========================
# 🚀 STARTUP
# =========================

async def main():

    async with bot:

        bot.setup_hook = setup_hook

        await bot.start(
            os.getenv("TOKEN")
        )

# =========================
# ▶️ RUNTIME
# =========================

asyncio.run(main())
