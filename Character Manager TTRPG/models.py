
# the data haolding classes are listed and detailed below 
# data structure definitions and specific data manipulation methods

# imports
import sqlite3 
import json

# methods and classes from other files 
from database import db_connection 
from attributes import BasicAttributes, SpecialAttributes, HarmTracks, WoundThresholds, DamageDice, ManaResource, DevotionResource, TrickeryDice 

class Ancestry:
    def __init__(self, name, basic_attributes, special_ability, harm_tracks, wound_thresholds):
        self.name = name
        self.basic_attributes = basic_attributes
        self.special_ability = special_ability
        self.harm_tracks = harm_tracks
        self.wound_thresholds = wound_thresholds

    def to_dict(self):
        return {
            "name": self.name,
            "basic_attributes": self.basic_attributes.to_dict(),
            "special_ability": self.special_ability,
            "harm_tracks": self.harm_tracks.to_dict(),
            "wound_thresholds": self.wound_thresholds.to_dict()
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            basic_attributes=BasicAttributes.from_dict(data["basic_attributes"]),
            special_ability=data["special_ability"],
            harm_tracks=HarmTracks.from_dict(data["harm_tracks"]),
            wound_thresholds=WoundThresholds.from_dict(data["wound_thresholds"])
        )
    
    def insert_ancestry(ancestry):
        conn = db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO ancestries (name, basic_attributes, special_ability, harm_tracks, wound_thresholds)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                ancestry.name,
                json.dumps(ancestry.basic_attributes.to_dict()),
                ancestry.special_ability,
                json.dumps(ancestry.harm_tracks.to_dict()),
                json.dumps(ancestry.wound_thresholds.to_dict())
            ))
            conn.commit()
        finally:
            conn.close()

    def load_ancestry(ancestry_id):
        conn = db_connection() 
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM ancestries WHERE id=?", (ancestry_id,))
            row = cursor.fetchone()
            if row:
                ancestry_data = {
                    'id': row[0],
                    'name': row[1],
                    'basic_attributes': json.loads(row[2]),
                    'special_ability': row[3],
                    'harm_tracks': json.loads(row[4]),
                    'wound_thresholds': json.loads(row[5])
                }
                return Ancestry.from_dict(ancestry_data)
        finally:
            conn.close()
        
class Profession:
    def __init__(self, name, abilities, special_attributes=None):
        self.name = name
        self.abilities = abilities  # This is a list or similar structure holding abilities.
        self.special_attributes = special_attributes if special_attributes else SpecialAttributes()

    def to_dict(self):
        return {
            "name": self.name,
            "abilities": self.abilities,
            "special_attributes": self.special_attributes.to_dict()
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            abilities=data["abilities"],
            special_attributes=SpecialAttributes.from_dict(data.get("special_attributes", {}))
        )
    
    def insert_profession(profession):
        conn = db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO professions (name, abilities, special_attributes)
                VALUES (?, ?, ?)
            ''', (
                profession.name,
                json.dumps(profession.abilities),
                json.dumps(profession.special_attributes.to_dict())
            ))
            conn.commit()
        finally:
            conn.close()
        
    def load_profession(profession_id):
        conn = db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM professions WHERE id=?", (profession_id,))
            row = cursor.fetchone()
            if row:
                return Profession.from_dict({
                    "name": row['name'],
                    "abilities": json.loads(row['abilities']),
                    "special_attributes": json.loads(row['special_attributes'])
                })
        finally:
            conn.close()
        
class Community:
    def __init__(self, name, ability_or_modifier, special_attributes=None, id=None):
        self.id = id
        self.name = name
        if isinstance(ability_or_modifier, dict):
            # If modifier is a dict, it's assumed to be attribute related
            self.special_attributes = SpecialAttributes.from_dict(ability_or_modifier)
        else:
            self.special_attributes = special_attributes if special_attributes else SpecialAttributes()
            self.ability_or_modifier = ability_or_modifier  # This could be a descriptive string or similar

    def to_dict(self):
        return {
            "name": self.name,
            "ability_or_modifier": self.ability_or_modifier,
            "special_attributes": self.special_attributes.to_dict()
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            ability_or_modifier=data["ability_or_modifier"],
            special_attributes=SpecialAttributes.from_dict(data["special_attributes"])
        )

    def insert_community(community):
        conn = db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO communities (name, special_attributes)
                VALUES (?, ?)
            ''', (
                community.name,
                json.dumps(community.to_dict())
            ))
            conn.commit()
        finally:
            conn.close()

    @classmethod
    def load_community(cls, community_id):
        conn = db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name, ability_or_modifier, special_attributes FROM communities WHERE id=?", (community_id,))
        row = cursor.fetchone()
        if row:
            name, ability_or_modifier, special_attributes = row
            community = cls(name, ability_or_modifier, special_attributes=SpecialAttributes.from_dict(json.loads(special_attributes)))
            community.id = row[0]
            return community
        else:
            return None 
        
