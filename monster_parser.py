import shutil
import logging

logging.basicConfig(filename="logs/mfe_changes.log", level=logging.INFO, format="%(asctime)s - %(message)s")

class MonsterParser:
    def __init__(self, filepath):
        self.filepath = filepath
        self.monsters = self.load_monsters()
        self.original_attributes = {}  # ✅ Ensure this is defined here

    def backup_file(self):
        """ Creates a backup of the existing monster.txt before modifying it. """
        backup_path = self.filepath + ".backup"
        shutil.copy(self.filepath, backup_path)
        print(f"✅ Backup created: {backup_path}")

    def load_monsters(self):
        """ Reads monster.txt and parses monsters into a dictionary while handling duplicate attributes. """
        monsters = {}
        original_attributes = {}  # ✅ Ensure original attributes are properly tracked
        current_monster = None

        with open(self.filepath, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                # Skip empty lines and comments
                if not line or line.startswith("#"):
                    continue

                # Detect new monster entry
                if line.startswith("name:"):
                    current_monster = line.split(":", 1)[1].strip()
                    monsters[current_monster] = {"original_name": current_monster}  # ✅ Store original name
                    original_attributes[current_monster] = set()  # ✅ Track original attributes

                elif current_monster:
                    if ":" in line:
                        key, value = line.split(":", 1)
                        key = key.strip()
                        value = value.strip()

                        # ✅ Track attribute existence
                        original_attributes[current_monster].add(key)

                        # ✅ Preserve multiple occurrences of attributes like `blows`, `flags`
                        if key in monsters[current_monster]:
                            if isinstance(monsters[current_monster][key], list):
                                monsters[current_monster][key].append(value)
                            else:
                                monsters[current_monster][key] = [monsters[current_monster][key], value]
                        else:
                            monsters[current_monster][key] = value
                    else:
                        print(f"⚠️ Warning: Skipping malformed line -> {line}")

        self.original_attributes = original_attributes  # ✅ Store tracking data globally
        return monsters

    def rename_monster(self, old_name, new_name):
        """ ✅ Handles renaming a monster while preserving attributes. """
        if new_name in self.monsters:
            print(f"⚠️ Error: A monster named '{new_name}' already exists. Choose another name.")
            return False

        if old_name in self.monsters:
            # ✅ Transfer data to the new name
            self.monsters[new_name] = self.monsters.pop(old_name)
            self.monsters[new_name]["original_name"] = new_name  # ✅ Update the stored name
            self.original_attributes[new_name] = self.original_attributes.pop(old_name)  # ✅ Ensure attribute tracking updates

            print(f"✅ Monster '{old_name}' successfully renamed to '{new_name}'!")
            return True
        else:
            print(f"❌ Error: Monster '{old_name}' not found in original attributes.")
            return False

    def save_monsters(self):
        """ ✅ Ensures renamed monsters retain all attributes and writes everything properly. """
        self.backup_file()

        with open(self.filepath, "w", encoding="utf-8") as file:
            for name, attributes in self.monsters.items():
                file.write(f"name:{name}\n")  # ✅ Ensure updated name is used

                for key, value in attributes.items():
                    if key != "original_name":  # ✅ Avoid writing tracking attribute
                        if isinstance(value, list):
                            for item in value:
                                file.write(f"{key}:{item}\n")  # ✅ Write list attributes separately
                        else:
                            file.write(f"{key}:{value}\n")  # ✅ Write single attributes

                file.write("\n")  # ✅ Separate monsters properly

        logging.info(f"✅ Changes saved to {self.filepath}")
        print(f"\n✅ Changes saved to {self.filepath}, and logged in logs/mfe_changes.log")
