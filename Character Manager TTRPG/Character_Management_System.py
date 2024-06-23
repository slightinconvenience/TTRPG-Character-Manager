import json
import re 
import os 

def main_menu():
    while True:
        # Display the main menu
        print("\nWelcome to the Character Manager:")
        print("1. Create New Character")
        print("2. Load Existing Character")
        print("3. Exit")

        # Get user choice
        choice = input("Enter your choice (1-3): ")

        # Handle the user's input
        if choice == '1':
            new_character = update_character_creation_with_details()
            save_character(new_character)
        elif choice == '2':
            character_name = input("Enter the character's name to load: ")
            try:
                loaded_character = load_character(f"{character_name}_Character.json")
                print(f"Loaded character: {loaded_character.personal_details['name']}")
            except FileNotFoundError:
                print("Character file not found.")
            except Exception as e:
                print(f"An error occurred: {str(e)}")
        elif choice == '3':
            print("Exiting the Character Manager.")
            break
        else:
            print("Invalid choice, please choose 1, 2, or 3.")
# obso
class Ancestry:
    def __init__(self, name, attribute_modifiers, special_ability, health_modifier):
        self.name = name
        self.attribute_modifiers = attribute_modifiers
        self.special_ability = special_ability
        self.health_modifier = health_modifier

    def to_dict(self):
        return {
            "name": self.name,
            "attribute_modifiers": self.attribute_modifiers,
            "special_ability": self.special_ability,
            "health_modifier": self.health_modifier
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["attribute_modifiers"], data["special_ability"], data["health_modifier"])
# obso
class Profession:
    def __init__(self, name, ability):
        self.name = name
        self.ability = ability

    def to_dict(self):
        return {
            "name": self.name,
            "ability": self.ability
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["ability"])
# obso
class Community:
    def __init__(self, name, ability_or_modifier):
        self.name = name
        self.ability_or_modifier = ability_or_modifier

    def to_dict(self):
        return {
            "name": self.name,
            "ability_or_modifier": self.ability_or_modifier
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["ability_or_modifier"])
# obso
class Path:
    def __init__(self, name, health_modifier, path_passives, path_moves, damage_die):
        self.name = name
        self.health_modifier = health_modifier
        self.path_passives = path_passives
        self.path_moves = path_moves
        self.damage_die = damage_die

    def to_dict(self):
        return {
            "name": self.name,
            "health_modifier": self.health_modifier,
            "path_passives": self.path_passives,
            "path_moves": self.path_moves,
            "damage_die": self.damage_die
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["health_modifier"], data["path_passives"], data["path_moves"], data["damage_die"])
# obso
class EnhancedAttributes:
    def __init__(self, prowess=0, might=0, presence=0, power=0, armor_uses=1):
        self.basic_attributes = {'prowess': prowess, 'might': might, 'presence': presence}
        self.special_attributes = {'power': power, 'armor_uses': armor_uses}
        self.harm_tracks = {'physical': [4, 4], 'mental': [4, 4], 'spiritual': [3, 3]}
        self.wound_thresholds = {'minor': 5, 'major': 7, 'severe': 9}
        self.damage_dice = {'physical': '1d4', 'mental': '1d4', 'spiritual': '1d4'}
        self.resources = {
            'mana': {'current': 0, 'max': 10},
            'mercy': {'current': 0, 'max': 10},
            'wrath': {'current': 0, 'max': 10},
            'trickery_dice': {'current': 0, 'max': 5}
        }

    def update_resource(self, resource_name, amount, is_current=True):
        resource = self.resources.get(resource_name)
        if resource:
            key = 'current' if is_current else 'max'
            resource[key] = max(0, min(resource[key] + amount, resource['max'] if is_current else float('inf')))
            self.resources[resource_name] = resource

    def to_dict(self):
        return {
            'basic_attributes': self.basic_attributes,
            'special_attributes': self.special_attributes,
            'harm_tracks': self.harm_tracks,
            'wound_thresholds': self.wound_thresholds,
            'damage_dice': self.damage_dice,
            'resources': self.resources
        }

    @classmethod
    def from_dict(cls, data):
        instance = cls(
            prowess=data['basic_attributes'].get('prowess', 0),
            might=data['basic_attributes'].get('might', 0),
            presence=data['basic_attributes'].get('presence', 0),
            power=data['special_attributes'].get('power', 0),
            armor_uses=data['special_attributes'].get('armor_uses', 1)
        )
        instance.harm_tracks = data.get('harm_tracks', {})
        instance.wound_thresholds = data.get('wound_thresholds', {})
        instance.damage_dice = data.get('damage_dice', {})
        instance.resources = data.get('resources', {})
        return instance
