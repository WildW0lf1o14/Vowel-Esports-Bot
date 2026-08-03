#Author Stephen (WildW0lf) 
#Date of Creation: 03/08/2026

import sqlite3
from datetime import datetime
import os


DATABASE_PATH = "data/vowel.db"
#-------------------------------
#Valid roles
#-------------------------------
VALID_ROLES = [
    "Manager",
    "Captain",
    "Coach",
    "Tank",
    "DPS",
    "Support"
]

# -------------------------------
# Database Connection
# -------------------------------

def get_connection():
    """
    Creates and returns a database connection
    """

    # Create data folder if missing
    if not os.path.exists("data"):
        os.makedirs("data")

    connection = sqlite3.connect(DATABASE_PATH)

    # Allows accessing columns by name
    connection.row_factory = sqlite3.Row

    return connection



# -------------------------------
# Database Setup
# -------------------------------

def initialise_database():
    """
    Creates required database tables
    """

    connection = get_connection()
    cursor = connection.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS players (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        discord_id TEXT UNIQUE NOT NULL,

        discord_name TEXT NOT NULL,

        ign TEXT NOT NULL,

        real_name TEXT,

        team TEXT DEFAULT 'VOWEL Esports',

        role TEXT,

        is_captain INTEGER DEFAULT 0,

        is_contact INTEGER DEFAULT 0,

        active INTEGER DEFAULT 1,

        joined_date TEXT NOT NULL

    )
    """)


    connection.commit()
    connection.close()



# -------------------------------
# Add Player
# -------------------------------

def add_player(
        discord_id,
        discord_name,
        ign,
        real_name=None,
        role=None,
        team="VOWEL Esports"
):

    connection = get_connection()
    cursor = connection.cursor()


    try:

        cursor.execute("""
        INSERT INTO players
        (
            discord_id,
            discord_name,
            ign,
            real_name,
            team,
            role,
            joined_date
        )

        VALUES (?, ?, ?, ?, ?, ?, ?)

        """,
        (
            discord_id,
            discord_name,
            ign,
            real_name,
            team,
            role,
            datetime.now().strftime("%Y-%m-%d")
        ))


        connection.commit()

        return True


    except sqlite3.IntegrityError:

        return False


    finally:

        connection.close()



# -------------------------------
# Remove Player
# -------------------------------

def remove_player(discord_id):

    connection = get_connection()
    cursor = connection.cursor()


    cursor.execute("""
    DELETE FROM players
    WHERE discord_id = ?
    """,
    (discord_id,))


    connection.commit()


    removed = cursor.rowcount > 0


    connection.close()


    return removed



# -------------------------------
# Get Single Player
# -------------------------------

def get_player(discord_id):

    connection = get_connection()
    cursor = connection.cursor()


    cursor.execute("""
    SELECT *
    FROM players
    WHERE discord_id = ?
    """,
    (discord_id,))


    player = cursor.fetchone()


    connection.close()


    return player



# -------------------------------
# Get Full Roster
# -------------------------------

def get_roster():

    connection = get_connection()
    cursor = connection.cursor()


    cursor.execute("""
    SELECT *
    FROM players
    WHERE active = 1
    ORDER BY role
    """)


    players = cursor.fetchall()


    connection.close()


    return players



# -------------------------------
# Update Captain Status
# -------------------------------

def set_captain(discord_id, status=True):

    connection = get_connection()
    cursor = connection.cursor()


    cursor.execute("""
    UPDATE players

    SET is_captain = ?

    WHERE discord_id = ?

    """,
    (
        1 if status else 0,
        discord_id
    ))


    connection.commit()


    updated = cursor.rowcount > 0


    connection.close()


    return updated



# -------------------------------
# Update Contact Status
# -------------------------------

def set_contact(discord_id, status=True):

    connection = get_connection()
    cursor = connection.cursor()


    cursor.execute("""
    UPDATE players

    SET is_contact = ?

    WHERE discord_id = ?

    """,
    (
        1 if status else 0,
        discord_id
    ))


    connection.commit()


    updated = cursor.rowcount > 0


    connection.close()


    return updated



# -------------------------------
# Update Player Role
# -------------------------------

def update_role(discord_id, role):

    connection = get_connection()
    cursor = connection.cursor()


    cursor.execute("""
    UPDATE players

    SET role = ?

    WHERE discord_id = ?

    """,
    (role,))


    connection.commit()


    updated = cursor.rowcount > 0


    connection.close()


    return updated



# -------------------------------
# Test Database
# -------------------------------

if __name__ == "__main__":

    initialise_database()

    print("Database successfully created.")
