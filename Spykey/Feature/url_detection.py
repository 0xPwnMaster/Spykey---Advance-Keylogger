
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
