# holds the classes and objects which make up the program and structure its data. 

# imports from standard libraries 
import json 
import sqlite3
import os 

# imports from custom libraries 
from attributes2 import BasicAttributes, SpecialAttributes, HarmTracks, WoundThresholds, DamageDice 

# imports from third party libraries

# imports from local libraries

class Ancestry: 
    # class to represent the ancestry of a character 
    def __init__(self, name, basic_attributes, special_ability, harm_tracks, wound_thresholds):
        self.name = name # name of the ancestry
        self.basic_attributes = basic_attributes # dictionary of basic attribute modifiers 
        self.special_ability = special_ability # special ability of the ancestry if present
        self.harm_tracks = harm_tracks # dictionary of harm track modifiers
        self.wound_thresholds = wound_thresholds # dictionary of wound threshold modifiers 

class Profession:
    # class to represent the profession of a character
    def __init__(self, name, abilities, special_attributes=None):
        self.name = name # name of the profession
        self.abilities = abilities  # dictionary of abilities 
        self.special_attributes = special_attributes if special_attributes else SpecialAttributes() # dictionary of special attributes and their modifiers if applicable, otherwise, basic special attributes are created

class Communtiy: 
    # class to represent the community of a character 
    def __init__(self, name, abilities): 
        self.id = id # id of the community
        self.name = name # name of the community
        self.abilities = abilities # dictionary of abilities

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
    def __init__(self, basic_attributes={"Prowess": 0, "Might": 0, "Presence": 0}, special_attributes={"Power": 1, "Armor Uses": 1, "Armor": 0}, harm_tracks={"Physical": 4, "Mental": 4, "Spiritual": 3}, wound_thresholds={"Light": 5, "Moderate": 7, "Severe": 9}, damage_dice={"Physical": "1d4", "Mental": "1d4", "Spiritual": "1d4"}):
        self.basic_attributes = basic_attributes
        self.special_attributes = special_attributes
        self.harm_tracks = harm_tracks
        self.wound_thresholds = wound_thresholds
        self.damage_dice = damage_dice 