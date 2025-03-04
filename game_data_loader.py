import os

class GameDataLoader:
    def __init__(self, game_data_path):
        self.game_data_path = game_data_path

        # ✅ Load flags from multiple sources
        self.valid_flags = self._load_flags_from_multiple_files([
            "object_property.txt",
            "object.txt",
            "object_base.txt"
        ])

        # ✅ Load blow data
        self.blow_methods = self._load_data("blow_methods.txt")
        self.blow_effects = self._load_data("blow_effects.txt")

        # ✅ Print loaded data for debugging
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

    def _load_flags_from_multiple_files(self, filenames):
        """ Extracts flag-like attributes from multiple files. """
        flags = set()  # Use a set to avoid duplicates

        for filename in filenames:
            path = os.path.join(self.game_data_path, filename)
            print(f"Checking file: {path}")  # Debugging output

            if not os.path.exists(path):
                print(f"⚠️ Warning: {filename} not found! Skipping.")
                continue

            try:
                with open(path, "r", encoding="utf-8") as file:
                    for line in file:
                        line = line.strip()

                        # ✅ Extract flags from "code:" lines
                        if line.startswith("code:"):
                            flag_name = line.split(":", 1)[1].strip()
                            flags.add(flag_name)

                        # ✅ Extract flags from general key-value pairs
                        elif ":" in line:
                            key, value = line.split(":", 1)
                            key = key.strip().lower()
                            value = value.strip()

                            # ✅ Consider only relevant keys
                            if key in ["flags", "flag"]:
                                for flag in value.split("|"):
                                    flags.add(flag.strip())

            except Exception as e:
                print(f"❌ Error reading {filename}: {e}")

        return sorted(flags)  # Convert back to sorted list for consistency
