# holds the classes and objects which make up the program and structure its data. 

# imports from standard libraries 
import json 
import sqlite3
import os 

# imports from custom libraries 

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