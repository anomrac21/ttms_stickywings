#!/usr/bin/env python3
"""Generate Sticky Wings Hugo menu content from menu board data."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"

SECTION_ICON = {
    "specials": "images/specials.webp",
    "sticky-wings": "images/sticky-wings.webp",
    "packs": "images/packs.webp",
    "combos": "images/combos.webp",
    "chicken-tenders": "images/chicken-tenders.webp",
    "loaded-fries": "images/loaded-fries.webp",
    "mac-and-cheese": "images/mac-and-cheese.webp",
    "pasta": "images/pasta.webp",
    "burgers": "images/burgers.webp",
    "mix": "images/mix.webp",
    "appetizers": "images/appetizers-mozzarella-sticks.webp",
    "sides": "images/sides.webp",
    "salads": "images/salads.webp",
    "desserts": "images/desserts.webp",
    "soup-saturdays": "images/soup-saturdays.webp",
}


def fm(**kwargs) -> str:
    lines = ["---"]
    for key, val in kwargs.items():
        if val is None:
            continue
        if isinstance(val, str):
            lines.append(f"{key}: {val}")
        elif isinstance(val, bool):
            lines.append(f"{key}: {'true' if val else 'false'}")
        elif isinstance(val, (int, float)):
            lines.append(f"{key}: {val}")
        elif isinstance(val, list):
            if not val:
                lines.append(f"{key}: []")
            elif isinstance(val[0], dict):
                lines.append(f"{key}:")
                for item in val:
                    lines.append("  -")
                    for k, v in item.items():
                        if isinstance(v, str) and v in ("-", "|"):
                            lines.append(f"      {k}: '{v}'")
                        else:
                            lines.append(f"      {k}: {v}")
            else:
                lines.append(f"{key}:")
                for item in val:
                    lines.append(f"  - {item}")
        else:
            lines.append(f"{key}: {val}")
    lines.append("---")
    return "\n".join(lines)


def write_item(section: str, slug: str, front: dict, body: str = ""):
    path = CONTENT / section / f"{slug}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    text = fm(**front)
    if body:
        text += "\n\n" + body.strip() + "\n"
    else:
        text += "\n"
    path.write_text(text, encoding="utf-8")


def write_index(section: str, title: str, weight: int, icon: str, body: str = "", images: dict | None = None):
    data = {"title": title, "weight": weight, "icon": icon}
    if images:
        data["images"] = images
    path = CONTENT / section / "_index.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["---"]
    for key, val in data.items():
        if key == "images" and isinstance(val, dict):
            lines.append("images:")
            for k, v in val.items():
                lines.append(f"    {k}: {v}")
        elif key == "weight":
            lines.append(f"weight: {weight}")
        else:
            lines.append(f"{key}: {val}")
    lines.append("---")
    if body:
        lines.append("")
        lines.append(body.strip())
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def single_price(title, price, section, slug, **extra):
    body = extra.pop("body", "")
    front = {
        "title": title,
        "prices": [{"variable1": "-", "variable2": "-", "price": price}],
        "types": extra.pop("types", ["Main"]),
        "tags": extra.pop("tags", []),
        "weight": extra.pop("weight", 1),
        **extra,
    }
    write_item(section, slug, front, body)


def variant1_prices(title, variants, section, slug, **extra):
    body = extra.pop("body", "")
    front = {
        "title": title,
        "prices": [{"variable1": v, "variable2": "-", "price": p} for v, p in variants],
        "types": extra.pop("types", ["Main"]),
        "tags": extra.pop("tags", []),
        "weight": extra.pop("weight", 1),
        **extra,
    }
    write_item(section, slug, front, body)


def sm_lg_prices(title, pairs, section, slug, **extra):
    body = extra.pop("body", "")
    prices = []
    for sm, lg in pairs:
        prices.append({"variable1": "Small", "variable2": "-", "price": sm})
        if lg is not None:
            prices.append({"variable1": "Large", "variable2": "-", "price": lg})
    front = {
        "title": title,
        "prices": prices,
        "types": extra.pop("types", ["Main"]),
        "tags": extra.pop("tags", []),
        "weight": extra.pop("weight", 1),
        **extra,
    }
    write_item(section, slug, front, body)


def main():
    # Section indexes
    sections = [
        ("specials", "Specials", 2, "Wings packs, value meals, and family deals."),
        ("sticky-wings", "Sticky Wings", 3, "Our signature sticky wings — pick your portion."),
        ("packs", "Wing Packs", 4, "Buddy, family, and party packs for sharing."),
        ("combos", "Combos BBQ | Grill | Jerk", 5, "BBQ, grill, and jerk combos. Choose Small or Large."),
        ("chicken-tenders", "Chicken Tenders", 6, "Crispy tenders and combo plates."),
        ("loaded-fries", "Loaded Fries", 7, "Fully loaded fries topped with your choice of protein."),
        ("mac-and-cheese", "Mac & Cheese Bowls", 8, "Creamy mac & cheese bowls — pick your protein."),
        ("pasta", "Pasta Goodness", 9, "Pastas from veggie to jerk chicken."),
        ("burgers", "Burgers", 10, "Sandwiches served alone or with fries."),
        ("mix", "Mix", 11, "Mix & match plates with a side."),
        ("appetizers", "Appetizers & Speciality Sides", 12, "Starters and cheesy sides."),
        ("sides", "Regular Sides", 13, "Crinkle cut, rice, noodles, and more."),
        ("salads", "Salads", 14, "Fresh salads and bowls."),
        ("desserts", "Desserts", 15, "Cakes and cheesecake slices."),
        ("soup-saturdays", "Soup Saturdays", 16, "Homemade soups every Saturday."),
    ]
    for slug, title, weight, body in sections:
        icon = SECTION_ICON[slug]
        write_index(slug, title, weight, icon, body, {"primary": icon})

    # Sticky Wings
    wings = [
        ("4pc & Fries", 38, "4-piece sticky wings with crinkle cut fries."),
        ("6pc & Fries", 58, "6-piece sticky wings with crinkle cut fries."),
        ("6pc & 2 Sides", 65, "6-piece sticky wings with two regular sides."),
        ("10pc & Fries", 75, "10-piece sticky wings with crinkle cut fries."),
        ("Wings & Pasta", 130, "Sticky wings paired with a pasta of your choice."),
        ("6pc Only", 45, "6-piece sticky wings only."),
        ("10pc Only", 65, "10-piece sticky wings only."),
        ("20pc Only", 100, "20-piece sticky wings only."),
    ]
    for i, (title, price, body) in enumerate(wings, 1):
        single_price(title, price, "sticky-wings", title.lower().replace(" & ", "-and-").replace(" ", "-").replace("/", "-"),
                     tags=["Wings"], weight=i, body=body)

    # Packs
    packs = [
        ("Buddy Pack", 160, "20pc wings (2 flavors), large fries, cole slaw & 2L drink.", 1),
        ("Family Pack", 260, "35pc wings (4 flavors), large fries, cole slaw.", 2),
        ("Party Pack", 320, "50pc wings (4 flavors), 2 large fries, 2 cole slaw & 2L drink.", 3),
    ]
    for title, price, body, w in packs:
        single_price(title, price, "packs", title.lower().replace(" ", "-"),
                     types=["Combo"], tags=["Wings", "Shareable"], weight=w,
                     body=body)

    # Specials
    single_price("Family Meal", 149, "specials", "family-meal",
                 types=["Combo"], tags=["BBQ", "Chicken"], weight=1,
                 ingredients=["6pc BBQ chicken", "2 sides", "2L soft drink"],
                 body="6pc BBQ chicken with two sides and a 2L soft drink.")
    value_meals = [
        ("BBQ Chicken Noodles + Drink", 38, "1 pc BBQ chicken with noodles and a small drink.", 2),
        ("Fish + Fries", 60, "Fried fish served with crinkle cut fries.", 3),
        ("Small Wings & Fries + Drink", 38, "Small wings portion with fries and a small drink.", 4),
    ]
    for title, price, body, w in value_meals:
        single_price(title, price, "specials", title.lower().replace(" + ", "-plus-").replace(" ", "-"),
                     types=["Combo"], tags=["Value"], weight=w, body=body)

    # Combos SM/LG
    combos = [
        ("1/4 Chicken L&T", 48, 60, 1),
        ("1/4 Chicken B&W", 60, 65, 2),
        ("1/2 Chicken", 65, None, 3),
        ("Boneless Chicken", 65, 75, 4),
        ("Chicken Tenders", 55, 65, 5),
        ("Lamb", 70, 80, 6),
        ("Beef Ribs", 75, 85, 7),
        ("Fried Fish", 65, 70, 8),
        ("Grilled Fish", 65, 75, 9),
        ("Shrimp", 65, 75, 10),
        ("Oxtail", 75, 85, 11),
    ]
    for title, sm, lg, w in combos:
        sm_lg_prices(title, [(sm, lg)], "combos", title.lower().replace(" ", "-").replace("/", "-"),
                     tags=["Combo"], cookingmethods=["BBQ", "Grill", "Jerk"], weight=w,
                     body=f"{title} combo — choose Small or Large.")

    # Chicken Tenders
    tenders = [
        ("Wings & Tenders", 65, 1),
        ("Tenders & Shrimp", 95, 2),
        ("Tenders & Fries", 55, 3),
        ("Large Tenders & Fries", 65, 4),
    ]
    for title, price, w in tenders:
        single_price(title, price, "chicken-tenders", title.lower().replace(" & ", "-and-").replace(" ", "-"),
                     tags=["Tenders", "Chicken"], weight=w)

    # Loaded Fries (updated prices from latest menu)
    loaded = [
        ("Beef Loaded Fries", 65, 1),
        ("Chicken Loaded Fries", 65, 2),
        ("Lamb Loaded Fries", 70, 3),
        ("Shrimp Loaded Fries", 75, 4),
        ("Veggie Loaded Fries", 45, 5),
    ]
    for title, price, w in loaded:
        single_price(title, price, "loaded-fries", title.lower().replace(" ", "-"),
                     tags=["Fries"], weight=w,
                     body="Crinkle cut fries loaded with cheese and toppings.")

    # Mac & Cheese - protein choice (prices not listed on menu board)
    write_item("mac-and-cheese", "mac-and-cheese-bowl", {
        "title": "Mac & Cheese Bowl",
        "prices": [
            {"variable1": "Chicken", "variable2": "-", "price": 0},
            {"variable1": "Beef", "variable2": "-", "price": 0},
            {"variable1": "Shrimp", "variable2": "-", "price": 0},
            {"variable1": "Lamb", "variable2": "-", "price": 0},
            {"variable1": "Fish", "variable2": "-", "price": 0},
        ],
        "tags": ["New"],
        "types": ["Main"],
        "weight": 1,
    }, "Creamy mac & cheese bowl. Choose chicken, beef, shrimp, lamb, or fish. Ask staff for pricing.")

    # Pasta
    pastas = [
        ("Veggie", 70, 1),
        ("Fasta Pasta", 60, 2),
        ("Chicken Alfredo", 90, 3),
        ("Shrimp Alfredo", 99, 4),
        ("Chicken & Shrimp", 120, 5),
        ("Lamb", 90, 6),
        ("Jerk Chicken Pasta", 90, 7),
    ]
    for title, price, w in pastas:
        single_price(title, price, "pasta", title.lower().replace(" & ", "-and-").replace(" ", "-"),
                     tags=["Pasta"], weight=w)

    # Burgers alone / with fries
    burgers = [
        ("Chicken Sandwich", 45, 55, 1),
        ("Sticky Classic Beef", 50, 60, 2),
        ("Fry Fish Sandwich", 55, 60, 3),
        ("Shrimp Sandwich", 60, 70, 4),
    ]
    for title, alone, fries, w in burgers:
        variant1_prices(title, [("Alone", alone), ("With Fries", fries)], "burgers",
                        title.lower().replace(" ", "-"),
                        tags=["Burger"], weight=w)

    # Mix
    mix_items = [
        ("Chicken & Lamb + 1 Side", 95, 1),
        ("Shrimp & Fish + 1 Side", 100, 2),
        ("Tenders & Shrimp", 95, 3),
    ]
    for title, price, w in mix_items:
        single_price(title, price, "mix", title.lower().replace(" & ", "-and-").replace(" ", "-"),
                     tags=["Mix"], weight=w)

    # Appetizers
    apps = [("Onion Rings", 30, 1), ("Mozzarella Sticks", 30, 2), ("Cheesy Fries", 30, 3)]
    for title, price, w in apps:
        single_price(title, price, "appetizers", title.lower().replace(" ", "-"),
                     types=["Side"], tags=["Appetizer"], weight=w)

    # Sides
    sides = [
        ("Crinkle Cut", 25, 1), ("Rice", 25, 2), ("Noodles", 30, 3),
        ("Creamy Potatoes", 30, 4), ("Cassava", 30, 5), ("Macaroni Salad", 25, 6),
        ("Potato Salad", 25, 7), ("Cole Slaw", 20, 8), ("Fresh Salad", 20, 9),
        ("Garlic Potatoes", 30, 10),
    ]
    for title, price, w in sides:
        single_price(title, price, "sides", title.lower().replace(" ", "-"),
                     types=["Side"], tags=["Side"], weight=w)

    # Salads
    salads = [
        ("Chicken Salad", 55, 1), ("Shrimp Salad", 65, 2),
        ("Fry Fish Salad", 60, 3), ("Mediterranean Quinoa", 45, 4),
    ]
    for title, price, w in salads:
        single_price(title, price, "salads", title.lower().replace(" ", "-"),
                     tags=["Salad"], weight=w)

    # Desserts
    desserts = [
        ("Oreo Cho'l Cheesecake", 40, 1),
        ("Chocolate Cake", 45, 2),
        ("Red Velvet", 40, 3),
        ("Carrot Cake", 40, 4),
        ("Regular Cake Slices", 15, 5),
    ]
    for title, price, w in desserts:
        single_price(title, price, "desserts", title.lower().replace(" ", "-").replace("'", ""),
                     types=["Dessert"], tags=["Dessert"], weight=w)

    # Soup Saturdays
    for title, slug, w in [("Corn Soup", "corn-soup", 1), ("Cow Heel Soup", "cow-heel-soup", 2)]:
        write_item("soup-saturdays", slug, {
            "title": title,
            "events": ["Saturday"],
            "tags": ["Soup", "Special"],
            "types": ["Main"],
            "weight": w,
        }, f"Available Saturdays — {title.lower()}.")

    print(f"Generated menu under {CONTENT}")


if __name__ == "__main__":
    main()
