from monster_parser import MonsterParser
from editor import MonsterEditor
from game_data_loader import GameDataLoader

class CLI:
    def __init__(self, monster_parser, editor, game_data_loader):
        self.monster_parser = monster_parser
        self.editor = editor
        self.game_data_loader = game_data_loader

    def main_menu(self):
        """ Displays the main menu and handles user input. """
        while True:
            print("\n=== Monster File Editor (MFE) ===")
            print("1. List Monsters")
            print("2. Search Monster")
            print("3. Edit Monster")
            print("4. View Valid Flags & Blows")
            print("5. Save & Exit")
            
            choice = input("Choose an option (1-5): ").strip()

            if choice == "1":
                self.list_monsters()
            elif choice == "2":
                self.search_monster()
            elif choice == "3":
                self.edit_monster()
            elif choice == "4":
                self.view_valid_options()
            elif choice == "5":
                self.save_and_exit()
                break
            else:
                print("Invalid option! Try again.")

    def list_monsters(self):
        """ Lists all monsters available in monster.txt """
        print("\nAvailable Monsters:")
        for name in self.monster_parser.monsters.keys():
            print(f"- {name}")

    def search_monster(self):
        """ Allows searching for a monster by name """
        name = input("\nEnter monster name: ").strip()
        if name in self.monster_parser.monsters:
            print(f"\n{name} found: {self.monster_parser.monsters[name]}")
        else:
            print("Monster not found!")

    def edit_monster(self):
        """ Allows editing of a selected monster """
        name = input("\nEnter monster name to edit: ").strip()
        self.editor.edit_monster(name)

    def view_valid_options(self):
        """ Displays valid flags, blows, and effects """
        self.game_data_loader.list_available_options()

    def save_and_exit(self):
        """ Saves the modified monsters and exits """
        self.monster_parser.save_monsters()
        print("Changes saved successfully!")
