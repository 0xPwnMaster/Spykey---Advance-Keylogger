import subprocess
import sys

# Function to run PowerShell commands
def run_powershell_command(command):
    try:
        result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True, check=True)
        print(f"Success: {command}\nOutput: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {command}\nError: {e.stderr}")
        return False

def install_python():
    print("Installing Python...")
    ps_command = """
    $pythonUrl = 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe'
    $pythonInstaller = '$env:TEMP\\python-installer.exe'
    Invoke-WebRequest -Uri $pythonUrl -OutFile $pythonInstaller
    Start-Process -FilePath $pythonInstaller -ArgumentList '/quiet InstallAllUsers=1 PrependPath=1' -Wait
    Remove-Item $pythonInstaller
    python --version
    """
    return run_powershell_command(ps_command)

def install_git():
    print("Installing Git...")
    ps_command = """
    $gitUrl = 'https://github.com/git-for-windows/git/releases/download/v2.50.0.windows.1/Git-2.50.0-64-bit.exe'
    $gitInstaller = '$env:TEMP\\git-installer.exe'
    Invoke-WebRequest -Uri $gitUrl -OutFile $gitInstaller
    Start-Process -FilePath $gitInstaller -ArgumentList '/VERYSILENT /NORESTART /COMPONENTS=gitlfs,assoc,autoupdate' -Wait
    Remove-Item $gitInstaller
    git --version
    """
    return run_powershell_command(ps_command)

def install_python_modules():
    required_packages = [
        "pynput",
        "psutil",
        "pywin32",
        "opencv-python",
        "pywinauto",
        "mss",
        "Pillow"
    ]

    all_success = True

    for module in required_packages:
        print(f"Installing {module} module...")
        ps_command = f"python -m pip install --quiet {module}"
        success = run_powershell_command(ps_command)
        if not success:
            all_success = False  # Track failure but continue to next module

    return all_success

def main():
    if not install_python():
        print("Failed to install Python.")
        sys.exit(1)
    if not install_git():
        print("Failed to install Git.")
        sys.exit(1)
    if not install_python_modules():
        print("Failed to install Python modules.")
        sys.exit(1)
    print("All dependencies installed successfully.")

if __name__ == "__main__":
    main()