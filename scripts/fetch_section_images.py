#!/usr/bin/env python3
"""Download section header images and update content/*/_index.md only."""
from __future__ import annotations

import re
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMAGES_DIR = ROOT / "static" / "images"
CONTENT = ROOT / "content"
PEX = "https://images.pexels.com/photos/{id}/pexels-photo-{id}.jpeg?auto=compress&cs=tinysrgb&w=900"
PEX_ALT = {
    "packs.webp": "https://images.pexels.com/photos/60616/fried-chicken-chicken-fried-crunchy-60616.jpeg?auto=compress&cs=tinysrgb&w=900",
    "combos.webp": "https://images.pexels.com/photos/60616/fried-chicken-chicken-fried-crunchy-60616.jpeg?auto=compress&cs=tinysrgb&w=900",
    "chicken-tenders.webp": "https://images.pexels.com/photos/60616/fried-chicken-chicken-fried-crunchy-60616.jpeg?auto=compress&cs=tinysrgb&w=900",
    "salads.webp": "https://images.pexels.com/photos/5938/food-salad-healthy-lunch.jpg?auto=compress&cs=tinysrgb&w=900",
}

# Pexels License — free to use
SECTION_IMAGES: dict[str, tuple[str, str]] = {
    "specials.webp": (PEX.format(id="2233348"), "Pexels"),
    "sticky-wings.webp": (PEX.format(id="106343"), "Pexels"),
    "packs.webp": (PEX_ALT["packs.webp"], "Pexels"),
    "combos.webp": (PEX_ALT["combos.webp"], "Pexels"),
    "chicken-tenders.webp": (PEX_ALT["chicken-tenders.webp"], "Pexels"),
    "loaded-fries.webp": (PEX.format(id="4498573"), "Pexels"),
    "mac-and-cheese.webp": (PEX.format(id="4518843"), "Pexels"),
    "pasta.webp": (PEX.format(id="1437267"), "Pexels"),
    "burgers.webp": (PEX.format(id="1639557"), "Pexels"),
    "mix.webp": (PEX.format(id="2233348"), "Pexels"),
    "sides.webp": (PEX.format(id="1583884"), "Pexels"),
    "salads.webp": (PEX_ALT["salads.webp"], "Pexels"),
    "desserts.webp": (PEX.format(id="291528"), "Pexels"),
    "soup-saturdays.webp": (PEX.format(id="539451"), "Pexels"),
    "promotions.webp": (PEX.format(id="106343"), "Pexels"),
}

SECTION_MAP: dict[str, str] = {
    "specials": "specials.webp",
    "sticky-wings": "sticky-wings.webp",
    "packs": "packs.webp",
    "combos": "combos.webp",
    "chicken-tenders": "chicken-tenders.webp",
    "loaded-fries": "loaded-fries.webp",
    "mac-and-cheese": "mac-and-cheese.webp",
    "pasta": "pasta.webp",
    "burgers": "burgers.webp",
    "mix": "mix.webp",
    "appetizers": "appetizers-mozzarella-sticks.webp",
    "sides": "sides.webp",
    "salads": "salads.webp",
    "desserts": "desserts.webp",
    "soup-saturdays": "soup-saturdays.webp",
    "promotions": "promotions.webp",
}


def download_one(filename: str, url: str) -> bool:
    from PIL import Image

    webp = IMAGES_DIR / filename
    jpg = IMAGES_DIR / filename.replace(".webp", ".jpg")
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            jpg.write_bytes(resp.read())
    except urllib.error.HTTPError as e:
        print(f"SKIP {filename}: HTTP {e.code}")
        return webp.exists()
    Image.open(jpg).save(webp, "WEBP", quality=85)
    jpg.unlink()
    print(f"OK {filename}")
    return True


def img(name: str) -> str:
    return f"images/{name}"


def update_section_index(section: str, image_file: str):
    path = CONTENT / section / "_index.md"
    if not path.exists():
        return
    raw = path.read_text(encoding="utf-8")
    title_m = re.search(r"^title:\s*(.+)$", raw, re.M)
    weight_m = re.search(r"^weight:\s*(.+)$", raw, re.M)
    title = title_m.group(1).strip() if title_m else section
    weight = weight_m.group(1).strip() if weight_m else "1"
    body = raw.split("---", 2)[2].strip() if raw.count("---") >= 2 else ""

    lines = ["---", f"title: {title}", f"weight: {weight}", f"icon: {img(image_file)}"]
    if section != "promotions":
        lines.append("images:")
        lines.append(f"    primary: {img(image_file)}")
    lines.append("---")
    if body:
        lines.extend(["", body])
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main():
    credits = []
    for filename, (url, source) in SECTION_IMAGES.items():
        if download_one(filename, url):
            credits.append(f"- {filename} — {source}")

    for section, image_file in SECTION_MAP.items():
        if section == "appetizers":
            path = CONTENT / "appetizers" / "_index.md"
            body = path.read_text(encoding="utf-8").split("---", 2)[2].strip()
            path.write_text(
                "---\n"
                "title: Appetizers & Speciality Sides\n"
                "weight: 12\n"
                "icon: images/appetizers-mozzarella-sticks.webp\n"
                "images:\n"
                "    primary: images/appetizers-onion-rings.webp\n"
                "---\n\n"
                + (body + "\n" if body else "Starters and cheesy sides.\n"),
                encoding="utf-8",
            )
            continue
        if (IMAGES_DIR / image_file).exists():
            update_section_index(section, image_file)
        else:
            print(f"WARN: missing {image_file} for {section}")

    appetizer = []
    credits_path = IMAGES_DIR / "IMAGE_CREDITS.txt"
    if credits_path.exists():
        appetizer = [ln for ln in credits_path.read_text(encoding="utf-8").splitlines() if "appetizers-" in ln]
    credits_path.write_text(
        "Section photos (Pexels / Unsplash License — free to use):\n"
        + "\n".join(appetizer + credits)
        + "\n",
        encoding="utf-8",
    )
    print("Section headers updated.")


if __name__ == "__main__":
    main()
