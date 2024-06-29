# instatiate the variables and attributes needs to make up the data attached to a character object 

# imports from standard libraries 
import json 
import sqlite3
import os 

# imports from custom libraries 

# imports from third party libraries

# imports from local libraries

# class to represent the basic attributes of a character
class BasicAttributes:
    # class to represent the basic attributes of a character
    def __init__(self, prowess=0, might=0, presence=0):
        self.prowess = prowess
        self.might = might
        self.presence = presence 
    # method to update the values of a specific attribute
    def update_attribute(self, attribute_name, value):
        if hasattr(self, attribute_name):
            setattr(self, attribute_name, value)
        else:
            print(f"Attribute {attribute_name} does not exist.")
    # method to get the value of a specific attribute
    def get_attribute(self, attribute_name):
        return getattr(self, attribute_name, None) 

# class to represent special attributes of a character
class SpecialAttributes:
    # class to represent the special attributes of a character
    def __init__(self, power=1, armor_uses=1, armor=0):
        self.power = power
        self.armor_uses = armor_uses
        self.armor = armor
    # method to update the value of a specific attribute
    def update_attribute(self, attribute_name, modifier):
        if hasattr(self, attribute_name):
            current_value = getattr(self, attribute_name)
            new_value = current_value + modifier
            setattr(self, attribute_name, new_value)
        else:
            print(f"Attribute {attribute_name} does not exist.")
    # method to get the value of a specific attribute
    def get_attribute(self, attribute_name):
        return getattr(self, attribute_name, None)
    
# class to represent harm tracks of a character
class HarmTracks:
    # class to represent the harm tracks of a character
    def __init__(self, physical=4, mental=4, spiritual=3):
        self.physical = physical
        self.mental = mental
        self.spiritual = spiritual
    # method to update the value of a specific attribute
    def update_attribute(self, attribute_name, modifier):
        if hasattr(self, attribute_name):
            current_value = getattr(self, attribute_name)
            new_value = current_value + modifier
            setattr(self, attribute_name, new_value)
        else:
            print(f"Attribute {attribute_name} does not exist.")
    # method to get the value of a specific attribute
    def get_attribute(self, attribute_name):
        return getattr(self, attribute_name, None)
    
# class to represent wound thresholds of a character
class WoundThresholds:
    # class to represent the wound thresholds of a character
    def __init__(self, light=5, moderate=7, severe=9):
        self.light = light
        self.moderate = moderate
        self.severe = severe
    # method to update the value of a specific attribute
    def update_attribute(self, attribute_name, modifier):
        if hasattr(self, attribute_name):
            current_value = getattr(self, attribute_name)
            new_value = current_value + modifier
            setattr(self, attribute_name, new_value)
        else:
            print(f"Attribute {attribute_name} does not exist.")
    # method to get the value of a specific attribute
    def get_attribute(self, attribute_name):
        return getattr(self, attribute_name, None)
    
# class to represent the damage die of a character
class DamageDice:
    # class to represent the damage die of a character
    def __init__(self, physical='1d4', mental='1d4', spiritual='1d4'):
        self.physical = physical
        self.mental = mental
        self.spiritual = spiritual
    # method to update the value of a specific attribute
    def update_attribute(self, attribute_name, new_value):
        if hasattr(self, attribute_name):
            setattr(self, attribute_name, new_value)
        else:
            print(f"Attribute {attribute_name} does not exist.") 
    # method to get the value of a specific attribute
    def get_attribute(self, attribute_name):
        return getattr(self, attribute_name, None)
    
# a class to represent the five types of mana of a character
class ManaResources:
    # class to represent the mana of a character
    def __init__(self, flame=0, mist=0, stone=0, will=0, wind=0):
        self.flame = flame
        self.mist = mist
        self.stone = stone
        self.will = will
        self.wind = wind
    # method to update the value of a specific attribute
    def update_attribute(self, attribute_name, modifier):
        if hasattr(self, attribute_name):
            current_value = getattr(self, attribute_name)
            new_value = current_value + modifier
            setattr(self, attribute_name, new_value)
        else:
            print(f"Attribute {attribute_name} does not exist.")
    # method to get the value of a specific attribute
    def get_attribute(self, attribute_name):
        return getattr(self, attribute_name, None)
    
# class to represent the two devotion types of a character 
class DevotionResource:
    def __init__(self, mercy=0, wrath=0):
        self.mercy = mercy
        self.wrath = wrath
    # method to update the value of a specific attribute
    def update_attribute(self, attribute_name, modifier):
        if hasattr(self, attribute_name):
            current_value = getattr(self, attribute_name)
            new_value = current_value + modifier
            setattr(self, attribute_name, new_value)
        else:
            print(f"Attribute {attribute_name} does not exist.")
    # method to get the value of a specific attribute
    def get_attribute(self, attribute_name):
        return getattr(self, attribute_name, None)
    
# a class to represent the trickery dice value, and current and maximum uses of a character
class TrickeryResource:
    def __init__(self, dice='1d4', uses=1, max_uses=1):
        self.dice = dice
        self.uses = uses
        self.max_uses = max_uses
    # method to update the value of a specific attribute
    def update_attribute(self, attribute_name, new_value):
        if hasattr(self, attribute_name):
            setattr(self, attribute_name, new_value)
        else:
            print(f"Attribute {attribute_name} does not exist.")
    # method to get the value of a specific attribute
    def get_attribute(self, attribute_name):
        return getattr(self, attribute_name, None)

# a class to represent the inventory of a character 
class Inventory:
    def __init__(self, items=[]):
        self.items = items
    # method to add an item to the inventory
    def add_item(self, item):
        self.items.append(item)
    # method to remove an item from the inventory
    def remove_item(self, item):
        self.items.remove(item)
    # method to get the value of a specific attribute
    def get_attribute(self, attribute_name):
        return getattr(self, attribute_name, None)
    
# a class to represent the moves of a character
class Moves:
    def __init__(self, moves=[]):
        self.moves = moves
    # method to add a move to the moves list
    def add_move(self, move):
        self.moves.append(move)
    # method to remove a move from the moves list
    def remove_move(self, move):
        self.moves.remove(move)
    # method to get the data of a specific move
    # ideally the data is stored in the database or in a json file and is retrieved when needed
    # otherwise the move is stored in the class instance as its id inside the database to be called later :) 