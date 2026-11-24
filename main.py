"""Copy the newspaper front page for 24 November 2026 to /output/entry.png.

The entry is a single pre-rendered image (entry.png, next to this script).
This program only copies it into the output directory the judge reads.
Standard library only; no network access is needed or used.
"""

import shutil
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "entry.png"
DEST_DIR = Path("/output")
DEST = DEST_DIR / "entry.png"


def main() -> None:
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, DEST)
    # Verify the copy landed intact before reporting success.
    if DEST.stat().st_size != SOURCE.stat().st_size:
        raise RuntimeError(f"copy incomplete: {DEST} is not {SOURCE.stat().st_size} bytes")
    # The entry must be a JPEG under the name entry.png: fail loudly
    # instead of handing the judge a corrupt or wrong-format file.
    if DEST.read_bytes()[:3] != b"\xff\xd8\xff":
        raise RuntimeError(f"{DEST} is not a JPEG (bad magic bytes)")
    print(f"Copied {SOURCE} -> {DEST} ({DEST.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
