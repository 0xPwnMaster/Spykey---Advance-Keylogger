import psutil
import win32gui
import win32process
# import selenium 
# import mss
# import regex as re 

def Get_activeApp_Data():
    try:
        hwnd = win32gui.GetForegroundWindow()
        process_title = win32gui.GetWindowText(hwnd)
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        p = psutil.Process(pid)
        process_name = p.name().lower().strip()
        print(process_name, process_title)
        return process_title, process_name
    except Exception as e:
        return "Unknown", f"Error: {e}"

def Get_browser_data():
    pass