# obso
class FinalEnhancedAttributes(EnhancedAttributes):
    def __init__(self, prowess=0, might=0, presence=0, power=0, armor_uses=1):
        super().__init__(prowess, might, presence, power, armor_uses)

    def update_power(self, level):
        power_levels = {1: 1, 3: 2, 5: 3, 7: 4, 10: 5}
        self.special_attributes['power'] = power_levels.get(level, 1)

    def set_resource(self, resource_name, current, max):
        """Sets the resource current and max directly."""
        if resource_name in self.resources:
            self.resources[resource_name]['current'] = current
            self.resources[resource_name]['max'] = max

    def to_dict(self):
        data = super().to_dict()  # Call the base class method to get the base dictionary
        # Add subclass-specific properties if any
        # Example: data['additional_property'] = self.additional_property
        return data

    @classmethod
    def from_dict(cls, data):
        obj = super(FinalEnhancedAttributes, cls).from_dict(data)  # Ensure this calls EnhancedAttributes.from_dict
        # Load any additional properties if FinalEnhancedAttributes has more beyond EnhancedAttributes
        return obj
# implement
class Moves:
    def __init__(self, basic=None, special=None, path=None):
        self.basic_moves = basic if basic else []
        self.special_moves = special if special else []
        self.path_moves = path if path else []
# obso
class Character:
    def __init__(self, name, age, ancestry, profession, community, path, level):
        self.personal_details = {'name': name, 'age': age}
        self.ancestry = ancestry
        self.profession = profession
        self.community = community
        self.path = path
        self.level = level
        self.attributes = FinalEnhancedAttributes()  # Initialize with the most comprehensive attribute class
        self.moves = []  # Placeholder for character moves
        self.apply_component_effects()  # Apply effects from ancestry, profession, community, and path
        self.update_power()  # Update power based on level

    def to_dict(self):
        return {
        "personal_details": self.personal_details,
        "ancestry": self.ancestry.to_dict(),
        "profession": self.profession.to_dict(),
        "community": self.community.to_dict(),
        "path": self.path.to_dict(),
        "level": self.level,
        "attributes": self.attributes.to_dict()  # Ensure this method captures all custom settings
    }

    @classmethod
    def from_dict(cls, data):
        ancestry = Ancestry.from_dict(data["ancestry"])
        profession = Profession.from_dict(data["profession"])
        community = Community.from_dict(data["community"])
        path = Path.from_dict(data["path"])
        char = cls(
            name=data["personal_details"]["name"],
            age=data["personal_details"]["age"],
            ancestry=ancestry,
            profession=profession,
            community=community,
            path=path,
            level=data["level"]
        )
        char.attributes = FinalEnhancedAttributes.from_dict(data["attributes"])
        return char

    def apply_component_effects(self):
        components = [self.ancestry, self.profession, self.community, self.path]
        for component in components:
         if component:
            self.apply_effects(component)

    def apply_effects(self, component):
        """
        Applies attribute bonuses and other modifiers based on the type of the component.
        """
        # Handle Ancestry: attribute modifiers and health modifiers
        if isinstance(component, Ancestry):
            for attr, bonus in component.attribute_modifiers.items():
                if attr in self.attributes.basic_attributes:
                    self.attributes.basic_attributes[attr] += bonus
            self.attributes.harm_tracks.update(component.health_modifier)

        # Handle Profession: primarily abilities (may be expanded to include attribute modifiers if needed)
        elif isinstance(component, Profession):
            # Here, you might extend functionality to add abilities to the character
            pass

        # Handle Community
        elif isinstance(component, Community):
            if isinstance(component.ability_or_modifier, dict):  # Check if it's a dictionary (attribute modifier)
            # Assuming 'armor' directly modifies a special_attributes attribute
                armor_bonus = component.ability_or_modifier.get('armor', 0)
                self.attributes.special_attributes['armor_uses'] += armor_bonus
            else:
            # Handle string abilities as before or extend functionality
                pass

        # Handle Path: health modifiers, damage dice, path passives, and moves
        elif isinstance(component, Path):
            self.attributes.harm_tracks.update(component.health_modifier)
            self.attributes.damage_dice = component.damage_die
            # Example of handling path passives and moves
            # This assumes there are methods to add passives and moves
            # self.passives.extend(component.path_passives)
            # self.moves.extend(component.path_moves)

    def update_power(self):
        # Adjust power based on level
        power_levels = {1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 9: 5, 10: 5}
        self.attributes.special_attributes['power'] = power_levels.get(self.level, 1)

    def update_harm_track(self, harm_type, amount):
        """Updates the harm track, ensuring it does not exceed its maximum limit."""
        current, maximum = self.attributes.harm_tracks[harm_type]
        self.attributes.harm_tracks[harm_type] = [max(0, min(current + amount, maximum)), maximum]