class Path:
    def __init__(self, name, health_modifier, path_passives, path_moves, damage_die, basic_attributes=None, special_attributes=None, harm_tracks=None, wound_thresholds=None, id=None):
        self.id = id
        self.name = name
        self.basic_attributes = basic_attributes if basic_attributes else BasicAttributes()
        self.special_attributes = special_attributes if special_attributes else SpecialAttributes()
        self.harm_tracks = harm_tracks if harm_tracks else HarmTracks()
        self.wound_thresholds = wound_thresholds if wound_thresholds else WoundThresholds()
        self.damage_die = damage_die
        self.path_passives = path_passives
        self.path_moves = path_moves

        # Handle health modifiers
        self.harm_tracks.update(health_modifier)

    def to_dict(self):
        return {
            "name": self.name,
            "basic_attributes": self.basic_attributes.to_dict(),
            "special_attributes": self.special_attributes.to_dict(),
            "harm_tracks": self.harm_tracks.to_dict(),
            "wound_thresholds": self.wound_thresholds.to_dict(),
            "damage_die": self.damage_die,
            "path_passives": self.path_passives,
            "path_moves": self.path_moves
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            health_modifier=data["harm_tracks"],  # Assuming health_modifier is part of harm_tracks
            path_passives=data["path_passives"],
            path_moves=data["path_moves"],
            damage_die=data["damage_die"],
            basic_attributes=BasicAttributes.from_dict(data["basic_attributes"]),
            special_attributes=SpecialAttributes.from_dict(data["special_attributes"]),
            harm_tracks=HarmTracks.from_dict(data["harm_tracks"]),
            wound_thresholds=WoundThresholds.from_dict(data["wound_thresholds"])
        )
    
    def insert_path(path):
        conn = db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO paths (name, basic_attributes, special_attributes, harm_tracks, wound_thresholds, damage_die, path_passives, path_moves)
                VALUES (?,?,?,?,?,?,?,?)
            ''', (
                path.name,
                json.dumps(path.basic_attributes.to_dict()),
                json.dumps(path.special_attributes.to_dict()),
                json.dumps(path.harm_tracks.to_dict()),
                json.dumps(path.wound_thresholds.to_dict()),
                path.damage_die,
                json.dumps(path.path_passives),
                json.dumps(path.path_moves)
            ))
            conn.commit()
        finally:
            conn.close()

    def load_path(path_id):
        conn = db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM paths WHERE id=?", (path_id,))
        row = cursor.fetchone()
        if row:
            path = Path.from_dict({
                "name": row['name'],
                "basic_attributes": json.loads(row['basic_attributes']),
                "special_attributes": json.loads(row['special_attributes']),
                "harm_tracks": json.loads(row['harm_tracks']),
                "wound_thresholds": json.loads(row['wound_thresholds']),
                "damage_die": row['damage_die'],
                "path_passives": json.loads(row['path_passives']),
                "path_moves": json.loads(row['path_moves'])
            })
            path.id = row[0]
            return path

class Character:
    def __init__(self, name, age, ancestry, profession, community, path, id=None):
        self.id = id
        self.name = name
        self.age = age
        self.ancestry = ancestry
        self.profession = profession
        self.community = community
        self.path = path
        self.abilities = [] 
        self.basic_attributes = BasicAttributes()
        self.special_attributes = SpecialAttributes()
        self.harm_tracks = HarmTracks()
        self.wound_thresholds = WoundThresholds()
        self.damage_dice = DamageDice()
        

    def to_dict(self):
        """Serialize the character information for storage or transmission."""
        return {
            "name": self.name,
            "age": self.age,
            "ancestry_id": self.ancestry.id if self.ancestry else None,
            "profession_id": self.profession.id if self.profession else None,
            "community_id": self.community.id if self.community else None,
            "path_id": self.path.id if self.path else None,
            "attributes_data": {
                "basic_attributes": self.basic_attributes.to_dict(),
                "special_attributes": self.special_attributes.to_dict(),
                "harm_tracks": self.harm_tracks.to_dict(),
                "wound_thresholds": self.wound_thresholds.to_dict(),
                "damage_dice": self.damage_dice.to_dict(),
            }
        }

    @classmethod
    def from_dict(cls, data):
        # Deserialize components, assuming related IDs are used to fetch full objects elsewhere
        ancestry = Ancestry.from_dict(data["ancestry"]) if "ancestry" in data else None
        profession = Profession.from_dict(data["profession"]) if "profession" in data else None
        community = Community.from_dict(data["community"]) if "community" in data else None
        path = Path.from_dict(data["path"]) if "path" in data else None

        # Create character instance
        char = cls(
            name=data["personal_details"]["name"],
            age=data["personal_details"]["age"],
            ancestry=ancestry,
            profession=profession,
            community=community,
            path=path,
            id=data.get("id")  # Assume an optional ID key for database identity
        )
        
        # Load attributes
        char.basic_attributes = BasicAttributes.from_dict(data["attributes"]["basic_attributes"])
        char.special_attributes = SpecialAttributes.from_dict(data["attributes"]["special_attributes"])
        char.harm_tracks = HarmTracks.from_dict(data["attributes"]["harm_tracks"])
        char.wound_thresholds = WoundThresholds.from_dict(data["attributes"]["wound_thresholds"])
        char.damage_dice = DamageDice.from_dict(data["attributes"]["damage_dice"])

        return char
    
    def save(self):
        with sqlite3.connect('character_manager.db') as conn:
            cursor = conn.cursor()
            character_data = json.dumps(self.to_dict())
            if self.id:
                cursor.execute('''
                UPDATE characters SET name=?, age=?, ancestry_id=?, profession_id=?, community_id=?, path_id=?, attributes_data=?
                WHERE id=?
                ''', (self.name, self.age, self.ancestry.id, self.profession.id, self.community.id, self.path.id, character_data, self.id))
            else:
                cursor.execute('''
                INSERT INTO characters (name, age, ancestry_id, profession_id, community_id, path_id, attributes_data)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (self.name, self.age, self.ancestry.id, self.profession.id, self.community.id, self.path.id, character_data))
                self.id = cursor.lastrowid
            conn.commit()

    def load(self):
        if not self.id:
            raise ValueError("Character ID is not set.")
        
        with sqlite3.connect('character_manager.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM characters WHERE id=?", (self.id,))
            row = cursor.fetchone()
            if row:
                data = json.loads(row[7])  # Assuming attributes_data is stored in the 8th column (0-indexed 7)
                # Update current instance
                self.name = row[1]
                self.age = row[2]
                self.ancestry = Ancestry.load(row[3])  # Assuming a static method load() that fetches based on id
                self.profession = Profession.load(row[4])
                self.community = Community.load(row[5])
                self.path = Path.load(row[6])
                self.basic_attributes = BasicAttributes.from_dict(data["basic_attributes"])
                self.special_attributes = SpecialAttributes.from_dict(data["special_attributes"])
                self.harm_tracks = HarmTracks.from_dict(data["harm_tracks"])
                self.wound_thresholds = WoundThresholds.from_dict(data["wound_thresholds"])
                self.damage_dice = DamageDice.from_dict(data["damage_dice"])

class Moves:
    def __init__(self, basic=None, special=None, path=None):
        self.basic_moves = basic if basic else []
        self.special_moves = special if special else []
        self.path_moves = path if path else []