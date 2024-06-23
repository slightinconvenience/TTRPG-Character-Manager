
# bruh 

# import 
import json 
import sqlite3
import os 

# methods and classes from other files 
import database 
from models import Character, Ancestry, Profession, Community, Path
from attributes import BasicAttributes, SpecialAttributes, HarmTracks, WoundThresholds, DamageDice, ManaResource, DevotionResource, TrickeryDice 

def initialize_program():
    while True:
        print("\nWelcome to the Character Manager:")
        print("1. Create New Character")
        print("2. Load Existing Character")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            # Placeholder for the function to create a new character
            print("Creating a new character...")
            create_character()
        elif choice == '2':
            # Placeholder for the function to load an existing character
            character_name = input("Enter the character's name to load: ")
            print(f"Loading character: {character_name}...")
            load_character(character_name)
        elif choice == '3':
            print("Exiting the Character Manager.")
            break
        else:
            print("Invalid choice, please choose 1, 2, or 3.")

# saving and loading characters 
def save_character(character):
    # Ensure the 'characters' directory exists
    directory = 'path_to/characters'
    os.makedirs(directory, exist_ok=True)

    # Serialize each component of the character to JSON
    character_data = {
        "name": character.name,
        "age": character.age,
        "ancestry_id": character.ancestry.id,
        "profession_id": character.profession.id,
        "community_id": character.community.id,
        "path_id": character.path.id,
        "level": character.level,
        "basic_attributes": character.basic_attributes.to_dict(),
        "special_attributes": character.special_attributes.to_dict(),
        "harm_tracks": character.harm_tracks.to_dict(),
        "wound_thresholds": character.wound_thresholds.to_dict(),
        "damage_dice": character.damage_dice.to_dict(),
        "mana_resource": character.mana_resource.to_dict(),
        "devotion_resource": character.devotion_resource.to_dict(),
        "trickery_dice": character.trickery_dice.to_dict()
    }

    # Determine the filename to save the JSON data
    filename = os.path.join(directory, f"{character.name.replace(' ', '_').lower()}_character.json")

    # Save the JSON data to a file
    try:
        with open(filename, 'w') as file:
            json.dump(character_data, file, indent=4)
        print(f"Character '{character.name}' saved successfully to '{filename}'")
    except Exception as e:
        print(f"Error saving character to file: {str(e)}")

def load_character(character_name):
    # Specify the directory where character files are stored
    directory = 'path_to/characters'
    filename = os.path.join(directory, f"{character_name.replace(' ', '_').lower()}_character.json")
    
    try:
        # Open the character JSON file and load its content
        with open(filename, 'r') as file:
            character_data = json.load(file)

        # Assuming that all attribute classes have a from_dict method to deserialize
        ancestry = Ancestry.from_dict(character_data['ancestry'])
        profession = Profession.from_dict(character_data['profession'])
        community = Community.from_dict(character_data['community'])
        path = Path.from_dict(character_data['path'])
        basic_attributes = BasicAttributes.from_dict(character_data['attributes']['basic_attributes'])
        special_attributes = SpecialAttributes.from_dict(character_data['attributes']['special_attributes'])
        harm_tracks = HarmTracks.from_dict(character_data['attributes']['harm_tracks'])
        wound_thresholds = WoundThresholds.from_dict(character_data['attributes']['wound_thresholds'])
        damage_dice = DamageDice.from_dict(character_data['attributes']['damage_dice'])
        mana_resource = ManaResource.from_dict(character_data['attributes']['mana_resource'])
        devotion_resource = DevotionResource.from_dict(character_data['attributes']['devotion_resource'])
        trickery_dice = TrickeryDice.from_dict(character_data['attributes']['trickery_dice'])

        # Create the Character object with the loaded data
        character = Character(
            name=character_data['name'],
            age=character_data['age'],
            ancestry=ancestry,
            profession=profession,
            community=community,
            path=path,
            level=character_data['level'],
            basic_attributes=basic_attributes,
            special_attributes=special_attributes,
            harm_tracks=harm_tracks,
            wound_thresholds=wound_thresholds,
            damage_dice=damage_dice,
            mana_resource=mana_resource,
            devotion_resource=devotion_resource,
            trickery_dice=trickery_dice
        )

        return character
    except FileNotFoundError:
        print(f"Character file '{filename}' not found.")
    except Exception as e:
        print(f"Error loading character from file: {str(e)}")
    return None

