import subprocess
import sys
import os
from platform import system
from .sysprompt import sysprompt


def ensure_pool():
    # Ensure local bin is in PATH
    local_bin = os.path.expanduser("~/.local/bin")
    if local_bin not in os.environ.get("PATH", "").split(":"):
        os.environ["PATH"] += ":" + local_bin

    try:
        subprocess.run(["pool", "--version"], capture_output=True, check=True)
    except Exception:
        print("pool CLI not found → installing...")
        subprocess.run(
            "curl -fsSL https://downloads.poolside.ai/pool/install.sh | POOL_INSTALL_ACCEPT_EULA=1 POOL_INSTALL_UPDATE_PATH=0 sh",
            shell=True,
            check=True,
        )

    # Ensure authenticated
    if not os.environ.get("POOLSIDE_API_KEY") and not os.path.exists(os.path.expanduser("~/.config/poolside/credentials.json")):
        print("pool CLI not logged in → logging in...")
        subprocess.run(["pool", "login"], check=True)


def run(entry_file: str):
    if system().lower() == "windows":
        sys.exit("Windows not supported")

    ensure_pool()

    entry_file = os.path.abspath(entry_file)

    if not os.path.exists(entry_file):
        sys.exit(f"File not found: {entry_file}")

    project_dir = os.path.dirname(entry_file)

    # --- sysprompt is the base behavior layer ---
    prompt = (
        sysprompt
        + "\n\n"
        + "TASK:\n"
        + "Convert this Python project into C.\n"
        + "Start from the entry file and follow imports across the project.\n\n"
        + f"ENTRY FILE: {entry_file}"
    )

    subprocess.run(
        [
            "pool",
            "exec",
            "-d",
            project_dir,
            "-p",
            prompt,
            "--unsafe-auto-allow",
        ],
        cwd=project_dir,
        check=True,
    )

    print("Complete")


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: transpilatron <file.py>")

    run(sys.argv[1])


if __name__ == "__main__":
    main()