def print_character_details(character):
    print("\nFinal character details:")
    print(f"Name: {character.personal_details['name']}, Age: {character.personal_details['age']}")
    print("Attributes:", character.attributes.basic_attributes)
    print("Special Attributes:", character.attributes.special_attributes)
    print("Harm Tracks:", character.attributes.harm_tracks)
    print("Wound Thresholds:", character.attributes.wound_thresholds)
    print("Damage Dice:", character.attributes.damage_dice)
    print("Power:", character.attributes.special_attributes['power'])
    print("Resources:", {k: v for k, v in character.attributes.resources.items() if v['current'] > 0})  # Displays only used resources

def define_detailed_options():
    """
    Define detailed options for Ancestry, Profession, Community, and Path with all attributes, moves,
    abilities, and specific modifiers as provided.
    """
    ancestries = [
        Ancestry("Drow", {'presence': 1}, ["Underground Expertise"], {'mental_harm': 1}),
        Ancestry("Dwarves", {'might': 1}, ["Social Drink"], {'physical_harm': 1}),
        Ancestry("Elves", {'presence': 1}, ["Historical Insight"], {'mental_harm_threshold': 2}),
        Ancestry("Faeries", {'prowess': 1}, ["Extra Reality"], {'spiritual_harm_threshold': 2}),
        Ancestry("Framed", {'prowess': 1}, ["Death Avoidance"], {'physical_harm_threshold': 2}),
        Ancestry("Halflings", {'prowess': 1}, ["Hospitality"], {'physical_harm': 1, 'mental_harm': 1, 'spiritual_harm': -1}),
        Ancestry("Humans", {'might': 1}, ["Warrant Expertise"], {'mental_harm': 1}),
        Ancestry("Orcs", {'might': 1}, ["Mighty Last Breath"], {'physical_harm': 2, 'mental_harm': -1}),
        Ancestry("Tieflings", {'prowess': 1}, ["Enhanced Recovery"], {'spiritual_harm': 1})
    ]

    professions = [
        Profession("Academic", ["Research Boon"]),
        Profession("Common", ["Extra Bond"]),
        Profession("Criminal", ["Warrant Boon"]),
        Profession("Martial", {'physical_wound_threshold': 1}),
        Profession("Religious", {'spirit_wound_threshold': 1}),
        Profession("Wilderness", ["Journey Boon"])
    ]

    communities = [
        Community("Desertborne", ["Heat Resilience"]),
        Community("Groveborne", ["Forest Expertise"]),
        Community("Highborne", ["Noble Parley"]),
        Community("Loreborne", ["Lore Expertise"]),
        Community("Orderborne", ["Order Defiance"]),
        Community("Ridgeborne", {'armor': 1}),
        Community("Skyborne", ["Ally Recovery"]),
        Community("Seaborne", ["Sea Resilience"]),
        Community("Slyborne", ["Criminal Insight"]),
        Community("Underborne", ["Darkness Defense"]),
        Community("Wanderborne", ["Nomad Camp"]),
        Community("Wildborne", ["Wild Stealth"])
    ]

    paths = [
        Path("Mage", {'mental_harm': 1}, ["Magic Potential", "Channeled Through Me", "Sphere Touched"], ["Channel", "Manifest", "Spell Defense"], {'physical_damage_die': '1d6'}),
        Path("Priest", {'spiritual_harm': 1}, ["Devotion", "Devotion's Weapon"], ["Pray", "Orison", "Petition"], {'physical_damage_die': '1d6'}),
        Path("Rogue", {'physical_harm_threshold': 1}, ["Trickery", "Hidden Knife"], ["Tricks of the Trade", "Sneak Attack"], {'physical_damage_die': '1d6'}),
        Path("Warrior", {'physical_harm': 2}, ["Fighting Style"], ["Reckless Attack", "My Life for Yours"], {'physical_damage_die': '1d6'}) 
    ]

    return ancestries, professions, communities, paths

