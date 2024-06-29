
import sqlite3
import json

def db_connection():
    return sqlite3.connect('slight_character_manager.db')

# basic add and update methods 

def add_ancestry(name, basic_attributes, special_ability, harm_tracks, wound_thresholds):
    conn = db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO ancestries (name, basic_attributes, special_ability, harm_tracks, wound_thresholds)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, json.dumps(basic_attributes), special_ability or 'No ability', json.dumps(harm_tracks), json.dumps(wound_thresholds)))
        conn.commit()
    finally:
        conn.close()

def update_ancestry(ancestry_id, name, basic_attributes, special_ability, harm_tracks, wound_thresholds):
    conn = db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            UPDATE ancestries
            SET name = ?, basic_attributes = ?, special_ability = ?, harm_tracks = ?, wound_thresholds = ?
            WHERE id = ?
        ''', (name, json.dumps(basic_attributes), special_ability or 'No ability', json.dumps(harm_tracks), json.dumps(wound_thresholds), ancestry_id))
        conn.commit()
    finally:
        conn.close()

def add_profession(name, abilities, special_attributes):
    conn = db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO professions (name, abilities, special_attributes)
            VALUES (?, ?, ?)
        ''', (name, json.dumps(abilities), json.dumps(special_attributes)))
        conn.commit()
    finally:
        conn.close()

def update_profession(profession_id, name, abilities, special_attributes):
    conn = db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            UPDATE professions
            SET name = ?, abilities = ?, special_attributes = ?
            WHERE id = ?
        ''', (name, json.dumps(abilities), json.dumps(special_attributes), profession_id))
        conn.commit()
    finally:
        conn.close()

def add_community(name, ability_or_modifier, special_attributes):
    conn = db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO communities (name, ability_or_modifier, special_attributes)
            VALUES (?, ?, ?)
        ''', (name, ability_or_modifier or 'No modifier', json.dumps(special_attributes)))
        conn.commit()
    finally:
        conn.close()

def update_community(community_id, name, ability_or_modifier, special_attributes):
    conn = db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            UPDATE communities
            SET name = ?, ability_or_modifier = ?, special_attributes = ?
            WHERE id = ?
        ''', (name, ability_or_modifier or 'No modifier', json.dumps(special_attributes), community_id))
        conn.commit()
    finally:
        conn.close()

def add_path(name, basic_attributes, special_attributes, harm_tracks, wound_thresholds, damage_die, path_passives, path_moves):
    conn = db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO paths (name, basic_attributes, special_attributes, harm_tracks, wound_thresholds, damage_die, path_passives, path_moves)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, json.dumps(basic_attributes), json.dumps(special_attributes), json.dumps(harm_tracks), json.dumps(wound_thresholds), json.dumps(damage_die), json.dumps(path_passives), json.dumps(path_moves)))
        conn.commit()
    finally:
        conn.close()

def update_path(path_id, name, basic_attributes, special_attributes, harm_tracks, wound_thresholds, damage_die, path_passives, path_moves):
    conn = db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            UPDATE paths
            SET name = ?, basic_attributes = ?, special_attributes = ?, harm_tracks = ?, wound_thresholds = ?, damage_die = ?, path_passives = ?, path_moves = ?
            WHERE id = ?
        ''', (name, json.dumps(basic_attributes), json.dumps(special_attributes), json.dumps(harm_tracks), json.dumps(wound_thresholds), damage_die or '1d4', json.dumps(path_passives), json.dumps(path_moves), path_id))
        conn.commit()
    finally:
        conn.close()

# ancestry specific methods

def add_drow_ancestry():
        # variables to pass to arguements for modularity 
        name = "Drow" 
        basic_attributes = {'presence': 1}
        special_ability = 'Underground Expertise'
        harm_tracks = {'mental': 1}
        wound_thresholds = {}
        # takes variables and adds data to database per the add_ancestry method 
        add_ancestry(name, basic_attributes, special_ability, harm_tracks, wound_thresholds) 

def add_dwarves_ancestry():
        # variables to pass to arguements for modularity 
        name = "Dwarves" 
        basic_attributes = {'might': 1}
        special_ability = 'Social Drink'
        harm_tracks = {'physical': 1}
        wound_thresholds = {}
        # takes variables and adds data to database per the add_ancestry method 
        add_ancestry(name, basic_attributes, special_ability, harm_tracks, wound_thresholds)

def add_elves_ancestry():
        # variables to pass to arguements for modularity 
        name = "Elves" 
        basic_attributes = {'presence': 1}
        special_ability = 'Historical Insight'
        harm_tracks = {}
        wound_thresholds = {'mental': 2}
        # takes variables and adds data to database per the add_ancestry method 
        add_ancestry(name, basic_attributes, special_ability, harm_tracks, wound_thresholds)

