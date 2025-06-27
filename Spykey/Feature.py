import psutil 
import win32gui 
import win32process
import cv2
import os   
from pywinauto import Application
import pywinauto
import mss
# import selenium
from PIL import Image 
import re
from pathlib import Path
import time

ADDRESS_BAR_TITLES = {
    "chrome.exe": "Address and search bar",
    "msedge.exe": "Address and search bar",
    "brave.exe": "Address and search bar",
    "firefox.exe": "Search with Google or enter address",  # Firefox may vary
    "opera.exe": "Address field",  # Opera-specific
}

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

def Get_activeApp_Data():
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
        print(f"[ERROR in Get_activeApp_Data]: {e}")
        return 0, "Unknown", f"Error: {e}"

def url_detection(hwnd):
    global ADDRESS_BAR_TITLES
    hwnd, _, process_name = Get_activeApp_Data()
    try:
        if process_name not in ADDRESS_BAR_TITLES:
            print(f"[!] Not a supported browser: {process_name}")
            return None

        app = pywinauto.Application(backend='uia').connect(handle=hwnd)
        dlg = app.window(handle=hwnd)

        # Get the title of the address bar for this browser
        bar_title = ADDRESS_BAR_TITLES[process_name]

        # Try to get the address bar and read the value
        address_bar = dlg.child_window(title=bar_title, control_type="Edit")
        url = address_bar.get_value()
        return url
    except (pywinauto.findwindows.ElementNotFoundError, pywinauto.findbestmatch.MatchError) as e:
        print(f"[ERROR locating address bar]: {e}")
    except Exception as e:
        print(f"[Unexpected ERROR in url_detection_chrome]: {e}")
    return None
