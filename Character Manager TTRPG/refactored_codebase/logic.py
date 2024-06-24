# holds the logic for the progam. 
# includes functions for initilizing the program, choosing the options inside, as well as running character generation and the save methods

# imports from standard libraries 
import json 
import sqlite3
import os 

# imports from custom libraries 

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

