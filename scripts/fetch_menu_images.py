#!/usr/bin/env python3
"""Download Unsplash menu images and update ttms_stickywings content references."""
from __future__ import annotations

import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMAGES = ROOT / "static" / "images"
CONTENT = ROOT / "content"

# Unsplash License — see static/images/IMAGE_CREDITS.txt
DOWNLOADS: dict[str, tuple[str, str]] = {
    "sticky-wings.webp": (
        "https://images.unsplash.com/photo-1608038098749-68d3f081430a?auto=format&fit=crop&w=900&q=80",
        "Timothy Miley (unsplash.com/photos/68d3f081430a)",
    ),
    "chicken-tenders.webp": (
        "https://images.unsplash.com/photo-1626645733644-4c887aa39ad7?auto=format&fit=crop&w=900&q=80",
        "Eiliv Aceron (unsplash.com/photos/4c887aa39ad7)",
    ),
    "combos-jerk-chicken.webp": (
        "https://images.unsplash.com/photo-1598103442097-256b64513061?auto=format&fit=crop&w=900&q=80",
        "Chad Montano (unsplash.com/photos/256b64513061)",
    ),
    "combos-beef-ribs.webp": (
        "https://images.unsplash.com/photo-1544025162-d76694265938?auto=format&fit=crop&w=900&q=80",
        "Randy Fath (unsplash.com/photos/d76694265938)",
    ),
    "combos-lamb.webp": (
        "https://images.unsplash.com/photo-1529692236671-f1f6cf9683ba?auto=format&fit=crop&w=900&q=80",
        "Eaters Collective (unsplash.com/photos/f1f6cf9683ba)",
    ),
    "combos-fried-fish.webp": (
        "https://images.unsplash.com/photo-1625937287822-0fad47f3bc92?auto=format&fit=crop&w=900&q=80",
        "Mariana Silva (unsplash.com/photos/0fad47f3bc92)",
    ),
    "combos-shrimp.webp": (
        "https://images.unsplash.com/photo-1565680018434-b149a059510c?auto=format&fit=crop&w=900&q=80",
        "Michael M (unsplash.com/photos/b149a059510c)",
    ),
    "combos-oxtail.webp": (
        "https://images.unsplash.com/photo-1604908178257-2a4c8c2e2f2e?auto=format&fit=crop&w=900&q=80",
        "Eaters Collective (unsplash.com/photos/2a4c8c2e2f2e)",
    ),
    "burgers-beef.webp": (
        "https://images.unsplash.com/photo-1568901346715-3542a09d49b6?auto=format&fit=crop&w=900&q=80",
        "James Goulty (unsplash.com/photos/3542a09d49b6)",
    ),
    "burgers-chicken.webp": (
        "https://images.unsplash.com/photo-1606755962774-008e7f9b6c64?auto=format&fit=crop&w=900&q=80",
        "Sam Moqadam (unsplash.com/photos/008e7f9b6c64)",
    ),
    "loaded-fries.webp": (
        "https://images.unsplash.com/photo-1743193711514-4f7bc5d78d4d?auto=format&fit=crop&w=900&q=80",
        "fellipe teixeira (unsplash.com/photos/4f7bc5d78d4d)",
    ),
    "loaded-fries-veggie.webp": (
        "https://images.unsplash.com/photo-1576107232684-1279f390104a?auto=format&fit=crop&w=900&q=80",
        "Louis Hansel (unsplash.com/photos/1279f390104a)",
    ),
    "mac-and-cheese.webp": (
        "https://images.unsplash.com/photo-1543339496-8ea465f39684?auto=format&fit=crop&w=900&q=80",
        "Eaters Collective (unsplash.com/photos/8ea465f39684)",
    ),
    "pasta-alfredo.webp": (
        "https://images.unsplash.com/photo-1645118290616-b64da52f5f1?auto=format&fit=crop&w=900&q=80",
        "Pablo Merchan Montes (unsplash.com/photos/b64da52f5f1)",
    ),
    "pasta-veggie.webp": (
        "https://images.unsplash.com/photo-1473090290779-42810966226?auto=format&fit=crop&w=900&q=80",
        "Eaters Collective (unsplash.com/photos/42810966226)",
    ),
    "sides-fries.webp": (
        "https://images.unsplash.com/photo-1576107232684-1279f390104a?auto=format&fit=crop&w=900&q=80",
        "Louis Hansel (unsplash.com/photos/1279f390104a)",
    ),
    "sides-rice.webp": (
        "https://images.unsplash.com/photo-1536304991221-684486c7defb?auto=format&fit=crop&w=900&q=80",
        "Chad Montano (unsplash.com/photos/684486c7defb)",
    ),
    "sides-potatoes.webp": (
        "https://images.unsplash.com/photo-1517686469429-61d945742d97?auto=format&fit=crop&w=900&q=80",
        "Eaters Collective (unsplash.com/photos/61d945742d97)",
    ),
    "sides-salad.webp": (
        "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=900&q=80",
        "Anna Pelzer (unsplash.com/photos/a57141f2eefd)",
    ),
    "salads-chicken.webp": (
        "https://images.unsplash.com/photo-1546793665-c74683f339c1?auto=format&fit=crop&w=900&q=80",
        "Anna Pelzer (unsplash.com/photos/c74683f339c1)",
    ),
    "salads-shrimp.webp": (
        "https://images.unsplash.com/photo-1553907758-0e5de59d9e55?auto=format&fit=crop&w=900&q=80",
        "Eaters Collective (unsplash.com/photos/0e5de59d9e55)",
    ),
    "salads-quinoa.webp": (
        "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=900&q=80",
        "Anna Pelzer (unsplash.com/photos/a57141f2eefd)",
    ),
    "desserts-chocolate-cake.webp": (
        "https://images.unsplash.com/photo-1578985545069-3cbad1d69fbe?auto=format&fit=crop&w=900&q=80",
        "American Heritage Chocolate (unsplash.com/photos/3cbad1d69fbe)",
    ),
    "desserts-cheesecake.webp": (
        "https://images.unsplash.com/photo-1524351199678-a2a6a837d682?auto=format&fit=crop&w=900&q=80",
        "Alexander Maasch (unsplash.com/photos/a2a6a837d682)",
    ),
    "desserts-red-velvet.webp": (
        "https://images.unsplash.com/photo-1586788680434-30d32483d865?auto=format&fit=crop&w=900&q=80",
        "American Heritage Chocolate (unsplash.com/photos/30d32483d865)",
    ),
    "desserts-carrot-cake.webp": (
        "https://images.unsplash.com/photo-1621303837174-897879a02185?auto=format&fit=crop&w=900&q=80",
        "American Heritage Chocolate (unsplash.com/photos/897879a02185)",
    ),
    "desserts-cake-slice.webp": (
        "https://images.unsplash.com/photo-1563729784474-d77dbb933a9e?auto=format&fit=crop&w=900&q=80",
        "American Heritage Chocolate (unsplash.com/photos/d77dbb933a9e)",
    ),
    "soup-corn.webp": (
        "https://images.unsplash.com/photo-1547596428-0b5aab7b3651?auto=format&fit=crop&w=900&q=80",
        "Eaters Collective (unsplash.com/photos/0b5aab7b3651)",
    ),
    "soup-hearty.webp": (
        "https://images.unsplash.com/photo-1604908178257-2a4c8c2e2f2e?auto=format&fit=crop&w=900&q=80",
        "Eaters Collective (unsplash.com/photos/2a4c8c2e2f2e)",
    ),
    "packs-wings.webp": (
        "https://images.unsplash.com/photo-1694146873317-ae4e6c8f43fe?auto=format&fit=crop&w=900&q=80",
        "Abigail Lynn (unsplash.com/photos/ae4e6c8f43fe)",
    ),
    "specials-bbq-chicken.webp": (
        "https://images.unsplash.com/photo-1598103442097-256b64513061?auto=format&fit=crop&w=900&q=80",
        "Chad Montano (unsplash.com/photos/256b64513061)",
    ),
    "mix-platter.webp": (
        "https://images.unsplash.com/photo-1529692236671-f1f6cf9683ba?auto=format&fit=crop&w=900&q=80",
        "Eaters Collective (unsplash.com/photos/f1f6cf9683ba)",
    ),
}

