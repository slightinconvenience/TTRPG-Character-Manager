# holds the logic for the progam. 
# includes functions for initilizing the program, choosing the options inside, as well as running character generation and the save methods

# imports from standard libraries 
import json 
import sqlite3
import os 

# imports from custom libraries 
import character_options 
import objects 
import attributes2 

# imports from third party libraries

# imports from local libraries

def start_program(): 
    # function to start the program 
    while True:
        print("Welcome to the character generator!")
        print("Please choose an option from the following: ")
        print("1. Generate a new character")
        print("2. Load a character")
        print("3. Exit")
        choice = input("Please enter the number of your choice: ")
        if choice == "1": 
            create_character()
        elif choice == "2": 
            load_character()
        elif choice == "3": 
            exit()
        else: 
            print("Invalid choice, please try again")

# function to print character details
def print_character_details(character):
    print("\nCharacter Details:")
    print(f"Name: {character.name}")
    print(f"Age: {character.age}")
    if character.ancestry:
        print(f"Ancestry: {character.ancestry}")
    if character.profession:
        print(f"Profession: {character.profession}")
    if character.community:
        print(f"Community: {character.community}")
    if character.path:
        print(f"Path: {character.path}")
    if character.basic_attributes:
        print("\nAttributes:")
        for attr, value in character.basic_attributes.items():
            if value:
                print(f"{attr.capitalize()}: {value}")
    if character.special_attributes:
        print("\nSpecial Attributes:")
        for attr, value in character.special_attributes.items():
            if value:
                print(f"{attr.capitalize()}: {value}")
    if character.harm_tracks:
        print("\nHarm Tracks:")
        for track, value in character.harm_tracks.items():
            if value:
                print(f"{track.capitalize()}: {value}")
    if character.wound_thresholds:
        print("\nWound Thresholds:")
        for threshold, value in character.wound_thresholds.items():
            if value:
                print(f"{threshold.capitalize()}: {value}")
    if character.damage_dice:
        print("\nDamage Dice:")
        for dice, value in character.damage_dice.items():
            if value:
                print(f"{dice.capitalize()}: {value}")

def attribute_improvements():
    # advanced function to dynamically handle attribute improvements
    print("\nYou can increase two of the three basic attributes (Prowess, Might, Presence) by 1.")
    print("Choose the first attribute to increase:")
    attributes = {"Prowess": 0, "Might": 0, "Presence": 0}
    # display attribute choices
    for index, attribute in enumerate(attributes, 1):
        print(f"{index}. {attribute}")
    first_choice = int(input("Enter the number of your choice: "))
    # prevent invalid choices
    while first_choice not in range(1, 3):
        print("Invalid choice. Please choose a number between 1 and 3.")
        first_choice = int(input("Enter the number of your choice: "))
    # increase the chosen attribute by 1
    first_attribute = list(attributes.keys())[first_choice - 1]
    attributes[first_attribute] += 1
    print("Choose the second attribute to increase:")
    for index, attribute in enumerate(attributes, 1):
        print(f"{index}. {attribute}")
    second_choice = int(input("Enter the number of your choice: "))
    while second_choice not in range(1, 3) or second_choice == first_choice:
        print("Invalid choice. Please choose a different number between 1 and 3.")
        second_choice = int(input("Enter the number of your choice: "))
    # increase the chosen attribute by 1
    second_attribute = list(attributes.keys())[second_choice - 1]
    attributes[second_attribute] += 1
    #return attributes
    attribute_improvements = attributes
    base_attributes = {"Prowess": 0, "Might": 0, "Presence": 0} 
    for attribute, value in attribute_improvements.items():
        if attribute in base_attributes:
            base_attributes[attribute] += value
    return base_attributes

# create character function
def create_character(): 
    # function to create a new character
    print("Creating a new character")
    # basic character information
    name = input("Please enter the name of your character: ")
    age = int(input("Enter your character's age: ")) 
    # basic character data 
    level = 1 # starting level 
    xp = 0 # starting xp
    # interactive selection of character options
    selected_ancestry = character_options.ancestry_options()
    selected_profession = character_options.profession_options() 
    selected_community = character_options.community_options()
    selected_path = character_options.path_options()

    # create character instance with selected options
    new_character = objects.Character(name, age, level, selected_ancestry, selected_profession, selected_community, selected_path)
    # i need the elections for ancestry, profession, community, and path to pull the data and place it into the character object
    # i suppose this means the objects need to be refactored to account for this data being passed in so it accuratly represents the choice 

    # choose attribute improvements 
    new_character.basic_attributes = attribute_improvements()

    # print character information
    print("\nCharacter created successfully!")
    print_character_details(new_character) 

