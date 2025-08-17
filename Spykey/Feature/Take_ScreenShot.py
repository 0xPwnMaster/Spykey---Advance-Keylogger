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
