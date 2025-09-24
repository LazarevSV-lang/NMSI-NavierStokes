#!/usr/bin/env python3
import os
import subprocess
import sys
import shutil

def ensure(cmd):
    try:
        subprocess.check_call(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {cmd}\n{e}")
        sys.exit(1)

def main():
    # Install requirements if needed
    if os.path.exists("requirements.txt"):
        ensure(f"{sys.executable} -m pip install -r requirements.txt")

    # Run notebooks with nbconvert (execute in-place)
    notebooks = [
        "NMSI_NSE3D_TG_skeleton.ipynb",
        "NMSI_NSE2D_Compare_ParamSweep.ipynb",
    ]
    for nb in notebooks:
        if not os.path.exists(nb):
            print(f"Missing notebook: {nb}")
            continue
        cmd = f"{sys.executable} -m jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=1200 "{nb}""
        print(f"Executing: {cmd}")
        ensure(cmd)
        # Also save a copy with _EXECUTED suffix
        out = nb.replace(".ipynb", "_EXECUTED.ipynb")
        try:
            shutil.copyfile(nb, out)
        except Exception as e:
            print(f"Copy failed: {e}")

if __name__ == "__main__":
    main()