SECTION_INDEX: dict[str, dict[str, str]] = {
    "specials": {
        "icon": "specials-bbq-chicken.webp",
        "primary": "sticky-wings.webp",
        "secondary": "specials-bbq-chicken.webp",
    },
    "sticky-wings": {"icon": "sticky-wings.webp", "primary": "sticky-wings.webp", "secondary": "packs-wings.webp"},
    "packs": {"icon": "packs-wings.webp", "primary": "packs-wings.webp", "secondary": "sticky-wings.webp"},
    "combos": {"icon": "combos-jerk-chicken.webp", "primary": "combos-jerk-chicken.webp", "secondary": "combos-beef-ribs.webp"},
    "chicken-tenders": {"icon": "chicken-tenders.webp", "primary": "chicken-tenders.webp", "secondary": "sticky-wings.webp"},
    "loaded-fries": {"icon": "loaded-fries.webp", "primary": "loaded-fries.webp", "secondary": "loaded-fries-veggie.webp"},
    "mac-and-cheese": {"icon": "mac-and-cheese.webp", "primary": "mac-and-cheese.webp", "secondary": "loaded-fries.webp"},
    "pasta": {"icon": "pasta-alfredo.webp", "primary": "pasta-alfredo.webp", "secondary": "pasta-veggie.webp"},
    "burgers": {"icon": "burgers-beef.webp", "primary": "burgers-beef.webp", "secondary": "burgers-chicken.webp"},
    "mix": {"icon": "mix-platter.webp", "primary": "mix-platter.webp", "secondary": "combos-jerk-chicken.webp"},
    "appetizers": {
        "icon": "appetizers-mozzarella-sticks.webp",
        "primary": "appetizers-onion-rings.webp",
        "secondary": "appetizers-cheesy-fries.webp",
    },
    "sides": {"icon": "sides-fries.webp", "primary": "sides-fries.webp", "secondary": "sides-potatoes.webp"},
    "salads": {"icon": "salads-chicken.webp", "primary": "salads-chicken.webp", "secondary": "salads-quinoa.webp"},
    "desserts": {"icon": "desserts-chocolate-cake.webp", "primary": "desserts-cheesecake.webp", "secondary": "desserts-red-velvet.webp"},
    "soup-saturdays": {"icon": "soup-corn.webp", "primary": "soup-corn.webp", "secondary": "soup-hearty.webp"},
    "promotions": {"icon": "sticky-wings.webp"},
}

