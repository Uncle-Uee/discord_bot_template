import os
import discord.interactions
from typing import Final
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

# STEP 0: LOAD OUR TOKEN
load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)


# STEP 1: PREFIX COMMAND
@client.command(name="ping", help="Check the bot's latency")
async def ping(ctx):
    await ctx.send(f"Pong! | Responded in {round(client.latency * 1000)}ms")


# STEP 2: SLASH COMMANDS
@client.tree.command(name="hello", description="Say hello to the bot")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello, {interaction.user}!")


# LOG EVENTS
def _log_commands(interaction: discord.Interaction):
    print(f"Slash Command used by: {interaction.user} in channel: {interaction.channel} [Server: {interaction.guild}]")


# region MATH COMMANDS

@client.tree.command()
@app_commands.describe(
    a='The first value you want to add something to',
    b='The value you want to add to the first value',
)
async def add(interaction: discord.Interaction, a: int, b: int):
    """Adds two numbers together."""
    await interaction.response.send_message(f'{a} + {b} = {a + b}')


@client.tree.command()
@app_commands.describe(
    a='The first value you want to subtract something from',
    b='The value you want to subtract from the first value',
)
async def sub(interaction: discord.Interaction, a: int, b: int):
    """Subtracts two numbers together."""
    await interaction.response.send_message(f'{a} - {b} = {a - b}')


@client.tree.command()
@app_commands.describe(
    a='The first value you want to multiply',
    b='The value you want to multiply by',
)
async def multiply(interaction: discord.Interaction, a: int, b: int):
    """Multiplies two numbers together."""
    await interaction.response.send_message(f'{a} * {b} = {a * b}')


@client.tree.command()
@app_commands.describe(
    a='The first value you want to divide',
    b='The value you want to divide by',
)
async def divide(interaction: discord.Interaction, a: int, b: int):
    """Divides two numbers together."""
    if b == 0:
        await interaction.response.send_message("You a dom naai, you can't divide by zero!")
    else:
        await interaction.response.send_message(f'{a} / {b} = {a / b}')


# endregion

# region ADMIN COMMANDS

@client.tree.command(name="move_all")
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(source_channel="The voice channel to move members from",
                       destination_channel="The voice channel to move members to")
async def move_all(interaction: discord.Interaction, source_channel: discord.VoiceChannel,
                   destination_channel: discord.VoiceChannel):
    """Slash command to move all users from one voice channel to another."""
    members = source_channel.members

    if not members:
        await interaction.response.send_message(f'No members in {source_channel.name}.', ephemeral=True)
        return

    # Move all members to the destination channel
    for member in members:
        await member.move_to(destination_channel)

    await interaction.response.send_message(
        f'Moved all members from {source_channel.name} to {destination_channel.name}.')

    _log_commands(interaction)


@move_all.error
async def admin_command_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)


# endregion


# STEP 3: EVENT HANDLERS
@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')


@client.event
async def setup_hook():
    # Sync the commands with the Discord API
    await client.tree.sync()


# STEP 4: RUN THE BOT
def main():
    client.run(TOKEN)


if __name__ == '__main__':
    main()
