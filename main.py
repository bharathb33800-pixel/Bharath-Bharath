
import os
import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = "[TKG] "

intents = discord.Intents.default()
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)


async def add_tkg_prefix(member):
    current_name = member.nick or member.name

    if current_name.casefold().startswith(PREFIX.casefold()):
        return

    try:
        await member.edit(
            nick=PREFIX + current_name,
            reason="TKG Auto Prefix"
        )
        print(f"Prefix added: {member.name}")

    except discord.Forbidden:
        print("Missing Manage Nicknames permission")

    except discord.HTTPException as error:
        print(f"Error: {error}")


@bot.event
async def on_ready():
    print(f"{bot.user} is online!")


@bot.event
async def on_member_join(member):
    await add_tkg_prefix(member)


@bot.event
async def on_voice_state_update(member, before, after):
    # Only add prefix when joining voice from outside
    if before.channel is None and after.channel is not None:
        await add_tkg_prefix(member)


if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN environment variable is missing")

bot.run(TOKEN)
