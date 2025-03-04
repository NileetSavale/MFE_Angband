from difflib import get_close_matches

class MonsterEditor:
    def __init__(self, monster_parser, game_data_loader):
        self.monster_parser = monster_parser
        self.game_data_loader = game_data_loader

    def suggest_correction(self, input_value, valid_options):
        """ Suggests the closest valid option if input is invalid """
        suggestion = get_close_matches(input_value, valid_options, n=1, cutoff=0.6)
        return suggestion[0] if suggestion else None

    def validate_integer(self, value, field_name):
        """ Ensures input is a valid integer """
        if not value.isdigit():
            print(f"⚠️ Error: '{value}' is not a valid number for {field_name}. Try again.")
            return None
        return int(value)

    def validate_flags(self, flags):
        """ Ensures only valid flags are accepted """
        valid_flags = self.monster_parser.valid_flags  # ✅ Fetch from MonsterParser
        new_flags = [flag.strip() for flag in flags.split(",") if flag.strip()]
        corrected_flags = []

        for flag in new_flags:
            if flag in valid_flags:
                corrected_flags.append(flag)
            else:
                suggestion = self.suggest_correction(flag, valid_flags)
                if suggestion:
                    confirm = input(f"⚠️ Did you mean '{suggestion}' instead of '{flag}'? (Y/N): ").strip().lower()
                    if confirm == "y":
                        corrected_flags.append(suggestion)
                    else:
                        print(f"⚠️ Warning: '{flag}' is not a recognized flag and will be ignored.")
                else:
                    print(f"⚠️ Warning: '{flag}' is not a recognized flag and will be ignored.")

        return corrected_flags if corrected_flags else None


    def edit_monster(self, name):
        if name not in self.monster_parser.monsters:
            print("❌ Monster not found!")
            return
        
        while True:
            monster = self.monster_parser.monsters[name]
            print(f"\n=== Editing: {name} ===")
            print(f"name: {monster['original_name']}")
            for key, value in monster.items():
                if key != "original_name":
                    if isinstance(value, list):
                        print(f"{key}: {', '.join(value)}")
                    else:
                        print(f"{key}: {value}")

            key = input("\nEnter attribute to edit (or type 'done' to finish, 'list' to view valid values): ").strip()
            if key.lower() == "done":
                break
            if key.lower() == "list":
                self.game_data_loader.list_available_options()
                continue

            # ✅ Allow renaming of monster
            if key == "name":
                new_name = input(f"Enter new monster name (Current: '{name}', press Enter to keep): ").strip()

                if new_name == "":
                    print(f"🔄 Keeping old name: {name}")
                elif new_name in self.monster_parser.monsters:
                    print(f"❌ Error: A monster with name '{new_name}' already exists!")
                else:
                    success = self.monster_parser.rename_monster(name, new_name)
                    if success:
                        print(f"✅ Monster name changed to '{new_name}'!")
                        name = new_name  # ✅ Update reference for further editing
                        monster = self.monster_parser.monsters[name]  # ✅ Update monster reference
                continue  # ✅ Ensures the loop continues instead of stopping

            if key not in monster:
                print(f"❌ Invalid attribute '{key}'! Try again.")
                continue  

            old_value_str = str(monster[key])


            # ✅ Handle numerical inputs properly
            if key in ["speed", "hit-points", "depth", "rarity", "experience", "armor-class"]:
                new_value = input(f"Enter new value for {key} (Current: '{old_value_str}', press Enter to keep): ").strip()
                if new_value == "":
                    print(f"🔄 Keeping old value: {old_value_str}")
                    continue
                validated_value = self.validate_integer(new_value, key)
                if validated_value is not None:
                    monster[key] = validated_value
                    print(f"✅ Updated '{key}': {monster[key]}")
                continue

            # ✅ Handle `flags` with validation
            if key == "flags":
                print(f"\n📌 Editing flags (Current: {', '.join(monster[key])})")
                new_flags_input = input("Enter new flags (comma-separated, press Enter to keep current): ").strip()

                if not new_flags_input:
                    print(f"🔄 Keeping old flags: {', '.join(monster[key])}")
                    continue

                validated_flags = self.validate_flags(new_flags_input)
                if validated_flags is not None:
                    monster[key] = validated_flags
                    print(f"✅ Updated '{key}': {', '.join(monster[key])}")
                else:
                    print(f"❌ No valid flags entered. Keeping old flags: {', '.join(monster[key])}")
                continue
            
            # ✅ Handle `desc` editing correctly
            if key == "desc":
                print(f"\n📌 Editing description (Current: '{old_value_str}')")
                new_desc = input("Enter new description (press Enter to keep current): ").strip()
                if new_desc == "":
                    print(f"🔄 Keeping old description: {old_value_str}")
                else:
                    monster[key] = new_desc
                    print(f"✅ Updated description: {monster[key]}")
                continue
            # ✅ Handle `blow` editing with validation
            if key == "blow":
                if key not in monster:
                    print("⚠️ This monster does not have any blows!")
                    continue

                blows = monster[key] if isinstance(monster[key], list) else [monster[key]]

                while True:
                    print(f"\n📌 Editing blows (Current: {', '.join(blows)})")

                    print("\nOptions for editing blows:")
                    print("1. Edit an existing blow")
                    print("2. Add a new blow (Max: 4)")
                    print("3. Remove a blow")
                    print("4. Exit blow editing")

                    choice = input("Enter choice (1-4): ").strip()

                    if choice == "1":
                        print("\nSelect the blow to edit:")
                        for i, blow in enumerate(blows, 1):
                            print(f"{i}. {blow}")

                        index = input("Enter blow number to edit: ").strip()
                        if not index.isdigit() or int(index) < 1 or int(index) > len(blows):
                            print("⚠️ Invalid selection!")
                            continue

                        index = int(index) - 1
                        parts = blows[index].split(":")
                        method = parts[0] if len(parts) > 0 else "NONE"
                        effect = parts[1] if len(parts) > 1 else "NONE"
                        power = parts[2] if len(parts) > 2 else "1d1"

                        # ✅ Validate `blow_methods`
                        new_method = input(f"Enter new method (Current: '{method}', press Enter to keep): ").strip() or method
                        if new_method not in self.game_data_loader.blow_methods:
                            print("⚠️ Invalid blow method.")
                            continue

                        # ✅ Validate `blow_effects`
                        new_effect = input(f"Enter new effect (Current: '{effect}', press Enter to keep): ").strip() or effect
                        if new_effect not in self.game_data_loader.blow_effects:
                            print("⚠️ Invalid blow effect.")
                            continue

                        new_power = input(f"Enter new power (Current: '{power}', press Enter to keep): ").strip() or power
                        blows[index] = f"{new_method}:{new_effect}:{new_power}" 
                        print(f"✅ Updated blow: {blows[index]}")
                    elif choice == "2":
                        if len(blows) >= 4:
                            print("⚠️ You cannot add more than 4 blows.")
                            continue

                        new_method = input("Enter new blow method: ").strip()
                        if new_method not in self.game_data_loader.blow_methods:
                            suggestion = self.suggest_correction(new_method, self.game_data_loader.blow_methods)
                            if suggestion:
                                confirm = input(f"Did you mean '{suggestion}'? (Y/N): ").strip().lower()
                                if confirm == "y":
                                    new_method = suggestion
                            else:
                                print("⚠️ Invalid method, please enter a valid blow method.")
                                continue

                        new_effect = input("Enter new blow effect: ").strip()
                        if new_effect not in self.game_data_loader.blow_effects:
                            suggestion = self.suggest_correction(new_effect, self.game_data_loader.blow_effects)
                            if suggestion:
                                confirm = input(f"Did you mean '{suggestion}'? (Y/N): ").strip().lower()
                                if confirm == "y":
                                    new_effect = suggestion
                            else:
                                print("⚠️ Invalid effect, please enter a valid blow effect.")
                                continue

                        new_power = input("Enter new blow power: ").strip()
                        blows.append(f"{new_method}:{new_effect}:{new_power}")
                        print(f"✅ Added new blow: {new_method}:{new_effect}:{new_power}")

                    elif choice == "3":
                        if not blows:
                            print("⚠️ No blows to remove.")
                            continue

                        print("\nSelect the blow to remove:")
                        for i, blow in enumerate(blows, 1):
                            print(f"{i}. {blow}")

                        index = input("Enter blow number to remove: ").strip()
                        if not index.isdigit() or int(index) < 1 or int(index) > len(blows):
                            print("⚠️ Invalid selection!")
                            continue

                        removed_blow = blows.pop(int(index) - 1)
                        print(f"✅ Removed blow: {removed_blow}")
                    elif choice == "4":
                        print("🔄 Exiting blow editing.")
                        break

                monster[key] = blows
                print(f"✅ Updated '{key}': {', '.join(monster[key])}")

        self.monster_parser.monsters[name] = monster  
        print(f"\n✅ {name} successfully updated!")