def interactive_selection(options, type_name):
    """
    Allows the user to interactively select an option from a list, displaying details for each choice based on the component type.
    """
    print(f"\nSelect a {type_name}:")
    for idx, option in enumerate(options, 1):
        if isinstance(option, Ancestry):
            details = f"Attribute Modifiers: {option.attribute_modifiers}, Special Ability: {option.special_ability}, Health Modifier: {option.health_modifier}"
        elif isinstance(option, Profession):
            details = f"Ability: {option.ability}"
        elif isinstance(option, Community):
            if isinstance(option.ability_or_modifier, dict):  # Check if it's a dictionary (attribute modifier)
                # Create a human-readable string from the dictionary
                mod_details = ", ".join([f"{k} +{v}" for k, v in option.ability_or_modifier.items()])
                details = f"Attribute Modifiers: {mod_details}"
            else:
                details = f"Ability: {option.ability_or_modifier}"
        elif isinstance(option, Path):
            details = f"Health Modifier: {option.health_modifier}, Path Passives: {option.path_passives}, Path Moves: {option.path_moves}, Damage Die: {option.damage_die}"
        print(f"{idx}. {option.name} ({details})")
    
    choice = int(input("Enter your choice (number): ")) - 1
    return options[choice]

def update_character_creation_with_details():
    """
    Fully updated character creation function incorporating all detailed options with interactive selections.
    """
    # Define all detailed options
    ancestries, professions, communities, paths = define_detailed_options()

    # Basic character info
    print("Welcome to the Character Creation Wizard!")
    name = input("Enter your character's name: ")
    age = int(input("Enter your character's age: "))

    # Interactive selections for detailed components
    print("\n--- Ancestry Selection ---")
    ancestry = interactive_selection(ancestries, "ancestry")
    print("\n--- Profession Selection ---")
    profession = interactive_selection(professions, "profession")
    print("\n--- Community Selection ---")
    community = interactive_selection(communities, "community")
    print("\n--- Path Selection ---")
    path = interactive_selection(paths, "path")

    # Initialize character with selected components
    level = 1  # Starting level for all characters
    new_character = Character(name, age, ancestry, profession, community, path, level)

    # Allow user to choose initial attributes
    print("\nInitial attribute values:")
    for attr, value in new_character.attributes.basic_attributes.items():
        print(f"{attr.capitalize()}: {value}")
    
    print("\nYou can increase two of the three basic attributes (Prowess, Might, Presence) by 1.")
    first_choice = input("Choose the first attribute to increase: ").lower()
    second_choice = input("Choose the second attribute to increase: ").lower()
    
    # Apply initial choices
    if first_choice in new_character.attributes.basic_attributes:
        new_character.attributes.basic_attributes[first_choice] += 1
    if second_choice in new_character.attributes.basic_attributes:
        new_character.attributes.basic_attributes[second_choice] += 1
    
    # Final review of the created character
    print_character_details(new_character)

    return new_character 

