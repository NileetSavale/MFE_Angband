from difflib import get_close_matches

class MonsterEditor:
    def __init__(self, monster_parser, game_data_loader):
        self.monster_parser = monster_parser
        self.game_data_loader = game_data_loader

    def suggest_correction(self, input_value, valid_options):
        """ Suggests the closest valid option if input is invalid """
        suggestion = get_close_matches(input_value, valid_options, n=1, cutoff=0.6)
        return suggestion[0] if suggestion else None

    def edit_monster(self, name):
        if name not in self.monster_parser.monsters:
            print("Monster not found!")
            return

        monster = self.monster_parser.monsters[name]
        print(f"\n=== Editing: {name} ===")
        for key, value in monster.items():
            print(f"{key}: {value}")

        while True:
            key = input("\nEnter attribute to edit (or type 'done' to finish, 'list' to view valid values): ").strip()
            if key.lower() == "done":
                break
            if key.lower() == "list":
                self.game_data_loader.list_available_options()
                continue
            if key not in monster:
                print("Invalid attribute! Try again.")
                continue

            new_value = input(f"Enter new value for {key}: ").strip()
            if not new_value:
                print("Error: Value cannot be empty. Try again.")
                continue

            # Handling blow methods with auto-correction
            if key == "blows":
                new_blow_methods = new_value.split(", ")
                corrected_methods = []
                
                for method in new_blow_methods:
                    if method not in self.game_data_loader.blow_methods:
                        suggestion = self.suggest_correction(method, self.game_data_loader.blow_methods)
                        if suggestion:
                            confirm = input(f"Did you mean '{suggestion}' instead of '{method}'? (Y/N): ").strip().lower()
                            if confirm == "y":
                                corrected_methods.append(suggestion)
                            else:
                                print(f"Warning: '{method}' is not valid and will be ignored.")
                        else:
                            print(f"Warning: '{method}' is not a recognized blow method and will be ignored.")
                    else:
                        corrected_methods.append(method)

                if corrected_methods:
                    monster[key] = corrected_methods
                    print(f"Updated '{key}': {monster[key]}")

            # Handling flags with auto-correction
            elif key == "flags":
                new_flags = new_value.split(", ")
                corrected_flags = []

                for flag in new_flags:
                    if flag not in self.game_data_loader.valid_flags:
                        suggestion = self.suggest_correction(flag, self.game_data_loader.valid_flags)
                        if suggestion:
                            confirm = input(f"Did you mean '{suggestion}' instead of '{flag}'? (Y/N): ").strip().lower()
                            if confirm == "y":
                                corrected_flags.append(suggestion)
                            else:
                                print(f"Warning: '{flag}' is not valid and will be ignored.")
                        else:
                            print(f"Warning: '{flag}' is not a recognized flag and will be ignored.")
                    else:
                        corrected_flags.append(flag)

                if corrected_flags:
                    monster[key] = corrected_flags
                    print(f"Updated '{key}': {monster[key]}")

            # Generic attribute updates
            else:
                monster[key] = new_value
                print(f"Updated '{key}': {monster[key]}")

        print(f"\n✅ {name} successfully updated!")
