import subprocess, os
from mcp import tool

# UNGUARDED — must be flagged
@tool
def run_command(cmd: str) -> str:
    return subprocess.run(cmd, shell=True, capture_output=True).stdout.decode()

# GUARDED — must NOT be flagged (authorize dominates)
@tool
def safe_delete(path: str) -> None:
    authorize(path)
    os.remove(path)

# DEFEATED GUARD — must be flagged (guard result discarded)
@tool
def risky_delete(path: str) -> None:
    authorize(path)
    os.remove(path)

def authorize(path: str) -> None:
    if not path.startswith("/tmp/"):
        raise PermissionError(path)
// trigger PR

# New unguarded sink added in PR
@tool
def new_unguarded(cmd: str) -> str:
    return subprocess.run(cmd, shell=True, capture_output=True).stdout.decode()
