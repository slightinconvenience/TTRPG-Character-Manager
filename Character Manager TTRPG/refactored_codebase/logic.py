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
            character_to_load = input("Please enter the name of the character you would like to load: ").lower()
            load_character(character_to_load)
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
            if value is not None:
                print(f"{attr.capitalize()}: {value}")
    if character.special_attributes:
        print("\nSpecial Attributes:")
        for attr, value in character.special_attributes.items():
            if value is not None:
                print(f"{attr.capitalize()}: {value}")
    if character.harm_tracks:
        print("\nHarm Tracks:")
        for track, value in character.harm_tracks.items():
            if value is not None:
                print(f"{track.capitalize()}: {value}")
    if character.wound_thresholds:
        print("\nWound Thresholds:")
        for threshold, value in character.wound_thresholds.items():
            if value is not None:
                print(f"{threshold.capitalize()}: {value}")
    if character.damage_dice:
        print("\nDamage Dice:")
        for dice, value in character.damage_dice.items():
            if value is not None:
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
    while first_choice not in range(1, 4):
        print("Invalid choice. Please choose a number between 1 and 3.")
        first_choice = int(input("Enter the number of your choice: "))
    # increase the chosen attribute by 1
    first_attribute = list(attributes.keys())[first_choice - 1]
    attributes[first_attribute] += 1
    print("Choose the second attribute to increase:")
    for index, attribute in enumerate(attributes, 1):
        print(f"{index}. {attribute}")
    second_choice = int(input("Enter the number of your choice: "))
    while second_choice not in range(1, 4) or second_choice == first_choice:
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
    new_character_info = objects.CharacterInfo(name, age, level, selected_ancestry, selected_profession, selected_community, selected_path)
    new_character_attributes = objects.CharacterAttributes()
    new_character = objects.Character(new_character_info, new_character_attributes)
    # i need the elections for ancestry, profession, community, and path to pull the data and place it into the character object
    # i suppose this means the objects need to be refactored to account for this data being passed in so it accuratly represents the choice 

    # choose attribute improvements 
    new_character.basic_attributes = attribute_improvements()

    # print character information
    print("\nCharacter created successfully!")
    print_character_details(new_character)

    # save character to file
    choice = input("Would you like to save {new_character.name} to a file? [y/n]: ").lower()
    if choice == "y":
        print("Saving character...")
        save_character(new_character)
    else:
        print("Character not saved.")
        return None 

# save character function 
def save_character(character):
    # Ensure the 'characters' directory exists
    directory = 'path_to/characters'
    os.makedirs(directory, exist_ok=True)
    # serialize the character object to JSON
    character_data = {
        "name": character.name,
        "age": character.age,
        "level": character.level,
        "xp": character.xp,
        "ancestry": character.ancestry,
        "profession": character.profession,
        "community": character.community,
        "path": character.path,
        "moves": character.moves,
        "abilities": character.abilities,
        "inventory": character.inventory,
        "basic_attributes": character.basic_attributes,
        "special_attributes": character.special_attributes,
        "harm_tracks": character.harm_tracks,
        "wound_thresholds": character.wound_thresholds,
        "damage_dice": character.damage_dice
    }
    # create file name for character 
    filename = os.path.join(directory, f"{character.name.replace(' ', '_').lower()}_character.json")
    # save character data to json file
    try:
        with open(filename, "w") as file:
            json.dump(character_data, file, indent=4) 
        print(f"Character saved successfully to {filename}")
    except Exception as e:
        print(f"An error occurred while saving the character: {e}")
    
# load character function
def load_character(character):
    # Specify the directory where character files are stored
    directory = 'path_to/characters'
    filename = os.path.join(directory, f"{character.replace(' ', '_').lower()}_character.json")
    # load character data from json file
    try: 
        with open(filename, "r") as file:
            character_data = json.load(file)

        # create character instance from loaded data
        loaded_character_info = objects.CharacterInfo(
            character_data["name"],
            character_data["age"],
            character_data["level"],
            character_data["ancestry"],
            character_data["profession"],
            character_data["community"],
            character_data["path"]
        )
        loaded_character_attributes = objects.CharacterAttributes(
            character_data["basic_attributes"],
            character_data["special_attributes"],
            character_data["harm_tracks"],
            character_data["wound_thresholds"],
            character_data["damage_dice"]
        )
        loaded_character = objects.Character(loaded_character_info, loaded_character_attributes)
        print(f"Character loaded successfully from {filename}")
        print_character_details(loaded_character)
        return loaded_character 
    
    except Exception as e:
        print(f"An error occurred while loading the character: {e}")
    except FileNotFoundError:
        print(f"Character file not found: {filename}")
    return None 

