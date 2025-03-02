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
        original_name = monster["original_name"]  # ✅ Keep track of the original name
        print(f"\n=== Editing: {name} ===")

        # ✅ Display current values before editing
        print(f"name: {monster['original_name']}")  
        for key, value in monster.items():
            if key != "original_name":  
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

            # ✅ Fix renaming process
            if key.lower() == "name":  
                new_name = input(f"Enter new name for {monster['original_name']} (Press Enter to keep '{monster['original_name']}'): ").strip()
                if not new_name:  
                    print(f"🔄 Keeping old name: {monster['original_name']}")
                    continue

                if new_name not in self.monster_parser.monsters:
                    # ✅ Move attributes to new name instead of creating an empty entry
                    self.monster_parser.monsters[new_name] = monster.copy()
                    self.monster_parser.monsters[new_name]["original_name"] = new_name  

                    # ✅ Ensure `original_attributes` is updated
                    if name in self.monster_parser.original_attributes:
                        self.monster_parser.original_attributes[new_name] = self.monster_parser.original_attributes.pop(name)

                    # ✅ Remove old name from dictionary after transferring data
                    del self.monster_parser.monsters[name]

                    name = new_name  
                    print(f"✅ Monster renamed to '{new_name}' and attributes retained!")
                else:
                    print("⚠️ Error: Name cannot be empty or duplicate. Try again.")
                continue

            if key not in monster:
                print(f"❌ Invalid attribute '{key}'! You can only edit existing attributes.")
                continue  

            # ✅ Special handling for `blow`
            if key.lower() == "blow":
                old_blow = monster[key]
                print(f"\n📌 Editing blows (Current: {', '.join(old_blow)})")
                new_blows = []
                for attack in old_blow:  
                    method, effect = attack.split(":") if ":" in attack else (attack, "NONE")
                    print(f"\nEditing attack: {method}:{effect}")
                    new_method = input(f"Enter new attack method (Current: '{method}', press Enter to keep): ").strip() or method
                    new_effect = input(f"Enter new attack effect (Current: '{effect}', press Enter to keep): ").strip() or effect
                    new_blows.append(f"{new_method}:{new_effect}")

                # ✅ Confirm and save changes
                monster[key] = new_blows
                print(f"✅ Updated '{key}': {', '.join(monster[key])}")

            else:
                # ✅ Show current value before allowing edits
                old_value = monster[key]
                if isinstance(old_value, list):
                    old_value_str = ", ".join(old_value)  
                else:
                    old_value_str = str(old_value)

                new_value = input(f"Enter new value for {key} (Current: '{old_value_str}', press Enter to keep): ").strip()

                if new_value == "":
                    print(f"🔄 Keeping old value: {old_value_str}")  
                    continue

                # ✅ Handle multi-value attributes
                if isinstance(monster[key], list):
                    new_values = new_value.split(", ")
                    monster[key] = new_values  
                    print(f"✅ Updated '{key}': {', '.join(monster[key])}")

                else:
                    monster[key] = new_value  
                    print(f"✅ Updated '{key}': {monster[key]}")

        # ✅ Ensure renamed monsters keep attributes
        self.monster_parser.monsters[name] = monster  

        print(f"\n✅ {name} successfully updated!")
