import json

SETTINGS_PATH = "config/settings.json"

def load_settings():
    with open(SETTINGS_PATH, "r") as f:
        return json.load(f)
    
def save_settings(data):
    with open(SETTINGS_PATH, "w") as f:
        json.dump(data, f, indent=2)