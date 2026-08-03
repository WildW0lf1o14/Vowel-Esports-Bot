#Author Stephen (WildW0lf) 
#Date of Creation: 03/08/2026

import discord
from discord import app_commands
from discord.ext import commands

import database


# -----------------------------------
# Bot Configuration
# -----------------------------------

TOKEN = "YOUR_BOT_TOKEN_HERE"


intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(
    command_prefix="!",
    intents=intents
)



# -----------------------------------
# Startup
# -----------------------------------

@bot.event
async def on_ready():

    database.initialise_database()

    try:

        synced = await bot.tree.sync()

        print(
            f"Logged in as {bot.user}"
        )

        print(
            f"Synced {len(synced)} commands"
        )


    except Exception as error:

        print(error)



# -----------------------------------
# Add Player
# -----------------------------------

@bot.tree.command(
    name="addplayer",
    description="Add a player to the VOWEL roster"
)
@app_commands.describe(
    member="Discord member",
    ign="In-game name",
    role="Player role",
    real_name="Optional real name"
)
async def addplayer(
    interaction: discord.Interaction,
    member: discord.Member,
    ign: str,
    role: str,
    real_name: str = None
):

    result = database.add_player(
        discord_id=str(member.id),
        discord_name=str(member),
        ign=ign,
        role=role,
        real_name=real_name
    )


    if result:

        await interaction.response.send_message(
            f"✅ {ign} has been added to the roster."
        )

    else:

        await interaction.response.send_message(
            "❌ Player already exists."
        )



# -----------------------------------
# Remove Player
# -----------------------------------

@bot.tree.command(
    name="removeplayer",
    description="Remove a player from the roster"
)
async def removeplayer(
    interaction: discord.Interaction,
    member: discord.Member
):

    result = database.remove_player(
        str(member.id)
    )


    if result:

        await interaction.response.send_message(
            f"✅ {member.display_name} removed."
        )

    else:

        await interaction.response.send_message(
            "❌ Player not found."
        )



# -----------------------------------
# Player Information
# -----------------------------------

@bot.tree.command(
    name="playerinfo",
    description="View player information"
)
async def playerinfo(
    interaction: discord.Interaction,
    member: discord.Member
):

    player = database.get_player(
        str(member.id)
    )


    if player is None:

        await interaction.response.send_message(
            "❌ Player not found."
        )

        return



    embed = discord.Embed(
        title=f"{player['ign']} Information",
        colour=discord.Colour.blue()
    )


    embed.add_field(
        name="Discord",
        value=player["discord_name"]
    )

    embed.add_field(
        name="Role",
        value=player["role"]
    )


    embed.add_field(
        name="Captain",
        value="⭐ Yes" if player["is_captain"] else "No"
    )


    embed.add_field(
        name="Opponent Contact",
        value="Yes" if player["is_contact"] else "No"
    )


    embed.add_field(
        name="Joined",
        value=player["joined_date"]
    )


    await interaction.response.send_message(
        embed=embed
    )



# -----------------------------------
# Display Roster
# -----------------------------------

@bot.tree.command(
    name="roster",
    description="Display current roster"
)
async def roster(
    interaction: discord.Interaction
):

    players = database.get_roster()


    if not players:

        await interaction.response.send_message(
            "Roster is currently empty."
        )

        return



    embed = discord.Embed(
        title="VOWEL Esports Roster",
        colour=discord.Colour.green()
    )


    for player in players:

        badges = ""

        if player["is_captain"]:
            badges += " ⭐ Captain"

        if player["is_contact"]:
            badges += " 📞 Contact"


        embed.add_field(
            name=player["ign"],
            value=
            f"Role: {player['role']}{badges}",
            inline=False
        )


    await interaction.response.send_message(
        embed=embed
    )



# -----------------------------------
# Set Captain
# -----------------------------------

@bot.tree.command(
    name="setcaptain",
    description="Assign captain status"
)
async def setcaptain(
    interaction: discord.Interaction,
    member: discord.Member
):

    result = database.set_captain(
        str(member.id),
        True
    )


    if result:

        await interaction.response.send_message(
            f"⭐ {member.display_name} is now captain."
        )

    else:

        await interaction.response.send_message(
            "❌ Player not found."
        )



# -----------------------------------
# Set Opponent Contact
# -----------------------------------

@bot.tree.command(
    name="setcontact",
    description="Assign opponent contact status"
)
async def setcontact(
    interaction: discord.Interaction,
    member: discord.Member
):

    result = database.set_contact(
        str(member.id),
        True
    )


    if result:

        await interaction.response.send_message(
            f"📞 {member.display_name} is now an opponent contact."
        )

    else:

        await interaction.response.send_message(
            "❌ Player not found."
        )



# -----------------------------------
# Change Role
# -----------------------------------

@bot.tree.command(
    name="setrole",
    description="Change player's role"
)
async def setrole(
    interaction: discord.Interaction,
    member: discord.Member,
    role: str
):

    result = database.update_role(
        str(member.id),
        role
    )


    if result:

        await interaction.response.send_message(
            f"✅ {member.display_name}'s role updated to {role}."
        )

    else:

        await interaction.response.send_message(
            "❌ Player not found."
        )



# -----------------------------------
# Run Bot
# -----------------------------------

bot.run(TOKEN)
