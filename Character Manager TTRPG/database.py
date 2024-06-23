
import sqlite3
import json 

from options_to_database import add_all_ancestries, add_all_professions, add_all_communities, add_all_paths

def db_connection():
    return sqlite3.connect('slight_character_manager.db')

def setup_database():
    # Connect to the SQLite3 database (it will be created if it doesn't exist)
    conn = db_connection()
    cursor = conn.cursor()
    
    # Create table for Ancestry
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ancestries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        basic_attributes TEXT NOT NULL,
        special_ability TEXT,
        harm_tracks TEXT NOT NULL,
        wound_thresholds TEXT NOT NULL
    )
    ''')
    
    # Create table for Profession
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS professions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        abilities TEXT NOT NULL,
        special_attributes TEXT
    )
    ''')
    
    # Create table for Community
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS communities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        ability_or_modifier TEXT,
        special_attributes TEXT
    )
    ''')
    
    # Create table for Path
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS paths (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        basic_attributes TEXT,
        special_attributes TEXT,
        harm_tracks TEXT,
        wound_thresholds TEXT,
        damage_die TEXT,
        path_passives TEXT,
        path_moves TEXT
    )
    ''')
    
    # Create table for Character
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS characters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        ancestry_id INTEGER,
        profession_id INTEGER,
        community_id INTEGER,
        path_id INTEGER,
        basic_attributes TEXT,
        special_attributes TEXT,
        harm_tracks TEXT,
        wound_thresholds TEXT,
        damage_dice TEXT,
        FOREIGN KEY (ancestry_id) REFERENCES ancestries(id),
        FOREIGN KEY (profession_id) REFERENCES professions(id),
        FOREIGN KEY (community_id) REFERENCES communities(id),
        FOREIGN KEY (path_id) REFERENCES paths(id)
    )
    ''')
    
    # Commit changes and close the connection
    conn.commit()
    conn.close()

def populate_initial_data():
        add_all_ancestries() 
        add_all_professions() 
        add_all_communities() 
        add_all_paths() 

# define the character options 

def ancestry_options():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM ancestries")
    ancestries = cursor.fetchall()
    print("\n--- Choose 1 Ancestry ---")
    for i, (id, name) in enumerate(ancestries, 1):
        print(f"{i}. {name}")
    selected_ancestry = None
    while selected_ancestry is None:
        try:
            choice = int(input("Select an ancestry by entering its number: "))
            if 1 <= choice <= len(ancestries):
                selected_ancestry = ancestries[choice - 1][0]
            else:
                print("Invalid selection. Please choose a number between 1 and {}.".format(len(ancestries)))
        except ValueError:
            print("Invalid selection. Please enter a number between 1 and {}.".format(len(ancestries)))
    return selected_ancestry

def profession_options():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM professions")
    professions = cursor.fetchall()
    print("\nAvailable Professions:")
    for i, (id, name) in enumerate(professions, 1):
        print(f"{i}. {name}")
    selected_profession = None
    while selected_profession is None:
        try:
            choice = int(input("Select a profession by entering its number: "))
            if 1 <= choice <= len(professions):
                selected_profession = professions[choice - 1][0]
            else:
                print("Invalid selection. Please choose a number between 1 and {}.".format(len(professions)))
        except ValueError:
            print("Invalid selection. Please enter a number between 1 and {}.".format(len(professions)))
    return selected_profession

def community_options():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM communities")
    communities = cursor.fetchall()
    print("\nAvailable Communities:")
    for i, (id, name) in enumerate(communities, 1):
        print(f"{i}. {name}")
    selected_community = None
    while selected_community is None:
        try:
            choice = int(input("Select a community by entering its number: "))
            if 1 <= choice <= len(communities):
                selected_community = communities[choice - 1][0]
            else:
                print("Invalid selection. Please choose a number between 1 and {}.".format(len(communities)))
        except ValueError:
            print("Invalid selection. Please enter a number between 1 and {}.".format(len(communities)))
    return selected_community

def path_options():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM paths")
    paths = cursor.fetchall()
    print("\nAvailable Paths:")
    for i, (id, name) in enumerate(paths, 1):
        print(f"{i}. {name}")
    selected_path = None
    while selected_path is None:
        try:
            choice = int(input("Select a path by entering its number: "))
            if 1 <= choice <= len(paths):
                selected_path = paths[choice - 1][0]
            else:
                print("Invalid selection. Please choose a number between 1 and {}.".format(len(paths)))
        except ValueError:
            print("Invalid selection. Please enter a number between 1 and {}.".format(len(paths)))
    return selected_path

# Call the method to set up the database
setup_database()

# call the methods to add the basic options and their relevant data
# populate_initial_data() 