def add_faeries_ancestry():
        # variables to pass to arguements for modularity 
        name = "Faeries" 
        basic_attributes = {'prowess': 1}
        special_ability = 'Extra Reality'
        harm_tracks = {}
        wound_thresholds = {'spiritual': 2}
        # takes variables and adds data to database per the add_ancestry method 
        add_ancestry(name, basic_attributes, special_ability, harm_tracks, wound_thresholds)

def add_framed_ancestry():
        # variables to pass to arguements for modularity 
        name = "Framed" 
        basic_attributes = {'prowess': 1}
        special_ability = 'Death Avoidance'
        harm_tracks = {}
        wound_thresholds = {'physical': 2}
        # takes variables and adds data to database per the add_ancestry method 
        add_ancestry(name, basic_attributes, special_ability, harm_tracks, wound_thresholds)

def add_halflings_ancestry():
        # variables to pass to arguements for modularity 
        name = "Halflings" 
        basic_attributes = {'prowess': 1}
        special_ability = 'Hospitality'
        harm_tracks = {'physical': 1, 'mental': 1, 'spiritual': -1}
        wound_thresholds = {} 
        # takes variables and adds data to database per the add_ancestry method 
        add_ancestry(name, basic_attributes, special_ability, harm_tracks, wound_thresholds)

def add_humans_ancestry():
        # variables to pass to arguements for modularity 
        name = "Humans" 
        basic_attributes = {'might': 1}
        special_ability = 'Warrant Expertise'
        harm_tracks = {'mental': 1}
        wound_thresholds = {} 
        # takes variables and adds data to database per the add_ancestry method 
        add_ancestry(name, basic_attributes, special_ability, harm_tracks, wound_thresholds)

def add_orcs_ancestry():
        # variables to pass to arguements for modularity 
        name = "Orcs" 
        basic_attributes = {'might': 1}
        special_ability = 'Mighty Last Breath'
        harm_tracks = {'physical': 2, 'mental': -1} 
        wound_thresholds = {} 
        # takes variables and adds data to database per the add_ancestry method 
        add_ancestry(name, basic_attributes, special_ability, harm_tracks, wound_thresholds)

def add_tieflings_ancestry():
        # variables to pass to arguements for modularity 
        name = "Tieflings" 
        basic_attributes = {'prowess': 1}
        special_ability = 'Enhanced Recovery'
        harm_tracks = {'spiritual': 1} 
        wound_thresholds = {} 
        # takes variables and adds data to database per the add_ancestry method 
        add_ancestry(name, basic_attributes, special_ability, harm_tracks, wound_thresholds)

# profession specific methods 

def add_academic_profession():
        name = 'Academic'
        abilities = 'Research Boon'
        special_attributes = {} 

        add_profession(name, abilities, special_attributes) 

def add_common_profession():
        name = 'Common'
        abilities = 'Extra Bond'
        special_attributes = {} 

        add_profession(name, abilities, special_attributes) 

def add_criminal_profession():
        name = 'Criminal'
        abilities = 'Warrant Boon'
        special_attributes = {} 
        
        add_profession(name, abilities, special_attributes) 

def add_martial_profession():
        name = 'Martial'
        abilities = 'Placeholder1'
        special_attributes = {} 
        
        add_profession(name, abilities, special_attributes) 

def add_religious_profession():
        name = 'Religious'
        abilities = 'Placeholder2'
        special_attributes = {} 
        
        add_profession(name, abilities, special_attributes) 

def add_wilderness_profession():
        name = 'Wilderness'
        abilities = 'Journey Boon'
        special_attributes = {} 
        
        add_profession(name, abilities, special_attributes) 

# community specific methods 

def add_desertborne_community():
        name = 'Desertborne' 
        ability_or_modifier = 'Heat Resilience'
        special_attributes = {}

        add_community(name, ability_or_modifier, special_attributes)

def add_groveborne_community():
        name = 'Groveborne' 
        ability_or_modifier = 'Forest Expertise'
        special_attributes = {}

        add_community(name, ability_or_modifier, special_attributes)

def add_highborne_community():
        name = 'Highborne' 
        ability_or_modifier = 'Noble Parley'
        special_attributes = {}

        add_community(name, ability_or_modifier, special_attributes)

def add_loreborne_community():
        name = 'Loreborne' 
        ability_or_modifier = 'Lore Expertise'
        special_attributes = {}

        add_community(name, ability_or_modifier, special_attributes)

def add_Orderborne_community():
        name = 'Orderborne' 
        ability_or_modifier = 'Order Defiance'
        special_attributes = {}

        add_community(name, ability_or_modifier, special_attributes)

