"""
password_generator
------------------
A small library for generating strong, random passwords.

Uses the `secrets` module (cryptographically secure) instead of `random`.
"""

import secrets
import string

LOWERCASE = string.ascii_lowercase
UPPERCASE = string.ascii_uppercase
DIGITS = string.digits
SYMBOLS = "!@#$%^&*()-_=+[]{};:,.<>?/"

AMBIGUOUS = "il1Lo0O"  # characters that look alike


def generate_password(
    length: int = 12,
    use_lowercase: bool = True,
    use_uppercase: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True,
    exclude_ambiguous: bool = False,
) -> str:
    """
    Generate a strong random password.

    Args:
        length: Number of characters (min 4, max 128).
        use_lowercase: Include a-z.
        use_uppercase: Include A-Z.
        use_digits: Include 0-9.
        use_symbols: Include punctuation.
        exclude_ambiguous: Remove characters like l, 1, O, 0.

    Returns:
        A randomly generated password string.

    Raises:
        ValueError: If length is out of range or no character set is selected.
    """
    if not isinstance(length, int):
        raise TypeError("length must be an integer")
    if length < 4 or length > 128:
        raise ValueError("length must be between 4 and 128")

    pools = []
    if use_lowercase:
        pools.append(LOWERCASE)
    if use_uppercase:
        pools.append(UPPERCASE)
    if use_digits:
        pools.append(DIGITS)
    if use_symbols:
        pools.append(SYMBOLS)

    if not pools:
        raise ValueError("At least one character set must be enabled")

    if exclude_ambiguous:
        pools = ["".join(c for c in p if c not in AMBIGUOUS) for p in pools]
        pools = [p for p in pools if p]  # drop any that became empty

    if length < len(pools):
        raise ValueError(
            f"length must be at least {len(pools)} to include all selected sets"
        )

    # Guarantee at least one char from each selected pool
    password_chars = [secrets.choice(pool) for pool in pools]

    # Fill the rest from the combined pool
    all_chars = "".join(pools)
    password_chars += [secrets.choice(all_chars) for _ in range(length - len(pools))]

    # Shuffle securely
    secrets.SystemRandom().shuffle(password_chars)

    return "".join(password_chars)


def generate_passphrase(word_count: int = 4, separator: str = "-") -> str:
    """
    Generate a memorable passphrase from random words.

    Args:
        word_count: Number of words (min 3, max 10).
        separator: String placed between words.

    Returns:
        A passphrase like "tiger-cloud-mango-river".
    """
    if word_count < 3 or word_count > 10:
        raise ValueError("word_count must be between 3 and 10")

    # A tiny built-in wordlist. Replace with a bigger one if you like.
    words = [
        "apple", "tiger", "cloud", "mango", "river", "stone", "light",
        "brave", "quick", "happy", "ocean", "forest", "silver", "golden",
        "thunder", "shadow", "rocket", "garden", "market", "sunset",
        "pepper", "banana", "orange", "purple", "yellow", "music",
        "pencil", "castle", "planet", "dragon", "falcon", "wizard",
    ]
    return separator.join(secrets.choice(words) for _ in range(word_count))


def password_strength(password: str) -> dict:
    """
    Estimate password strength.

    Returns a dict with score (0-4), label, and feedback.
    """
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Use at least 8 characters")

    if len(password) >= 12:
        score += 1
    else:
        feedback.append("12+ characters is much stronger")

    if any(c.islower() for c in password) and any(c.isupper() for c in password):
        score += 1
    else:
        feedback.append("Mix upper and lower case letters")

    if any(c.isdigit() for c in password):
        score += 1
    else:
        feedback.append("Add at least one number")

    if any(c in SYMBOLS for c in password):
        score += 1
    else:
        feedback.append("Add at least one symbol")

    score = min(score, 4)

    labels = ["Very Weak", "Weak", "Fair", "Strong", "Very Strong"]
    return {
        "score": score,
        "label": labels[score],
        "feedback": feedback or ["Great password!"],
    }