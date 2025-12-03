"""
Response Style Templates
========================
Rotating response styles for the YG Gentleman Bot.
Each style has a unique personality while maintaining the refined tone.
All responses incorporate "YN peasant" to emphasize the transformation.
"""

import random

# Response style templates
# {correction} will be replaced with the YG phrase
# {phrase} will be replaced with the detected YN phrase (optional)

RESPONSE_STYLES = [
    # Style A - The Butler (Warm & Welcoming)
    {
        "name": "The Butler",
        "templates": [
            'Ahem, such YN peasant speak... a gentleman would say: "{correction}"',
            'Pardon me, but that is YN peasant vernacular. Might one suggest: "{correction}"',
            'A YN peasant utterance detected. The refined expression is: "{correction}"',
            'Dear sir, leave the YN peasant words behind. Perhaps: "{correction}"',
        ]
    },

    # Style B - The Professor (Educational)
    {
        "name": "The Professor",
        "templates": [
            'A note on etiquette: that is YN peasant dialect. "{correction}" is the preferred phrasing.',
            'For one\'s edification: YN peasant speak has no place here. Try "{correction}"',
            'The YN peasant tongue betrays you. The gentlemanly expression is "{correction}"',
            'Such YN peasant vocabulary! The distinguished vernacular would be: "{correction}"',
        ]
    },

    # Style C - The Mentor (Encouraging)
    {
        "name": "The Mentor",
        "templates": [
            'Still speaking like a YN peasant? Rise up, good sir. Try: "{correction}"',
            'One shows YN peasant tendencies. The refined alternative: "{correction}"',
            'Shed the YN peasant ways! A gentleman in training says: "{correction}"',
            'That YN peasant phrase must go. Might one suggest: "{correction}"',
        ]
    },

    # Style D - The Aristocrat (Playful)
    {
        "name": "The Aristocrat",
        "templates": [
            'Good heavens, such YN peasant gibberish! Might one suggest: "{correction}"',
            'I say! That YN peasant drivel! A gentleman would phrase it thus: "{correction}"',
            'Gracious me, pure YN peasant babble! The proper expression: "{correction}"',
            'Heavens above, YN peasant nonsense! One means to say: "{correction}"',
        ]
    },

    # Style E - The Connoisseur (Refined)
    {
        "name": "The Connoisseur",
        "templates": [
            'That reeks of YN peasant origins. A distinguished gentleman says: "{correction}"',
            'YN peasant speech detected. The mark of refinement: "{correction}"',
            'How very YN peasant of you. For the discerning gentleman: "{correction}"',
            'Such YN peasant crudeness! The cultivated expression: "{correction}"',
        ]
    },

    # Style F - The Elder (Wise)
    {
        "name": "The Elder",
        "templates": [
            'In my day, we left YN peasant speak behind. One says: "{correction}"',
            'The wisdom of gentlemen rejects YN peasant tongue: "{correction}"',
            'Cast off the YN peasant chains! As the distinguished elders say: "{correction}"',
            'YN peasant words have no power here. Time-honoured refinement suggests: "{correction}"',
        ]
    },

    # Style G - The Diplomat (Gracious)
    {
        "name": "The Diplomat",
        "templates": [
            'With respect, that is YN peasant parlance. Might one offer: "{correction}"',
            'A YN peasant slip, perhaps? With the utmost respect: "{correction}"',
            'One detects YN peasant influence. One ventures to propose: "{correction}"',
            'Forgive the correction, but YN peasants speak thus. Try: "{correction}"',
        ]
    },

    # Style H - The Steward (Helpful)
    {
        "name": "The Steward",
        "templates": [
            'That YN peasant phrase won\'t do, dear fellow. The proper expression: "{correction}"',
            'Allow me to elevate you from YN peasant speak: "{correction}"',
            'YN peasant vocabulary detected. For your consideration: "{correction}"',
            'We don\'t speak like YN peasants here. A refinement: "{correction}"',
        ]
    },
]

# Special occasion responses (used rarely for variety)
SPECIAL_RESPONSES = [
    'Ah, the YN peasant to YG transformation continues! "{correction}"',
    'From YN peasant to Young Gentleman, one step at a time: "{correction}"',
    'The YN peasant fades, the gentleman emerges: "{correction}"',
    'Quarter-zip energy rejects YN peasant speak: "{correction}"',
    'Matcha-sipping gentlemen don\'t talk like YN peasants: "{correction}"',
    'Black excellence refined. Leave the YN peasant behind: "{correction}"',
    'YN peasant? In THIS group? Absolutely not: "{correction}"',
    'The audacity of YN peasant speak! One says: "{correction}"',
]


def get_random_response(correction: str, use_special: bool = False) -> str:
    """
    Get a random response with the correction inserted.

    Args:
        correction: The YG phrase to insert
        use_special: If True, 10% chance to use special response

    Returns:
        Formatted response string
    """
    # 10% chance for special response if enabled
    if use_special and random.random() < 0.10:
        template = random.choice(SPECIAL_RESPONSES)
    else:
        # Pick a random style
        style = random.choice(RESPONSE_STYLES)
        # Pick a random template from that style
        template = random.choice(style["templates"])

    return template.format(correction=correction)


def get_response_by_style(correction: str, style_name: str) -> str:
    """
    Get a response from a specific style.

    Args:
        correction: The YG phrase to insert
        style_name: Name of the style (e.g., "The Butler")

    Returns:
        Formatted response string
    """
    for style in RESPONSE_STYLES:
        if style["name"].lower() == style_name.lower():
            template = random.choice(style["templates"])
            return template.format(correction=correction)

    # Fallback to random if style not found
    return get_random_response(correction)


def list_styles() -> list[str]:
    """Return list of all available style names."""
    return [style["name"] for style in RESPONSE_STYLES]


if __name__ == "__main__":
    # Test the styles
    test_correction = "Good evening, gentlemen"

    print("All available styles:")
    for style_name in list_styles():
        print(f"  - {style_name}")

    print("\nSample responses:")
    for _ in range(10):
        print(f"  {get_random_response(test_correction, use_special=True)}")
