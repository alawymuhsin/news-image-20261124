"""Publish the newspaper image for the 24 November 2026 news-image entry.

The picture itself is produced elsewhere and stored next to this script as
entry.png. All this program does is hand that file over to the grading
sandbox: it reads the bytes, makes sure they really look like a JPEG of a
sane size, and drops an identical copy at the output location the harness
expects. Nothing here fetches anything from the network and nothing here
draws or edits the picture.
"""

import os
import sys
from pathlib import Path

PICTURE_NAME = "entry.png"
JPEG_OPENING = b"\xff\xd8\xff"
LARGEST_ACCEPTED = 1_048_576


def locate_picture() -> Path:
    """Return the path of the image sitting beside this script."""
    here = Path(__file__).resolve().parent
    return here / PICTURE_NAME


def pick_destination() -> Path:
    """Return the output folder, honouring the harness variable when set."""
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return Path(chosen)


def main() -> int:
    picture = locate_picture()
    if not picture.is_file():
        print(f"missing picture: {picture}", file=sys.stderr)
        return 1

    picture_bytes = picture.read_bytes()
    if len(picture_bytes) == 0:
        print("picture is empty, refusing to publish it", file=sys.stderr)
        return 1
    if len(picture_bytes) > LARGEST_ACCEPTED:
        print(
            f"picture is {len(picture_bytes)} bytes, over the "
            f"{LARGEST_ACCEPTED} byte limit",
            file=sys.stderr,
        )
        return 1
    if not picture_bytes.startswith(JPEG_OPENING):
        print("picture does not begin with JPEG magic bytes", file=sys.stderr)
        return 1

    destination = pick_destination()
    destination.mkdir(parents=True, exist_ok=True)
    target = destination / PICTURE_NAME
    target.write_bytes(picture_bytes)

    written = target.stat().st_size
    if written != len(picture_bytes):
        print(
            f"wrote {written} bytes but the picture has "
            f"{len(picture_bytes)} bytes",
            file=sys.stderr,
        )
        return 1

    with target.open("rb") as handle:
        opening = handle.read(len(JPEG_OPENING))
    if opening != JPEG_OPENING:
        print("the copied file does not begin with JPEG magic bytes",
              file=sys.stderr)
        return 1

    print(f"published {PICTURE_NAME}: {written} bytes -> {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
