import argparse
import subprocess
import sys
import os
from platform import system
from .prompts import MINIMAL_PROMPT, USUAL_PROMPT


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


def run(entry_file: str, mode: str):
    if system().lower() == "windows":
        sys.exit("Windows not supported")

    ensure_pool()

    entry_file = os.path.abspath(entry_file)

    if not os.path.exists(entry_file):
        sys.exit(f"File not found: {entry_file}")

    project_dir = os.path.dirname(entry_file)

    # Select prompt based on mode
    if mode == "minimal":
        prompt_body = MINIMAL_PROMPT
    else:
        prompt_body = USUAL_PROMPT

    # --- sysprompt is the base behavior layer ---
    prompt = (
        prompt_body
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
    parser = argparse.ArgumentParser(description="Transpile Python to C via AI agent.")
    parser.add_argument(
        "--minimal",
        action="store_const",
        dest="mode",
        const="minimal",
        help="Use minimal mode: static linking, raw sockets only, no torch/tflite/web frameworks",
    )
    parser.add_argument(
        "--usual",
        action="store_const",
        dest="mode",
        const="usual",
        help="Use usual mode (default): dynamic linking, libcurl, libtorch, tflite, web frameworks",
    )
    parser.add_argument("entry_file", help="Python entry file to transpile")
    args = parser.parse_args()

    mode = args.mode if args.mode else "usual"
    run(args.entry_file, mode)


if __name__ == "__main__":
    main()
