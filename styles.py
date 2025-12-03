"""
Response Style Templates
========================
Rotating response styles for the YG Gentleman Bot.
Each style has a unique personality while maintaining the refined tone.
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
            'Ahem, if one may... a gentleman would say: "{correction}"',
            'Pardon the interruption, but might one suggest: "{correction}"',
            'If one may be so bold... the refined expression is: "{correction}"',
            'A gentle word, dear sir... perhaps: "{correction}"',
        ]
    },

    # Style B - The Professor (Educational)
    {
        "name": "The Professor",
        "templates": [
            'A note on etiquette, dear sir: "{correction}" is the preferred phrasing.',
            'For one\'s edification: the gentlemanly expression is "{correction}"',
            'A linguistic refinement, if one may: "{correction}"',
            'The distinguished vernacular would be: "{correction}"',
        ]
    },

    # Style C - The Mentor (Encouraging)
    {
        "name": "The Mentor",
        "templates": [
            'Almost there, good sir. Perhaps try: "{correction}"',
            'One shows promise. The refined alternative: "{correction}"',
            'A gentleman in training! Consider: "{correction}"',
            'Splendid effort. Might one suggest: "{correction}"',
        ]
    },

    # Style D - The Aristocrat (Playful)
    {
        "name": "The Aristocrat",
        "templates": [
            'Good heavens! Might one suggest: "{correction}"',
            'I say! A gentleman would phrase it thus: "{correction}"',
            'Gracious me! The proper expression: "{correction}"',
            'Heavens above! One means to say: "{correction}"',
        ]
    },

    # Style E - The Connoisseur (Refined)
    {
        "name": "The Connoisseur",
        "templates": [
            'A distinguished gentleman would phrase it thus: "{correction}"',
            'The mark of refinement: "{correction}"',
            'For the discerning gentleman: "{correction}"',
            'The cultivated expression: "{correction}"',
        ]
    },

    # Style F - The Elder (Wise)
    {
        "name": "The Elder",
        "templates": [
            'In refined circles, one says: "{correction}"',
            'The wisdom of gentlemen dictates: "{correction}"',
            'As the distinguished elders would say: "{correction}"',
            'Time-honoured refinement suggests: "{correction}"',
        ]
    },

    # Style G - The Diplomat (Gracious)
    {
        "name": "The Diplomat",
        "templates": [
            'Might one offer a suggestion? "{correction}"',
            'With the utmost respect: "{correction}"',
            'One ventures to propose: "{correction}"',
            'If one might be so gracious: "{correction}"',
        ]
    },

    # Style H - The Steward (Helpful)
    {
        "name": "The Steward",
        "templates": [
            'The proper expression, dear fellow: "{correction}"',
            'Allow me to assist: "{correction}"',
            'For your consideration: "{correction}"',
            'A refinement, if you please: "{correction}"',
        ]
    },
]

# Special occasion responses (used rarely for variety)
SPECIAL_RESPONSES = [
    'Ah, the transformation continues! "{correction}"',
    'From YN to YG, one step at a time: "{correction}"',
    'The gentleman emerges: "{correction}"',
    'Quarter-zip energy dictates: "{correction}"',
    'Matcha-sipping wisdom: "{correction}"',
    'Black excellence refined: "{correction}"',
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