ITEM_IMAGES: dict[tuple[str, str], str] = {
    # specials
    ("specials", "family-meal"): "specials-bbq-chicken.webp",
    ("specials", "bbq-chicken-noodles-plus-drink"): "specials-bbq-chicken.webp",
    ("specials", "fish-plus-fries"): "combos-fried-fish.webp",
    ("specials", "small-wings-&-fries-plus-drink"): "sticky-wings.webp",
    # sticky-wings — all wings
    **{( "sticky-wings", p.stem): "sticky-wings.webp" for p in (CONTENT / "sticky-wings").glob("*.md") if p.name != "_index.md"},
    # packs
    **{( "packs", p.stem): "packs-wings.webp" for p in (CONTENT / "packs").glob("*.md") if p.name != "_index.md"},
    # combos
    ("combos", "1-4-chicken-l&t"): "combos-jerk-chicken.webp",
    ("combos", "1-4-chicken-b&w"): "combos-jerk-chicken.webp",
    ("combos", "1-2-chicken"): "combos-jerk-chicken.webp",
    ("combos", "boneless-chicken"): "combos-jerk-chicken.webp",
    ("combos", "chicken-tenders"): "chicken-tenders.webp",
    ("combos", "lamb"): "combos-lamb.webp",
    ("combos", "beef-ribs"): "combos-beef-ribs.webp",
    ("combos", "fried-fish"): "combos-fried-fish.webp",
    ("combos", "grilled-fish"): "combos-fried-fish.webp",
    ("combos", "shrimp"): "combos-shrimp.webp",
    ("combos", "oxtail"): "combos-oxtail.webp",
    # chicken-tenders
    **{( "chicken-tenders", p.stem): "chicken-tenders.webp" for p in (CONTENT / "chicken-tenders").glob("*.md") if p.name != "_index.md"},
    # loaded-fries
    ("loaded-fries", "veggie-loaded-fries"): "loaded-fries-veggie.webp",
    **{( "loaded-fries", p.stem): "loaded-fries.webp" for p in (CONTENT / "loaded-fries").glob("*.md") if p.name != "_index.md" and p.stem != "veggie-loaded-fries"},
    # mac-and-cheese
    ("mac-and-cheese", "mac-and-cheese-bowl"): "mac-and-cheese.webp",
    # pasta
    ("pasta", "veggie"): "pasta-veggie.webp",
    ("pasta", "fasta-pasta"): "pasta-veggie.webp",
    ("pasta", "jerk-chicken-pasta"): "combos-jerk-chicken.webp",
    **{( "pasta", p.stem): "pasta-alfredo.webp" for p in (CONTENT / "pasta").glob("*.md") if p.name != "_index.md" and p.stem not in {"veggie", "fasta-pasta", "jerk-chicken-pasta"}},
    # burgers
    ("burgers", "chicken-sandwich"): "burgers-chicken.webp",
    ("burgers", "sticky-classic-beef"): "burgers-beef.webp",
    ("burgers", "fry-fish-sandwich"): "combos-fried-fish.webp",
    ("burgers", "shrimp-sandwich"): "combos-shrimp.webp",
    # mix
    ("mix", "chicken-and-lamb-+-1-side"): "mix-platter.webp",
    ("mix", "shrimp-and-fish-+-1-side"): "combos-fried-fish.webp",
    ("mix", "tenders-and-shrimp"): "chicken-tenders.webp",
    # appetizers — keep existing filenames
    ("appetizers", "onion-rings"): "appetizers-onion-rings.webp",
    ("appetizers", "mozzarella-sticks"): "appetizers-mozzarella-sticks.webp",
    ("appetizers", "cheesy-fries"): "appetizers-cheesy-fries.webp",
    # sides
    ("sides", "crinkle-cut"): "sides-fries.webp",
    ("sides", "rice"): "sides-rice.webp",
    ("sides", "noodles"): "pasta-veggie.webp",
    ("sides", "creamy-potatoes"): "sides-potatoes.webp",
    ("sides", "cassava"): "sides-fries.webp",
    ("sides", "macaroni-salad"): "sides-salad.webp",
    ("sides", "potato-salad"): "sides-salad.webp",
    ("sides", "cole-slaw"): "sides-salad.webp",
    ("sides", "fresh-salad"): "sides-salad.webp",
    ("sides", "garlic-potatoes"): "sides-potatoes.webp",
    # salads
    ("salads", "chicken-salad"): "salads-chicken.webp",
    ("salads", "shrimp-salad"): "salads-shrimp.webp",
    ("salads", "fry-fish-salad"): "combos-fried-fish.webp",
    ("salads", "mediterranean-quinoa"): "salads-quinoa.webp",
    # desserts
    ("desserts", "oreo-chol-cheesecake"): "desserts-cheesecake.webp",
    ("desserts", "chocolate-cake"): "desserts-chocolate-cake.webp",
    ("desserts", "red-velvet"): "desserts-red-velvet.webp",
    ("desserts", "carrot-cake"): "desserts-carrot-cake.webp",
    ("desserts", "regular-cake-slices"): "desserts-cake-slice.webp",
    # soup
    ("soup-saturdays", "corn-soup"): "soup-corn.webp",
    ("soup-saturdays", "cow-heel-soup"): "soup-hearty.webp",
}


