# holds the classes and objects which make up the program and structure its data. 

# imports from standard libraries 
import json 
import sqlite3
import os 

# imports from custom libraries 
from attributes2 import BasicAttributes, SpecialAttributes, HarmTracks, WoundThresholds, DamageDice 

class Ancestry: 
    # class to represent the ancestry of a character 
    def __init__(self, name, basic_attributes, special_ability, harm_tracks, wound_thresholds):
        self.name = name # name of the ancestry
        self.basic_attributes = basic_attributes # dictionary of basic attribute modifiers 
        self.special_ability = special_ability # special ability of the ancestry if present
        self.harm_tracks = harm_tracks # dictionary of harm track modifiers
        self.wound_thresholds = wound_thresholds # dictionary of wound threshold modifiers 

    def load_ancestry_data(ancestry_name):
        with open('character_options_json/ancestry_options.json', 'r') as file:
            ancestries = json.load(file)
            # Access the ancestry data by key
            ancestry_data = ancestries.get(ancestry_name)
            if ancestry_data:
                return ancestry_data
            else:
                return None
            
    def ancestry_update(character, ancestry_data):
        # update character with ancestry data
        character.ancestry = ancestry_data['name']

        for key, value in ancestry_data['basic_attributes'].items():
            character.basic_attributes[key] += value

        if 'harm_tracks' in ancestry_data and ancestry_data['harm_tracks']:
                for key, value in ancestry_data['harm_tracks'].items():
                    if key in character.harm_tracks:
                        character.harm_tracks[key] += value
                    else:
                        character.harm_tracks[key] = value

        for key, value in ancestry_data['damage_reduction'].items():
            if key in character.damage_reduction:
                character.damage_reduction[key] += value
            else:
                character.damage_reduction[key] = value

class Profession:
    # class to represent the profession of a character
    def __init__(self, name, abilities, damage_reduction):
        self.name = name # name of the profession
        self.abilities = abilities  # dictionary of abilities 
        self.damage_reduction = damage_reduction # dictionary of damage reduction modifiers

    def load_profession_data(profession_name):
        with open('character_options_json/profession_options.json', 'r') as file:
            professions = json.load(file)
            # Access the profession data by key
            profession_data = professions.get(profession_name)
            if profession_data:
                return profession_data
            else:
                return None
            
    def profession_update(character, profession_data):
        # update character with profession data
        character.profession = profession_data['name']
        # Check if abilities is not empty
        if profession_data['abilities']:
            # Directly add the ability as a key with a value, e.g., True
            character.abilities[profession_data['abilities']] = True

        # Assuming damage_reduction is handled correctly as per previous example
        for key, value in profession_data['damage_reduction'].items():
            if key in character.damage_reduction:
                character.damage_reduction[key] += value
            else:
                character.damage_reduction[key] = value
            
class Community: 
    # class to represent the community of a character 
    def __init__(self, name, abilities): 
        self.id = id # id of the community
        self.name = name # name of the community
        self.abilities = abilities # dictionary of abilities 

    def community_update(character, community_data):
        # update character with community data
        character.community = community_data['name']
        character.abilities.update(community_data['abilities'])

class Path: 
    # class to represent the path of a character 
    def __init__(self, name, health_modifier, path_passives, path_moves, damage_die, basic_attributes=None, special_attributes=None, harm_tracks=None, wound_thresholds=None, id=None):
        self.id = id # id of the path
        self.name = name # name of the path
        self.basic_attributes = basic_attributes if basic_attributes else BasicAttributes() # dictionary of basic attribute modifiers if applicable, otherwise, basic attributes are created
        self.special_attributes = special_attributes if special_attributes else SpecialAttributes() # dictionary of special attribute modifiers if applicable, otherwise, basic special attributes are created
        self.harm_tracks = harm_tracks if harm_tracks else HarmTracks() # dictionary of harm track modifiers if applicable, otherwise, basic harm tracks are created
        self.wound_thresholds = wound_thresholds if wound_thresholds else WoundThresholds() # dictionary of wound threshold modifiers if applicable, otherwise, basic wound thresholds are created
        self.damage_die = damage_die # damage die of the path
        self.path_passives = path_passives # dictionary of path passives
        self.path_moves = path_moves # dictionary of path moves

        # Handle health modifiers
        self.harm_tracks.update(health_modifier) # update harm tracks with health modifier

    def path_update(character, path_data):
        # update character with path data
        character.path = path_data['name']
        character.basic_attributes.update(path_data['basic_attributes'])
        character.special_attributes.update(path_data['special_attributes'])
        character.harm_tracks.update(path_data['harm_tracks'])
        character.wound_thresholds.update(path_data['wound_thresholds'])
        character.damage_die = path_data['damage_die']
        character.path_passives.update(path_data['path_passives'])
        character.path_moves.update(path_data['path_moves'])

class Character:
    # class to represent a character 
    def __init__(self, char_info, char_attributes, id=None):
        self.id = id # database id of character. obsolete for now 
        self.name = char_info.name
        self.age = char_info.age
        self.level = char_info.level
        self.xp = 0
        self.ancestry = char_info.ancestry
        self.profession = char_info.profession
        self.community = char_info.community
        self.path = char_info.path
        self.abilities = {} 
        self.inventory = {}
        self.moves = {}
        self.basic_attributes = char_attributes.basic_attributes
        self.special_attributes = char_attributes.special_attributes
        self.harm_tracks = char_attributes.harm_tracks
        self.wound_thresholds = char_attributes.wound_thresholds
        self.damage_reduction = char_attributes.damage_reduction
        self.damage_dice = char_attributes.damage_dice
        # the below is not used until the character has the relevant path giving them access to those resources. needs more dev :) 
        #self.mana_resources = {"Flame": 0, "Mist": 0, "Stone": 0, "Will": 0, "Wind": 0}
        #self.devotion_resources = {"Mercy": 0, "Wrath": 0} 
        #self.trickery_resources = {"Dice": "1d4", "Max Uses": 1}

class CharacterInfo: 
    # class to represent the basioc infor of a character 
    def __init__(self, name, age, level, ancestry, profession, community, path):
        self.name = name
        self.age = age
        self.level = level
        self.ancestry = ancestry
        self.profession = profession
        self.community = community
        self.path = path

class CharacterAttributes:
    def __init__(self, basic_attributes={"Prowess": 0, "Might": 0, "Presence": 0}, special_attributes={"Power": 1, "Armor Uses": 1, "Armor": 0}, harm_tracks={"Physical": 4, "Mental": 4, "Spiritual": 3}, wound_thresholds={"Light": 5, "Moderate": 7, "Severe": 9}, damage_reduction={"Physical": 0, "Mental": 0, "Spiritual": 0}, damage_dice={"Physical": "1d4", "Mental": "1d4", "Spiritual": "1d4"}):
        self.basic_attributes = basic_attributes
        self.special_attributes = special_attributes
        self.harm_tracks = harm_tracks
        self.wound_thresholds = wound_thresholds
        self.damage_reduction = damage_reduction
        self.damage_dice = damage_dice 