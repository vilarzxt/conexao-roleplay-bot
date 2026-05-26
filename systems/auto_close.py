# =========================
# ⏰ AUTO CLOSE ENGINE
# V1.3.2 - FINAL (PRODUCTION)
# =========================

import asyncio
import datetime
import discord


# =========================
# 🧠 ACTIVE TIMERS REGISTRY
# =========================

ACTIVE_TIMERS = {}


# =========================
# ⏰ AUTO CLOSE MANAGER
# =========================

class AutoCloseManager:

    def __init__(self, bot):
        self.bot = bot


    # =========================
    # 🔍 CHECK ACTIVE TIMER
    # =========================

    def is_active(self, channel_id: int) -> bool:
        return channel_id in ACTIVE_TIMERS


    # =========================
    # 🚀 START TIMER
    # =========================

    async def start_timer(
        self,
        channel: discord.TextChannel,
        user: discord.Member,
        timeout_seconds: int
    ):

        # cancela timer anterior se existir
        if channel.id in ACTIVE_TIMERS:

            ACTIVE_TIMERS[channel.id].cancel()
            del ACTIVE_TIMERS[channel.id]

        task = asyncio.create_task(
            self._run_timer(channel, user, timeout_seconds)
        )

        ACTIVE_TIMERS[channel.id] = task


    # =========================
    # 🔄 RESET TIMER (ACTIVITY)
    # =========================

    async def reset_timer(self, channel: discord.TextChannel):

        if channel.id in ACTIVE_TIMERS:

            try:
                ACTIVE_TIMERS[channel.id].cancel()
            except:
                pass

            del ACTIVE_TIMERS[channel.id]


    # =========================
    # ⏳ TIMER CORE LOOP
    # =========================

    async def _run_timer(
        self,
        channel: discord.TextChannel,
        user: discord.Member,
        timeout_seconds: int
    ):

        try:

            warning_50 = int(timeout_seconds * 0.5)
            warning_75 = int(timeout_seconds * 0.75)

            # =========================
            # ⚠️ WARNING 1
            # =========================

            await asyncio.sleep(warning_50)

            if channel.id not in ACTIVE_TIMERS:
                return

            await channel.send(
                f"⚠️ {user.mention}, seu ticket ficará inativo em breve."
            )

            # =========================
            # ⚠️ WARNING 2
            # =========================

            await asyncio.sleep(warning_75 - warning_50)

            if channel.id not in ACTIVE_TIMERS:
                return

            await channel.send(
                f"⚠️ Último aviso {user.mention}: ticket será encerrado em breve."
            )

            # =========================
            # ⏰ FINAL WAIT
            # =========================

            await asyncio.sleep(timeout_seconds - warning_75)

            if channel.id not in ACTIVE_TIMERS:
                return

            await self._close_due_inactivity(channel, user)

        except asyncio.CancelledError:
            return

        except Exception as e:
            print(f"[AUTO_CLOSE ERROR] {e}")


    # =========================
    # 🔒 AUTO CLOSE EXECUTION
    # =========================

    async def _close_due_inactivity(
        self,
        channel: discord.TextChannel,
        user: discord.Member
    ):

        try:

            await channel.send(
                "⏰ Ticket encerrado automaticamente por inatividade."
            )

            # remove timer
            if channel.id in ACTIVE_TIMERS:
                del ACTIVE_TIMERS[channel.id]

            # DM user
            try:

                await user.send(
                    f"📨 Seu ticket `{channel.name}` foi encerrado por inatividade."
                )

            except:
                pass

            await channel.delete(reason="Auto-close por inatividade")

        except Exception as e:
            print(f"[AUTO_CLOSE CLOSE ERROR] {e}")


# =========================
# 🚀 FACTORY
# =========================

def setup_auto_close(bot):
    return AutoCloseManager(bot)