def img(name: str) -> str:
    return f"images/{name}"


def download_images() -> list[str]:
    try:
        from PIL import Image
    except ImportError:
        Image = None  # type: ignore

    IMAGES.mkdir(parents=True, exist_ok=True)
    credits: list[str] = []
    for filename, (url, credit) in DOWNLOADS.items():
        jpg = IMAGES / filename.replace(".webp", ".jpg")
        webp = IMAGES / filename
        if webp.exists():
            credits.append(f"- {filename} — {credit}")
            continue
        print(f"Downloading {filename}...")
        urllib.request.urlretrieve(url, jpg)
        if Image:
            Image.open(jpg).save(webp, "WEBP", quality=85)
            jpg.unlink()
        else:
            jpg.rename(webp)
        credits.append(f"- {filename} — {credit}")
    return credits


def set_item_image(text: str, image_path: str) -> str:
    if "images:" not in text:
        block = f"images:\n  -\n      image: {image_path}\n"
        return text.replace("---\n", f"---\n{block}", 1) if text.startswith("---") else block + text
    return re.sub(
        r"(images:\s*\n\s*-\s*\n\s*image:\s*)images/[^\n]+",
        rf"\1{image_path}",
        text,
        count=1,
    )


def write_section_index(section: str, meta: dict[str, str]):
    path = CONTENT / section / "_index.md"
    if not path.exists():
        return
    raw = path.read_text(encoding="utf-8")
    title_m = re.search(r"^title:\s*(.+)$", raw, re.M)
    weight_m = re.search(r"^weight:\s*(.+)$", raw, re.M)
    title = title_m.group(1).strip() if title_m else section
    weight = weight_m.group(1).strip() if weight_m else "1"
    body_text = raw.split("---", 2)[2].strip() if raw.count("---") >= 2 else ""
    lines = ["---", f"title: {title}", f"weight: {weight}", f"icon: {img(meta['icon'])}"]
    if "primary" in meta:
        lines.append("images:")
        lines.append(f"    primary: {img(meta['primary'])}")
        lines.append(f"    secondary: {img(meta['secondary'])}")
    lines.append("---")
    if body_text:
        lines.extend(["", body_text])
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def update_home_index():
    path = CONTENT / "_index.md"
    text = path.read_text(encoding="utf-8")
    title_m = re.search(r'^title:\s*"(.+)"', text, re.M)
    title = title_m.group(1) if title_m else "Sticky Wings"
    body = text.split("---", 2)[2].strip() if text.count("---") >= 2 else ""
    new = f"""---
title: "{title}"
image: {img("sticky-wings.webp")}
images:
    - image: {img("sticky-wings.webp")}
    - image: {img("chicken-tenders.webp")}
    - image: {img("combos-jerk-chicken.webp")}
slideshow:
    - image: {img("sticky-wings.webp")}
    - image: {img("chicken-tenders.webp")}
    - image: {img("burgers-beef.webp")}
    - image: {img("loaded-fries.webp")}
---

{body}
"""
    path.write_text(new, encoding="utf-8")


