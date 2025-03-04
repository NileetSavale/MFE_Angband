import shutil
import logging

logging.basicConfig(filename="logs/mfe_changes.log", level=logging.INFO, format="%(asctime)s - %(message)s")

class MonsterParser:
    def __init__(self, filepath):
        self.filepath = filepath
        self.monsters = self.load_monsters()
        self.original_attributes = {name: set(attrs.keys()) for name, attrs in self.monsters.items()}  # ✅ Track original attributes

    def backup_file(self):
        """ Creates a backup of the existing monster.txt before modifying it. """
        backup_path = self.filepath + ".backup"
        shutil.copy(self.filepath, backup_path)
        print(f"✅ Backup created: {backup_path}")

    def load_monsters(self):
        """ Reads monster.txt and parses monsters into a dictionary while handling duplicate attributes. """
        monsters = {}
        current_monster = None

        with open(self.filepath, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if line.startswith("name:"):
                    current_monster = line.split(":", 1)[1].strip()
                    monsters[current_monster] = {"original_name": current_monster}

                elif current_monster:
                    if ":" in line:
                        key, value = line.split(":", 1)
                        key = key.strip()
                        value = value.strip()

                        if key in monsters[current_monster]:
                            if isinstance(monsters[current_monster][key], list):
                                monsters[current_monster][key].append(value)
                            else:
                                monsters[current_monster][key] = [monsters[current_monster][key], value]
                        else:
                            monsters[current_monster][key] = value
                    else:
                        print(f"⚠️ Warning: Skipping malformed line -> {line}")

        return monsters

    def rename_monster(self, old_name, new_name):
        """ Handles renaming a monster while updating all references in `friends`. """
        if new_name in self.monsters:
            print(f"⚠️ Error: A monster named '{new_name}' already exists. Choose another name.")
            return False

        if old_name not in self.monsters:
            print(f"❌ Error: Monster '{old_name}' not found.")
            return False

        self.monsters[new_name] = self.monsters.pop(old_name)
        self.monsters[new_name]["original_name"] = new_name  
        
        # ✅ Ensure the `original_attributes` updates correctly
        if old_name in self.original_attributes:
            self.original_attributes[new_name] = self.original_attributes.pop(old_name)

        self.update_friends_references(old_name, new_name)

        print(f"✅ Monster '{old_name}' successfully renamed to '{new_name}'!")
        return True

    def update_friends_references(self, old_name, new_name):
        """ Updates all references of `old_name` in `friends` attributes of other monsters. """
        print(f"\n🔍 Scanning for references to '{old_name}' in other monsters...")
        for monster in self.monsters.values():
            if "friends" in monster:
                updated_friends = []
                for friend in monster["friends"]:
                    parts = friend.split(":")
                    if parts[-1] == old_name:  # ✅ Only update if the name was actually changed
                        parts[-1] = new_name
                        print(f"🔄 Updating friend reference: {friend} → {':'.join(parts)}")
                    updated_friends.append(":".join(parts))
                monster["friends"] = updated_friends  # ✅ Save updated friend list

    def save_monsters(self):
        """ Saves the modified monsters back to the file. """
        self.backup_file()

        with open(self.filepath, "w", encoding="utf-8") as file:
            for name, attributes in self.monsters.items():
                file.write(f"name:{name}\n")

                for key, value in attributes.items():
                    if key != "original_name":
                        if isinstance(value, list):
                            for item in value:
                                file.write(f"{key}:{item}\n")
                        else:
                            file.write(f"{key}:{value}\n")

                file.write("\n")

        logging.info(f"✅ Changes saved to {self.filepath}")
        print(f"\n✅ Changes saved to {self.filepath}, and logged in logs/mfe_changes.log")
