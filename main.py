"""news-image-01 entry: copy the finished front page to /output/entry.png.

Standard library only. Run locally with:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out, exist_ok=True)
    shutil.copyfile(
        os.path.join(here, "entry.png"),
        os.path.join(out, "entry.png"),
    )


if __name__ == "__main__":
    main()
