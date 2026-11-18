POINTS = {'0': 0, '15': 1, '30': 2, '40': 3}
MAX_GAMES_IN_SET = 7
MAX_DIGITS = 6  # caps input size so huge digit strings can't hit int() limits / DoS


def _to_non_negative_int(token, max_digits=MAX_DIGITS):
    """Return token as a non-negative int, or None if it isn't one.

    Only plain ASCII digits are accepted: str.isdigit() alone would let through
    characters like '²' that int() rejects, and int() alone would accept
    signs, underscores and non-ASCII digits.
    """
    token = token.strip()
    if not token or len(token) > max_digits:
        return None
    if not (token.isascii() and token.isdigit()):
        return None
    return int(token)


def _split_pair(text):
    """Split 'X-Y' into two stripped parts, or return None if malformed."""
    if not isinstance(text, str):
        return None
    parts = text.split('-')
    if len(parts) != 2:
        return None
    return parts[0].strip(), parts[1].strip()


def parse_score(text):
    """Parse 'A-B' points won into (a, b). Returns None for invalid input."""
    pair = _split_pair(text)
    if pair is None:
        return None
    a = _to_non_negative_int(pair[0])
    b = _to_non_negative_int(pair[1])
    if a is None or b is None:
        return None
    return a, b


def game_lead(text):
    """Return the point lead for a game score like '40-30'. None if invalid."""
    pair = _split_pair(text)
    if pair is None:
        return None
    first, second = pair
    if first not in POINTS or second not in POINTS:
        return None
    return POINTS[first] - POINTS[second]


def set_spread(games_csv):
    """Return max - min of games won per set ('6,4,7'). None if invalid."""
    if not isinstance(games_csv, str):
        return None
    games = []
    for token in games_csv.split(','):
        g = _to_non_negative_int(token, max_digits=1)
        if g is None or g > MAX_GAMES_IN_SET:
            return None
        games.append(g)
    return max(games) - min(games)


def main():
    print("==== Running parse_score ====")
    user_input = input("Enter points won as A-B (e.g. 3-2): ")
    result = parse_score(user_input)
    if result is None:
        print("Invalid input: expected two non-negative whole numbers like 3-2")
    else:
        print("Points A and B:", result)

    print("\n==== Running game_lead ====")
    user_input = input("Enter a game score (e.g. 40-30): ")
    result = game_lead(user_input)
    if result is None:
        print("Invalid input: each side must be one of 0, 15, 30, 40 (e.g. 40-30)")
    else:
        print("Lead in Points:", result)

    print("\n==== Running set_spread ====")
    user_input = input("Enter games won per set as CSV (e.g. 6,4,7): ")
    result = set_spread(user_input)
    if result is None:
        print("Invalid input: expected comma-separated games between 0 and 7")
    else:
        print("Spread:", result)


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nInput cancelled.")