class EnhancedAttributes:
    def __init__(self, prowess=0, might=0, presence=0, power=0, armor_uses=1):
        self.basic_attributes = {'prowess': prowess, 'might': might, 'presence': presence}
        self.special_attributes = {'power': power, 'armor_uses': armor_uses}
        self.harm_tracks = {'physical': [4, 4], 'mental': [4, 4], 'spiritual': [3, 3]}
        self.wound_thresholds = {'minor': 5, 'major': 7, 'severe': 9}
        self.damage_dice = {'physical': '1d4', 'mental': '1d4', 'spiritual': '1d4'}
        self.resources = {
            'mana': {'current': 0, 'max': 10},
            'mercy': {'current': 0, 'max': 10},
            'wrath': {'current': 0, 'max': 10},
            'trickery_dice': {'current': 0, 'max': 5}
        }

    def update_resource(self, resource_name, amount, is_current=True):
        resource = self.resources.get(resource_name)
        if resource:
            key = 'current' if is_current else 'max'
            resource[key] = max(0, min(resource[key] + amount, resource['max'] if is_current else float('inf')))
            self.resources[resource_name] = resource

def enhanced_character_to_dict(new_character):
    """Converts an EnhancedCharacter object into a dictionary for JSON serialization, including all resources."""
    char_dict = {
        "personal_details": new_character.personal_details,  # Corrected to pass the entire dictionary
        "attributes": {
            "basic_attributes": new_character.attributes.basic_attributes,
            "special_attributes": new_character.attributes.special_attributes,
            "harm_tracks": new_character.attributes.harm_tracks,
            "wound_thresholds": new_character.attributes.wound_thresholds,
            "damage_dice": new_character.attributes.damage_dice,
            "resources": new_character.attributes.resources
        },
        "path": {
            "name": new_character.path.name,
            "additional_effects": new_character.path.additional_effects
        }
    }
    return char_dict

def enhanced_save_character(new_character, filename="Character.json"):
    """Saves an EnhancedCharacter object to a JSON file."""
    char_dict = enhanced_character_to_dict(new_character)
    with open(filename, 'w') as file:
        json.dump(char_dict, file, indent=4)

def enhanced_load_character(filename="enhanced_character.json"):


    """Loads an EnhancedCharacter object from a JSON file."""
    with open(filename, 'r') as file:
        char_dict = json.load(file)
    
    # Properly instantiate the character object using placeholders where needed
    character = Character(
        name=char_dict["personal_details"]["name"],
        age=char_dict["personal_details"]["age"],
        ancestry=Ancestry(name=""),  # Placeholder
        profession=Profession(name=""),
        community=Community(name=""),
        path=Path(name=char_dict["path"]["name"], health_modifier={}, path_passives=[], path_moves=[], damage_die="1d4"),  # Assume placeholder values
        level=1  # Assume level 1 for simplification
    )
    return character

def save_character(new_character):
    try:
        safe_name = re.sub(r'[^\w\-_\. ]', '_', new_character.personal_details['name'])
        filename = f"{safe_name}_Character.json"
        char_dict = new_character.to_dict()
        with open(filename, 'w') as file:
            json.dump(char_dict, file, indent=4)
        print(f"Character saved successfully to {filename}")
    except Exception as e:
        print(f"Failed to save character: {str(e)}")

def load_character(filename):
    try:
        with open(filename, 'r') as file:
            char_dict = json.load(file)
        loaded_character = Character.from_dict(char_dict)  # Assuming a method exists to recreate a Character from dict
        print("Character loaded successfully.")
        print_character_details(loaded_character)
        return loaded_character
    except FileNotFoundError:
        print("Character file not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Start :) 
main_menu()  