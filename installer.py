import os, shutil, json
import sys

def get_install_dir():
    return os.path.join(os.getenv('LOCALAPPDATA'), 'VividVision')

def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller.
    """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def save_script_in_startup(notification_intensity="silent", interval=20*60):
    path_to_startup = os.path.join(
        os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup'
    )
    install_dir = get_install_dir()
    os.makedirs(install_dir, exist_ok=True)

    shutil.copy(resource_path("VividVision.exe"), os.path.join(path_to_startup, "VividVision.exe"))

    config = {"notification_intensity":notification_intensity, "interval":interval}

    with open(os.path.join(install_dir, "config.json"), "w") as f:
        json.dump(config, f, indent=4)


if __name__ == "__main__":
    save_script_in_startup()
