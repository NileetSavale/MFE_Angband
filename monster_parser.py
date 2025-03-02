import shutil
import logging

logging.basicConfig(filename="logs/mfe_changes.log", level=logging.INFO, format="%(asctime)s - %(message)s")

class MonsterParser:
    def __init__(self, filepath):
        self.filepath = filepath
        self.monsters = self.load_monsters()

    def backup_file(self):
        """ Creates a backup of the existing monster.txt before modifying it. """
        backup_path = self.filepath + ".backup"
        shutil.copy(self.filepath, backup_path)
        print(f"✅ Backup created: {backup_path}")

    def load_monsters(self):
        """ Reads monster.txt and parses monsters into a dictionary while handling duplicate attributes. """
        monsters = {}
        current_monster = None
        original_attributes = {}  # Keep track of attributes per monster

        with open(self.filepath, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                # Skip empty lines and comments
                if not line or line.startswith("#"):
                    continue

                # Detect new monster entry
                if line.startswith("name:"):
                    current_monster = line.split(":", 1)[1].strip()
                    monsters[current_monster] = {}
                    original_attributes[current_monster] = set()  # Track what was present

                elif current_monster:
                    if ":" in line:
                        key, value = line.split(":", 1)
                        key = key.strip()
                        value = value.strip()

                        # Track that this attribute was originally in the file
                        original_attributes[current_monster].add(key)

                        # If the key already exists, store values as a list
                        if key in monsters[current_monster]:
                            if isinstance(monsters[current_monster][key], list):
                                monsters[current_monster][key].append(value)
                            else:
                                monsters[current_monster][key] = [monsters[current_monster][key], value]
                        else:
                            monsters[current_monster][key] = value
                    else:
                        print(f"⚠️ Warning: Skipping malformed line -> {line}")

        # Store original attribute presence for validation in the editor
        self.original_attributes = original_attributes
        return monsters

    def save_monsters(self):
        """ Saves modified monsters back to monster.txt while preserving original format. """
        self.backup_file()

        with open(self.filepath, "w", encoding="utf-8") as file:
            for name, attributes in self.monsters.items():
                file.write(f"name:{name}\n")
                for key, value in attributes.items():
                    if key in self.original_attributes.get(name, []):  # Only write original attributes
                        if isinstance(value, list):
                            for item in value:
                                file.write(f"{key}:{item}\n")
                        else:
                            file.write(f"{key}:{value}\n")
                file.write("\n")  # Separate monsters

        logging.info(f"✅ Changes saved to {self.filepath}")
        print(f"\n✅ Changes saved to {self.filepath}, and logged in logs/mfe_changes.log")
