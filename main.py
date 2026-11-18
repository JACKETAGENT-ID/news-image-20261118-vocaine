#!/usr/bin/env python3
"""Entry program for news-image-20261118 (vocaine).

Copies the pre-rendered entry image (entry.png, built by generate.py)
to the make.fun output directory. Standard library only, no network,
deterministic: both runs write identical bytes.
"""
import os
import shutil
import sys


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "./out"
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    if not os.path.isfile(src):
        print("entry.png not found next to main.py", file=sys.stderr)
        return 1
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote", dst, os.path.getsize(dst), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
