from monster_parser import MonsterParser
from editor import MonsterEditor
from game_data_loader import GameDataLoader

if __name__ == "__main__":
    monster_filepath = input("Enter the full path to your monster.txt file: ").strip()
    game_data_path = input("Enter the path to your game data directory: ").strip()
    
    try:
        parser = MonsterParser(monster_filepath)
        game_data_loader = GameDataLoader(game_data_path)
        editor = MonsterEditor(parser, game_data_loader)
        editor.edit_monster(input("Enter the monster name to edit: ").strip())
        parser.save_monsters()
    except FileNotFoundError:
        print("Error: File not found. Please provide a valid path.")
