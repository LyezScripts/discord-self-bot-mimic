--This bot replys to the mimiced user with exactly what they say how to use, !mimceuser <useid> !stopmimic (stops affected users) 

import discord
import asyncio
from datetime import datetime, timezone

TOKEN = "YOUR_DISCORD_ACCOUNT_TOKEN"

COMMAND_PREFIX = "!" --you can change this to anything EXAMPLE !


class MimicBot(discord.Client):
    def __init__(self):
        super().__init__(chunk_guilds_at_startup=False)
        self.target_id = None
        self.channel_id = None
        self.started_at = None

    async def on_ready(self):
        print(f"logged in as {self.user} ({self.user.id})")

    async def on_message(self, message):
        if message.author.id == self.user.id:
            if message.content.startswith(COMMAND_PREFIX):
                await self.handle_command(message)
            return

        if self.target_id is None or self.channel_id is None:
            return

        if message.channel.id != self.channel_id:
            return

        if self.started_at is not None and message.created_at < self.started_at:
            return

        if message.author.id != self.target_id:
            return

        if not message.content:
            return

        try:
            await message.reply(message.content, mention_author=False)
        except (discord.Forbidden, discord.HTTPException):
            pass

    async def handle_command(self, message):
        content = message.content.strip()

        if content.startswith(f"{COMMAND_PREFIX}mimicuser"):
            parts = content.split()
            if len(parts) < 2:
                return
            try:
                target = int(parts[1])
            except ValueError:
                return
            self.target_id = target
            self.channel_id = message.channel.id
            self.started_at = datetime.now(timezone.utc)
            try:
                await message.channel.send(f"mimicking {target}")
            except (discord.Forbidden, discord.HTTPException):
                pass

        elif content.startswith(f"{COMMAND_PREFIX}stopmimic"):
            self.target_id = None
            self.channel_id = None
            self.started_at = None
            try:
                await message.channel.send("stopped")
            except (discord.Forbidden, discord.HTTPException):
                pass


async def main():
    client = MimicBot()
    try:
        await client.start(TOKEN)
    except Exception as e:
        print(f"fatal: {type(e).__name__}: {e}")
    finally:
        if not client.is_closed():
            await client.close()


if __name__ == "__main__":
    asyncio.run(main())
