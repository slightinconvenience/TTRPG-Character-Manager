# options for character selction 

# imports from standard libraries
import json 
import sqlite3
import os 

# imports from custom libraries

# ancestry options 
def ancestry_options(): 
    ancestries = ["Drow", "Dwarves", "Elves", "Faries", "Framed", "Halflings", "Humans", "Orcs", "Tieflings"]
    for index, name in enumerate(ancestries, 1):
        print(f"{index}. {name}")

    choice = int(input("Select an ancestry by enter its number: "))
    if 1 <= choice <= len(ancestries):
        selected_ancestry = ancestries[choice - 1]
        print(selected_ancestry)
        return selected_ancestry
    else:
        print("Invalid selection. Please choose a number between 1 and {}.".format(len(ancestries)))

# profession options
def profession_options():
    professions = ["Academic", "Common", "Criminal", "Martial", "Religious", "Wilderness"]
    for index, name in enumerate(professions, 1):
        print(f"{index}. {name}")

    choice = int(input("Select a profession by entering its number: "))
    if 1 <= choice <= len(professions):
        selected_profession = professions[choice - 1]
        print(selected_profession)
        return selected_profession
    else:
        print("Invalid selection. Please choose a number between 1 and {}.".format(len(professions)))

# community options 
def community_options():
    communities = ['Desertborne', 'Groveborne', 'Highborne', 'Loreborne', 'Orderborne', 'Ridgeborne', 'Skyborne', 'Seaborne', 'Slyborne', 'Underborne', 'Wanderborne', 'Wildborne']
    for index, name in enumerate(communities, 1):
        print(f"{index}. {name}")
    
    choice = int(input("Select a community by entering its number: "))
    if 1 <= choice <= len(communities):
        selected_community = communities[choice - 1]
        print(selected_community)
        return selected_community
    else:
        print("Invalid selection. Please choose a number between 1 and {}.".format(len(communities)))

# path options 
def path_options():
    paths = ["Mage", "Priest", "Rogue", "Warrior"]
    for index, name in enumerate(paths, 1):
        print(f"{index}. {name}")

    choice = int(input("Select a path by entering its number: "))
    if 1 <= choice <= len(paths):
        selected_path = paths[choice - 1]
        print(selected_path)
        return selected_path
    else:
        print("Invalid selection. Please choose a number between 1 and {}.".format(len(paths)))

#ancestry_options() 
#profession_options()
#community_options()
#path_options()


