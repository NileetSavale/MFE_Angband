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
            print("❌ Monster not found!")
            return

        monster = self.monster_parser.monsters[name]
        print(f"\n=== Editing: {name} ===")

        # Display attributes correctly
        for key, value in monster.items():
            if isinstance(value, list):
                print(f"{key}: {', '.join(value)}")
            else:
                print(f"{key}: {value}")

        while True:
            key = input("\nEnter attribute to edit (or type 'done' to finish, 'list' to view valid values): ").strip()
            if key.lower() == "done":
                break
            if key.lower() == "list":
                self.game_data_loader.list_available_options()
                continue
            if key not in self.monster_parser.original_attributes[name]:  # Only allow editing existing attributes
                print(f"❌ Invalid attribute '{key}'! You can only edit existing attributes.")
                continue  

            new_value = input(f"Enter new value for {key}: ").strip()
            if not new_value:
                print("⚠️ Error: Value cannot be empty. Try again.")
                continue

            # Handle multiple values correctly (blows, flags)
            if isinstance(monster[key], list):
                new_values = new_value.split(", ")

                corrected_values = []
                for val in new_values:
                    if key == "blows" and val not in self.game_data_loader.blow_methods:
                        suggestion = self.suggest_correction(val, self.game_data_loader.blow_methods)
                        if suggestion:
                            confirm = input(f"Did you mean '{suggestion}' instead of '{val}'? (Y/N): ").strip().lower()
                            if confirm == "y":
                                corrected_values.append(suggestion)
                            else:
                                print(f"⚠️ Warning: '{val}' is not valid and will be ignored.")
                        else:
                            print(f"⚠️ Warning: '{val}' is not a recognized blow method and will be ignored.")
                    elif key == "flags" and val not in self.game_data_loader.valid_flags:
                        suggestion = self.suggest_correction(val, self.game_data_loader.valid_flags)
                        if suggestion:
                            confirm = input(f"Did you mean '{suggestion}' instead of '{val}'? (Y/N): ").strip().lower()
                            if confirm == "y":
                                corrected_values.append(suggestion)
                            else:
                                print(f"⚠️ Warning: '{val}' is not valid and will be ignored.")
                        else:
                            print(f"⚠️ Warning: '{val}' is not a recognized flag and will be ignored.")
                    else:
                        corrected_values.append(val)

                if corrected_values:
                    monster[key] = corrected_values
                    print(f"✅ Updated '{key}': {monster[key]}")

            # Single-value attribute updates
            else:
                monster[key] = new_value
                print(f"✅ Updated '{key}': {monster[key]}")

        print(f"\n✅ {name} successfully updated!")