def add_ridgeborne_community():
        name = 'Ridgeborne' 
        ability_or_modifier = ''
        special_attributes = {'armor': 1} 

        add_community(name, ability_or_modifier, special_attributes)

def add_skyborne_community():
        name = 'Skyborne' 
        ability_or_modifier = 'Ally Recovery'
        special_attributes = {}

        add_community(name, ability_or_modifier, special_attributes)

def add_seaborne_community():
        name = 'Seaborne' 
        ability_or_modifier = 'Sea Resilience'
        special_attributes = {}

        add_community(name, ability_or_modifier, special_attributes)

def add_Slyborne_community():
        name = 'Slyborne' 
        ability_or_modifier = 'Criminal Insight'
        special_attributes = {}

        add_community(name, ability_or_modifier, special_attributes)

def add_underborne_community():
        name = 'Underborne' 
        ability_or_modifier = 'Darkness Defense'
        special_attributes = {}

        add_community(name, ability_or_modifier, special_attributes)

def add_wanderborne_community():
        name = 'Wanderborne' 
        ability_or_modifier = 'Nomad Camp'
        special_attributes = {}

        add_community(name, ability_or_modifier, special_attributes)

def add_wildborne_community():
        name = 'Wildborne' 
        ability_or_modifier = 'Wild Stealth'
        special_attributes = {}

        add_community(name, ability_or_modifier, special_attributes)

# list containing names of all communities 
communities = ['Desertborne', 'Groveborne', 'Highborne', 'Loreborne', 'Orderborne', 'Ridgeborne', 'Skyborne', 'Seaborne', 'Slyborne', 'Underborne', 'Wanderborne', 'Wildborne']
# path specific methods 

def add_mage_path(): 
        name = 'Mage'
        basic_attributes = {}
        special_attributes = {}
        harm_tracks = {'mental': 1}
        wound_thresholds = {}
        damage_die = {'physical': '1d6'}
        path_passives = ['Magic Potential', 'Channeled Through Me', 'Sphere Touched']
        path_moves = ['Channel', 'Manifest', 'Spell Defense']

        add_path(name, basic_attributes, special_attributes, harm_tracks, wound_thresholds, damage_die, path_passives, path_moves)

def add_priest_path(): 
        name = 'Priest'
        basic_attributes = {}
        special_attributes = {}
        harm_tracks = {'spiritual': 1}
        wound_thresholds = {}
        damage_die = {'physical': '1d6'}
        path_passives = ['Devotion', 'Devotions Weapon']
        path_moves = ['Pray', 'Orison', 'Petition']

        add_path(name, basic_attributes, special_attributes, harm_tracks, wound_thresholds, damage_die, path_passives, path_moves)

def add_rogue_path(): 
        name = 'Rogue'
        basic_attributes = {}
        special_attributes = {}
        harm_tracks = {}
        wound_thresholds = {'physical': 1}
        damage_die = {'physical': '1d6'}
        path_passives = ['Trickery', 'Hidden Knife']
        path_moves = ['Tricks of the Trade', 'Sneak Attack'] 

        add_path(name, basic_attributes, special_attributes, harm_tracks, wound_thresholds, damage_die, path_passives, path_moves)

def add_warrior_path(): 
        name = 'Warrior'
        basic_attributes = {}
        special_attributes = {}
        harm_tracks = {'physical': 2}
        wound_thresholds = {}
        damage_die = {'physical': '1d6'}
        path_passives = ['Fighting Style']
        path_moves = ['Reckless Attack', 'My Life for Yours'] 

        add_path(name, basic_attributes, special_attributes, harm_tracks, wound_thresholds, damage_die, path_passives, path_moves)

# method to add all ancestries 
def add_all_ancestries():
    add_drow_ancestry()
    add_dwarves_ancestry()
    add_elves_ancestry()
    add_faeries_ancestry()
    add_framed_ancestry()
    add_halflings_ancestry()
    add_humans_ancestry()
    add_orcs_ancestry()
    add_tieflings_ancestry()
      
# method to add all professions 
def add_all_professions():
    add_academic_profession()
    add_common_profession()
    add_criminal_profession()
    add_martial_profession()
    add_religious_profession()
    add_wilderness_profession()

# method to add all communities 
def add_all_communities():
    add_desertborne_community()
    add_groveborne_community()
    add_highborne_community()
    add_loreborne_community()
    add_Orderborne_community()
    add_ridgeborne_community()
    add_skyborne_community()
    add_seaborne_community()
    add_Slyborne_community()
    add_underborne_community()
    add_wanderborne_community()
    add_wildborne_community()

# method to add all paths 
def add_all_paths():
    add_mage_path()
    add_priest_path()
    add_rogue_path()
    add_warrior_path()

