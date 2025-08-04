import json
from pathlib import Path


def extract_credentials():
    path  = Path (r"F:\Python\CyberSce_Project\cred collector\ex\data.json")
    try:
        with open(path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print("data.json not found!")
        return
    except json.JSONDecodeError:
        print("Invalid JSON in data.json!")
        return

    with open('cred.txt', 'w') as cred_file:
        cred_file.write("Captured Credentials\n")
        cred_file.write("=" * 50 + "\n\n")
        
        for entry in data:
            if 'formData' in entry:
                cred_file.write(f"URL: {entry['url']}\n")
                cred_file.write(f"Timestamp: {entry['timestamp']}\n")
                for key, value in entry['formData'].items():
                    cred_file.write(f"{key.capitalize()}: {value}\n")
                cred_file.write("-" * 50 + "\n")

if __name__ == "__main__":
    extract_credentials()