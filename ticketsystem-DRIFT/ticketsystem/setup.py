import os
import subprocess
import sys

VENV_DIR = "venv"


def venv_paths():
    if os.name == "nt":
        python = os.path.join(VENV_DIR, "Scripts", "python.exe")
        pip = os.path.join(VENV_DIR, "Scripts", "pip.exe")
    else:
        python = os.path.join(VENV_DIR, "bin", "python")
        pip = os.path.join(VENV_DIR, "bin", "pip")
    return python, pip


def main():
    if not os.path.exists(VENV_DIR):
        print("Lager nytt venv...")
        subprocess.check_call([sys.executable, "-m", "venv", VENV_DIR])

    python, pip = venv_paths()

    print("Laster ned pakker til venv...")
    subprocess.check_call([pip, "install", "-r", "requirements.txt"])

    print("Starter ticket systemet...")
    subprocess.check_call([python, "app.py"])


if __name__ == "__main__":
    main()
