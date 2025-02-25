import os

class GameDataLoader:
    def __init__(self, game_data_path):
        self.game_data_path = game_data_path

        # Load flags from object_property.txt
        self.valid_flags = self._load_flags_from_properties("object_property.txt")

        # Load blows from blow_methods.txt and blow_effects.txt
        self.blow_methods = self._load_data("blow_methods.txt")
        self.blow_effects = self._load_data("blow_effects.txt")

        # Print loaded data for debugging
        print("\n=== Loaded Dependencies ===")
        print(f"Blow Methods ({len(self.blow_methods)}): {self.blow_methods}")
        print(f"Blow Effects ({len(self.blow_effects)}): {self.blow_effects}")
        print(f"Valid Flags ({len(self.valid_flags)}): {self.valid_flags}")

    def _load_data(self, filename):
        """ Load simple key-value formatted data from the game files. """
        path = os.path.join(self.game_data_path, filename)

        print(f"Checking file: {path}")  # Debugging output

        if not os.path.exists(path):
            print(f"⚠️ Warning: {filename} not found in {self.game_data_path}!")
            return []

        try:
            with open(path, "r", encoding="utf-8") as file:
                data = []
                for line in file:
                    line = line.strip()

                    # Skip empty lines and comments
                    if not line or line.startswith("#"):
                        continue

                    # Extract valid entries
                    if "name:" in line:
                        parts = line.split(":", 1)
                        if len(parts) == 2:
                            data.append(parts[1].strip())
                        else:
                            print(f"⚠️ Warning: Skipping malformed line in {filename} -> {line}")

                return data

        except Exception as e:
            print(f"❌ Error reading {filename}: {e}")
            return []

    def _load_flags_from_properties(self, filename):
        """ Extracts flag-like attributes from object_property.txt """
        path = os.path.join(self.game_data_path, filename)

        print(f"Checking file: {path}")  # Debugging output

        if not os.path.exists(path):
            print(f"⚠️ Warning: {filename} not found! Using empty flags list.")
            return []

        flags = []
        try:
            with open(path, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()

                    # Extract flag codes
                    if line.startswith("code:"):
                        flag_name = line.split(":", 1)[1].strip()
                        flags.append(flag_name)

        except Exception as e:
            print(f"❌ Error reading {filename}: {e}")
        
        return flags