# updating character instance details with choices made during character creation 
def create_character():
    """
    Character creation function incorporating all detailed options with interactive selections.
    """

    # Basic character info
    print("Welcome to the Character Creation Wizard!")
    name = input("Enter your character's name: ")
    age = int(input("Enter your character's age: "))

    # Initialize character with selected components
    level = 1  # Starting level for all characters

    # Interactive selections for detailed components
    print("\n--- Choose 1 Ancestry ---")
    ancestry_id = database.ancestry_options() 
    selected_ancestry = Ancestry.load_ancestry(ancestry_id) 
    print("\n--- Choose 1 Profession ---")
    profession_id = database.profession_options()
    selected_profession = Profession.load_profession(profession_id) 
    print("\n--- Choose 1 Community ---")
    community_id = database.community_options()
    selected_community = Community.load_community(community_id)
    print("\n--- Choose 1 Path ---")
    path_id = database.path_options()
    selected_path = Path.load_path(path_id) 

    # Create the Character instance with the selected components
    new_character = Character(name, age, selected_ancestry, selected_profession, selected_community, selected_path, level)

    # Print the current values of the basic attributes
    print("\nCurrent attribute values:")
    for attr, value in new_character.basic_attributes.items():
        print(f"{attr.capitalize()}: {value}")

    # Allow user to choose initial attributes
    print("\nYou can increase two of the three basic attributes (Prowess, Might, Presence) by 1.")
    first_choice = input("Choose the first attribute to increase: ").lower()
    second_choice = input("Choose the second attribute to increase: ").lower()

    while first_choice == second_choice:
        print("You cannot choose the same attribute twice. Please choose a different attribute.")
        second_choice = input("Choose the second attribute to increase: ").lower()

    # Apply initial choices
    if first_choice in new_character.basic_attributes:
        new_character.basic_attributes[first_choice] += 1
    if second_choice in new_character.basic_attributes:
        new_character.basic_attributes[second_choice] += 1
    
    # Final review of the created character
    print_character_details(new_character)

    return new_character

# applying the effects of character creation choices :) 
def apply_component_effects(self):
    components = [self.ancestry, self.profession, self.community, self.path]
    for component in components:
        if component:
            self.apply_effects(component)

def apply_effects(self, component):
    """
    Applies attribute bonuses and other modifiers based on the type of the component.
    """
    if isinstance(component, Ancestry):
        for attr, bonus in component.attribute_modifiers.items():
            if attr in self.attributes.basic_attributes:
                self.attributes.basic_attributes[attr] += bonus
        self.attributes.harm_tracks.update(component.health_modifier)

    elif isinstance(component, Profession):
        # Here, you might extend functionality to add abilities to the character
        pass

    elif isinstance(component, Community):
        if isinstance(component.ability_or_modifier, dict):  # Check if it's a dictionary (attribute modifier)
            # Assuming 'armor' directly modifies a special_attributes attribute
            armor_bonus = component.ability_or_modifier.get('armor', 0)
            self.attributes.special_attributes['armor_uses'] += armor_bonus
        else:
            # Handle string abilities as before or extend functionality
            pass

    elif isinstance(component, Path):
        self.attributes.harm_tracks.update(component.health_modifier)
        self.attributes.damage_dice = component.damage_die
        # Example of handling path passives and moves
        # This assumes there are methods to add passives and moves
        # self.passives.extend(component.path_passives)
        # self.moves.extend(component.path_moves) coo

# prints character details following creation 
def print_character_details(character):
    """
    Prints the details of a character instance.

    :param Character character: The character instance to print.
    """

    print("\nCharacter Details:")
    print(f"Name: {character.name}")
    print(f"Age: {character.age}")
    if character.ancestry:
        print(f"Ancestry: {character.ancestry.name}")
    if character.profession:
        print(f"Profession: {character.profession.name}")
    if character.community:
        print(f"Community: {character.community.name}")
    if character.path:
        print(f"Path: {character.path.name}")
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
    if character.resources:
        print("\nResources:")
        for resource, value in character.resources.items():
            if value:
                print(f"{resource.capitalize()}: {value}")