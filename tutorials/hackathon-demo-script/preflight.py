"""Run the checks for the things that break demos, right before you present.

Each line is PASS, WARN or FAIL. Any FAIL exits with code 1.
"""
import shutil
import socket
import subprocess
import sys
from pathlib import Path

PORT = 8000
results = []


def check(name, status, detail):
    results.append(status)
    print(f"{status:<5}{name}: {detail}")


def data_file():
    p = Path("demo_data.json")
    if not p.is_file():
        return check("test data", "FAIL", "demo_data.json is missing. Run python3 seed_data.py")
    r = subprocess.run([sys.executable, "seed_data.py", "--check"], capture_output=True, text=True)
    check("test data", "PASS" if r.returncode == 0 else "FAIL", r.stdout.strip() or "does not match the seed")


def backup_video():
    p = Path("backup/demo-backup.mp4")
    if not p.is_file():
        return check("backup video", "FAIL", "backup/demo-backup.mp4 is missing. Record it before demo day.")
    size = p.stat().st_size
    if shutil.which("ffprobe"):
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                            "-of", "default=nw=1:nk=1", str(p)], capture_output=True, text=True)
        try:
            secs = float(r.stdout.strip())
        except ValueError:
            return check("backup video", "FAIL", "ffprobe cannot read the file")
        return check("backup video", "PASS" if secs > 0 else "FAIL", f"{secs:.1f}s long, {size} bytes")
    check("backup video", "WARN", f"{size} bytes, ffprobe not found so the length was not checked")


def port_free():
    with socket.socket() as s:
        busy = s.connect_ex(("127.0.0.1", PORT)) == 0
    check(f"port {PORT}", "FAIL" if busy else "PASS", "something is already listening" if busy else "free")


def disk():
    free = shutil.disk_usage(".").free / 1e9
    check("disk space", "PASS" if free > 1 else "FAIL", f"{free:.0f} GB free")


def network():
    try:
        socket.create_connection(("example.com", 443), timeout=3).close()
        check("network", "PASS", "reached example.com on port 443")
    except OSError as e:
        check("network", "WARN", f"cannot reach example.com ({e.__class__.__name__}). Fine only if the demo is offline")


def main():
    for fn in (data_file, backup_video, port_free, disk, network):
        fn()
    failed = results.count("FAIL")
    print(f"{len(results)} checks, {failed} failed.")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
