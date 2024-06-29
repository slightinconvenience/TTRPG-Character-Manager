# collection of functions to update character variables 

# imports from standard libraries
import json
import sqlite3
import os

# imports from custom libraries
import objects
import attributes2

# methods or functions that update data for character creation
def ancestry_update(character, ancestry_data):
    # update character with ancestry data
    character.ancestry = ancestry_data['name']

    for key, value in ancestry_data['basic_atttributes'].items():
        character.basic_attributes[key] += value
    else:
        character.basic_attributes[key] = value

    #character.abilites.update(ancestry_data['special_ability']) # special ability shoul be added to abilities dict in character instance

    for key, value in ancestry_data['harm_tracks'].items():
        character.harm_tracks[key] += value
    else:
        character.harm_tracks[key] = value
    
    for key, value in ancestry_data['damage_reduction'].items():
        character.damage_reduction[key] += value
    else:
        character.damage_reduction[key] = value

def profession_update(character, profession_data):
    # update character with profession data
    character.profession = profession_data['name']
    if profession_data['abilities']:
        character.abilities.update(profession_data['abilities'])

    for key, value in profession_data['damage_reduction'].items():
        character.damage_reduction[key] += value
    else:
        character.damage_reduction[key] = value

def community_update(character, community_data):
    # update character with community data
    character.community = community_data['name']
    character.abilities.update(community_data['abilities'])
    
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