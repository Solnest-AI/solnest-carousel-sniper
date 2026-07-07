"""
Voice-clean caption generator.

Inputs:
- Carousel data JSON (slide content, listing facts, offer details)
- Brand JSON (voice rules, signoff line, handle)

Output: a caption string ready for Instagram, with the brand's voice rules
enforced. Strips em dashes, en dashes, hashtags, and the brand's banned phrases.

This script is intentionally generation-free: it composes the caption from
structured data only. No LLM call. If you want LLM-written captions, swap
this for a wrapper that calls Claude or your model of choice and then runs
the output through enforce_voice_rules() below.
"""
import re


BAD_DASHES = ["—", "–"]
GENERIC_AI_PHRASES = [
    "in today's fast-paced world",
    "unlock the power of",
    "elevate your",
    "take your business to the next level",
    "leverage cutting-edge",
]
HASHTAG_RE = re.compile(r"#\w+", re.UNICODE)


def enforce_voice_rules(text, brand):
    rules = brand.get("voice_rules", {})

    if rules.get("no_em_dashes", True):
        text = text.replace("—", ". ")
    if rules.get("no_en_dashes", True):
        text = text.replace("–", " to ")

    if rules.get("no_hashtags", True):
        text = HASHTAG_RE.sub("", text)

    banned = list(GENERIC_AI_PHRASES) + list(rules.get("banned_phrases", []))
    for phrase in banned:
        pattern = re.compile(re.escape(phrase), re.IGNORECASE)
        text = pattern.sub("", text)

    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" +\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def generate_caption(data, brand):
    listing = data.get("listing", {})
    offer = data.get("offer") or brand.get("offer", {})
    event = data.get("event_anchor")

    lines = []

    title_hook = data.get("caption_hook")
    if title_hook:
        lines.append(title_hook)
    elif listing.get("title"):
        lines.append(f"{listing['title']}.")
    lines.append("")

    facts = []
    if listing.get("beds"):
        facts.append(f"{listing['beds']} bedrooms")
    if listing.get("baths"):
        facts.append(f"{listing['baths']} baths")
    if listing.get("sleeps"):
        facts.append(f"Sleeps {listing['sleeps']}")
    if listing.get("pet_friendly"):
        facts.append("Pet friendly")
    if facts:
        lines.append(". ".join(facts) + ".")
        lines.append("")

    if listing.get("headline_amenities"):
        lines.append(". ".join(listing["headline_amenities"][:5]) + ".")
        lines.append("")

    if listing.get("nearby"):
        for item in listing["nearby"][:4]:
            lines.append(item)
        lines.append("")

    if event:
        lines.append(f"{event.get('name', 'Limited dates')}: {event.get('date_label', '')}".strip())
        if event.get("urgency"):
            lines.append(event["urgency"])
        lines.append("")

    if offer and offer.get("default_code"):
        amount = offer.get("default_amount", "")
        thing = offer.get("default_thing", "your stay")
        lines.append(
            f"Comment {offer['default_code']} below and we will send you the direct booking link with {amount} off {thing}."
        )
        lines.append("")

    if listing.get("location_summary"):
        lines.append(listing["location_summary"])
    if listing.get("rating"):
        rating_line = f"{listing['rating']} stars"
        if listing.get("review_count"):
            rating_line += f" from {listing['review_count']} reviews"
        lines.append(rating_line + ".")
    lines.append("")

    save_line = data.get("save_line") or "Save this post so you can find the property next time you need a getaway."
    lines.append(save_line)
    lines.append("")

    if brand.get("signoff"):
        lines.append(brand["signoff"])

    raw = "\n".join(lines)
    return enforce_voice_rules(raw, brand)
