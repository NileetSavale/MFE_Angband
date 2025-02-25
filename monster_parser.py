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
        print(f"Backup created: {backup_path}")

    def load_monsters(self):
        """ Reads monster.txt and parses monsters into a dictionary. """
        monsters = {}
        current_monster = None

        with open(self.filepath, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                # Skip empty lines or comment lines
                if not line or line.startswith("#"):
                    continue

                # Detect a new monster by its "name:" field
                if line.startswith("name:"):
                    current_monster = line.split(":", 1)[1].strip()
                    monsters[current_monster] = {"flags": [], "flags_off": []}
                    continue

                # Ensure valid key-value pairs exist before unpacking
                if current_monster and ":" in line:
                    key, value = line.split(":", 1)
                    monsters[current_monster][key.strip()] = value.strip()
                else:
                    print(f"Warning: Skipping malformed line in monster.txt -> {line}")

        return monsters

    def save_monsters(self):
        """ Saves modified monsters back to monster.txt after creating a backup and logging changes. """
        self.backup_file()

        with open(self.filepath, "w", encoding="utf-8") as file:
            for name, attributes in self.monsters.items():
                file.write(f"name:{name}\n")
                for key, value in attributes.items():
                    if isinstance(value, list):
                        file.write(f"{key}:{' | '.join(value)}\n")
                    else:
                        file.write(f"{key}:{value}\n")
                file.write("\n")

        logging.info(f"Changes saved to {self.filepath}")
        print(f"\nChanges saved to {self.filepath}, and logged in logs/mfe_changes.log")
