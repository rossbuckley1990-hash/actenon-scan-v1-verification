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

# New unguarded sink for v1.3.1 PR test
@tool
def new_v131_unguarded(cmd: str) -> str:
    return subprocess.run(cmd, shell=True, capture_output=True).stdout.decode()

# Second push — another unguarded sink
@tool
def second_push_unguarded(cmd: str) -> str:
    return subprocess.run(cmd, shell=True, capture_output=True).stdout.decode()

# D3A: exercise the public @v1 consumer after the v1.5.0 release recovery.
# Verification expectations include the repository's existing guard configuration.
