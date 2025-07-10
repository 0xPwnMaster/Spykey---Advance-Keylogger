import os
import re
import time
from pathlib import Path

import psutil
import cv2
import mss
from PIL import Image

import win32gui
import win32process

import  pywinauto
from pywinauto.findwindows import ElementNotFoundError
from pywinauto.findbestmatch import MatchError


ADDRESS_BAR_TITLES = {
    'brave.exe': "Address and search bar",
    'chrome.exe': 'Address and search bar',
    'firefox.exe': 'Search or enter address',
    'msedge.exe': 'Address and search bar',
    'opera.exe': 'Address bar',
}
login_keywords = [
    'login', 'signin', 'sign-in', 'log-in', 'logon', 'log-on', 'signon', 'sign-on',
    'userlogin', 'usersignin', 'auth', 'authentication', 'authn', 'authin', 'authorize',
    'authorization', 'sso', 'single-sign-on', 'singlesignon', 'oauth', 'oauth2',
    'signup', 'sign-up', 'register', 'registration', 'join', 'createaccount',
    'create-account', 'newaccount', 'enroll', 'membership'
]

def Take_Screenshots(full_file):
    try:
        if not isinstance(full_file, str):
            raise ValueError(f"path must be str")
        if not full_file.lower().endswith(('jpeg', 'jpg')):
            full_file = full_file + ".jpeg"
            
        with mss.mss() as sct:
            if len(sct.monitors) < 2:
                return f"Monitor index error {sct.monitors}"
           
            img = sct.grab(sct.monitors[1])
            pil_img = Image.frombytes("RGB", img.size, img.rgb)     # Why this line 
            pil_img.save(full_file, format="JPEG", quality=50, optimize=True)
        with open(full_file, 'rb') as f:
            header = f.read(2)
            if header != b'\xff\xd8':
                return f"Error: Saved file {full_file} is not a valid JPEG"
        return f"Screenshot saved to {os.path.abspath(full_file)}"
    except mss.ScreenShotError as e:
        return f"Screen capture error: {e}"
    except (FileExistsError, FileNotFoundError, PermissionError) as fe:
        return f"[File Error] {fe}"
    except OSError as os_err:
        return f"[OS Error]: {os_err}"
    except Exception as er:
        return f"An unexpected error occurred: {er}"

def take_snapshot(save_path: Path) -> bool:
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return False
    time.sleep(0.5)
    ret, frame = cap.read()
    cap.release()
    if not ret or frame is None:
        print("Error: Could not capture image.")
        return False

    success = cv2.imwrite(str(save_path), frame)
    if success:
        return True
    else:
        print("Error: Failed to save image.")
        return False

def get_activeApp_Data():
    try:
        hwnd = win32gui.GetForegroundWindow()
        if hwnd == 0:
            return 0, "No active window", "N/A"
        process_title = win32gui.GetWindowText(hwnd)
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        p = psutil.Process(pid)
        process_name = p.name().lower().strip()
        return hwnd, process_title, process_name
    except Exception as e:
        print(f"[ERROR in get_active_app_data]: {e}")
        return 0, "Unknown", f"Error: {e}"

def url_detection(hwnd, process_name):
    if process_name not in ADDRESS_BAR_TITLES:
        return None

    try:
        app = pywinauto.Application(backend='uia').connect(handle=hwnd)
        dlg = app.window(handle=hwnd)
        bar_title = ADDRESS_BAR_TITLES[process_name]
        address_bar = dlg.child_window(title=bar_title, control_type="Edit")
        url = address_bar.get_value()
        return url
    except (ElementNotFoundError, MatchError) as e:
        print(f"[ERROR locating address bar]: {e}")
    except Exception as e:
        print(f"[Unexpected ERROR in url_detection]: {e}")
    return None

def login_detection(url):
    pattern = r'\b(?:' + '|'.join([re.escape(kw) for kw in login_keywords]) + r')\b'
    result = re.search(pattern, url, re.IGNORECASE)
    if result:
        print(f"[!] Potential login page detected: {url}")
    else:
        print(f"[+] No login keyword detected in URL: {url}")

def main():
    browser_names = list(ADDRESS_BAR_TITLES.keys())
    hwnd, title, process = get_activeApp_Data()

    if process in browser_names:
        url = url_detection(hwnd, process)
        print(f"\n\nProcess: {process}")
        if url:
            print(f"URL: {url}")
            login_detection(url)
        else:
            print("[!] Unable to retrieve URL.\n\n")
    else:
        print(f"[!] Active process '{process}' is not a supported browser.\n\n")

if __name__ == "__main__":
    while True:
        main()
        time.sleep(3)
