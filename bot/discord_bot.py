"""Tiny Discord bot for querying Vectara.

This script logs in using the ``DISCORD_TOKEN`` environment variable and
listens for messages that start with ``!ask``.  The remainder of the
message is treated as a search query which is forwarded to Vectara using
:func:`backend.query.search_vectara`.  The top result is posted back to
the channel.  It is deliberately minimal and intended as a smoke test
that the bot can connect and interact with the Vectara API.
"""

from __future__ import annotations

import os
import discord

from backend.query import search_vectara


class RagBot(discord.Client):
    async def on_ready(self) -> None:
        print(f"Logged in as {self.user} (id={self.user.id})")

    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return
        if message.content.startswith("!ask "):
            query = message.content[len("!ask "):].strip()
            results = search_vectara(query)
            answer = results[0] if results else "No results"
            await message.channel.send(answer)


def main() -> None:
    intents = discord.Intents.default()
    client = RagBot(intents=intents)
    client.run(os.getenv("DISCORD_TOKEN"))


if __name__ == "__main__":
    main()