def update_content_images():
    for section, meta in SECTION_INDEX.items():
        write_section_index(section, meta)

    for md in CONTENT.rglob("*.md"):
        if md.name == "_index.md" or md.parent.name == "promotions":
            continue
        section = md.parent.name
        slug = md.stem
        key = (section, slug)
        image_file = ITEM_IMAGES.get(key)
        if not image_file:
            print(f"WARN: no image mapping for {section}/{slug}")
            continue
        text = md.read_text(encoding="utf-8")
        updated = set_item_image(text, img(image_file))
        if updated != text:
            md.write_text(updated, encoding="utf-8")

    # promotions icon only
    promo = CONTENT / "promotions" / "_index.md"
    promo.write_text(
        "---\n"
        f"title: Promotions\nweight: 1\nicon: {img('sticky-wings.webp')}\n---\n",
        encoding="utf-8",
    )
    update_home_index()


def write_credits(extra: list[str]):
    existing = (IMAGES / "IMAGE_CREDITS.txt").read_text(encoding="utf-8") if (IMAGES / "IMAGE_CREDITS.txt").exists() else ""
    appetizer_lines = [ln for ln in existing.splitlines() if "appetizers-" in ln]
    all_credits = appetizer_lines + extra
    header = "Menu photos (Unsplash License — free to use):\n"
    (IMAGES / "IMAGE_CREDITS.txt").write_text(header + "\n".join(all_credits) + "\n", encoding="utf-8")


def main():
    credits = download_images()
    update_content_images()
    write_credits(credits)
    print("Done — images and content updated.")


if __name__ == "__main__":
    main()
