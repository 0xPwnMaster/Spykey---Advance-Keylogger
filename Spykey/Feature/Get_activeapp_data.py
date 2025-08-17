
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

