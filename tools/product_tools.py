import json
import re
from pathlib import Path

from livekit.agents import function_tool

from .memory import memory

PRODUCTS_FILE = Path(__file__).resolve().parent.parent / "data" / "products.json"


def _products():
    return json.loads(PRODUCTS_FILE.read_text(encoding="utf-8"))


def _terms(value):
    terms = set(re.findall(r"[a-z0-9]+", str(value).lower()))
    # Make natural voice queries such as “lilies” match catalog text using “lily”.
    terms.update(word[:-1] for word in list(terms) if word.endswith("s") and len(word) > 3)
    return terms


def _budget_from_text(value):
    """Extract a natural-language rupee limit such as “below 1000” or “under ₹1,000”."""
    match = re.search(r"(?:below|under|less than|within|budget(?: of)?)\s*(?:₹|rs\.?\s*)?([0-9][0-9,]*)", str(value).lower())
    return float(match.group(1).replace(",", "")) if match else 0


@function_tool
async def search_flowers(query: str, color: str = "", occasion: str = "", max_price: float = 0) -> str:
    """Search the floral catalog by flower name, color, occasion, keywords, availability, or budget."""
    query_terms = _terms(query)
    color_terms = _terms(color)
    occasion_terms = _terms(occasion)
    # Voice models sometimes keep the budget inside query or send it as a string.
    try:
        max_price = float(max_price or 0)
    except (TypeError, ValueError):
        max_price = 0
    max_price = max_price or _budget_from_text(query)
    matches = []
    for flower in _products():
        searchable = _terms(" ".join([
            flower["name"], flower["category"], flower["color"], flower["description"], flower["care_tips"],
            " ".join(flower["occasion"])
        ]))
        price_ok = not max_price or flower["price_inr"] <= max_price
        color_ok = not color_terms or color_terms.intersection(_terms(flower["color"]))
        occasion_ok = not occasion_terms or occasion_terms.intersection(_terms(" ".join(flower["occasion"])))
        query_ok = not query_terms or query_terms.intersection(searchable)
        if price_ok and color_ok and occasion_ok and query_ok:
            score = 0
            score += 2 * len(query_terms.intersection(_terms(flower["name"])))
            score += 2 * len(query_terms.intersection(_terms(" ".join(flower["occasion"]))))
            score += 2 * len(color_terms.intersection(_terms(flower["color"])))
            matches.append((score, flower))
    matches.sort(key=lambda item: (-item[0], item[1]["price_inr"]))
    if max_price:
        memory["budget"] = max_price
    if occasion:
        memory["occasion"] = occasion
    if matches:
        memory["preferred_product"] = matches[0][1]["name"]
        return "\n".join(
            f"{f['name']} — ₹{f['price_inr']:,}; {f['availability']}. {f['description']} "
            f"It matches because it suits {', '.join(f['occasion'])} and is {f['color'].lower()}."
            for _, f in matches[:6]
        )
    return "I couldn't find a matching flower. Please try another color, occasion, or budget."


@function_tool
async def recommend_bouquet(occasion: str, max_price: float = 0, color: str = "") -> str:
    """Recommend the best available bouquet for an occasion, color preference, and optional budget."""
    requested = _terms(occasion)
    color_terms = _terms(color)
    candidates = []
    for flower in _products():
        if flower["category"] not in {"Bouquet", "Wedding Bouquet", "Luxury Bouquet", "Basket"}:
            continue
        if max_price and flower["price_inr"] > max_price:
            continue
        occasion_terms = _terms(" ".join(flower["occasion"]))
        score = len(requested.intersection(occasion_terms))
        if color_terms.intersection(_terms(flower["color"])):
            score += 1
        if score:
            candidates.append((score, flower))
    candidates.sort(key=lambda item: (-item[0], item[1]["price_inr"]))
    if not candidates:
        return "I couldn't find a bouquet for that occasion and budget."
    memory["occasion"] = occasion
    memory["preferred_product"] = candidates[0][1]["name"]
    flower = candidates[0][1]
    return (f"I recommend {flower['name']} for {occasion}. It costs ₹{flower['price_inr']:,}, is {flower['availability'].lower()}, "
            f"and matches because {flower['description']} Care tip: {flower['care_tips']}")
