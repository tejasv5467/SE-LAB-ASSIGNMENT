"""Input-safe parsers for the house painting quote lab."""


def clean_colour_name(name):
    """Return a normalized colour code, or an empty string for invalid input."""
    if not isinstance(name, str):
        return ""
    return name.strip().lower().replace(" ", "_")


def room_area(text):
    """Return area for nonnegative integer LENGTHxWIDTH, otherwise 0."""
    if not isinstance(text, str):
        return 0
    parts = text.lower().split("x")
    if len(parts) != 2:
        return 0
    length, width = (part.strip() for part in parts)
    if not length.isascii() or not length.isdecimal():
        return 0
    if not width.isascii() or not width.isdecimal():
        return 0
    return int(length) * int(width)


def total_wall_area(text):
    """Sum semicolon-separated nonnegative whole-number areas; invalid input returns 0."""
    if not isinstance(text, str):
        return 0
    areas = [part.strip() for part in text.split(";")]
    if not all(part.isascii() and part.isdecimal() for part in areas):
        return 0
    return sum(int(part) for part in areas)


def main():
    print("==== Running clean_colour_name ====")
    value = input("Enter a paint colour name (e.g. Ocean Blue): ")
    print("Colour code:", clean_colour_name(value))

    print("\n==== Running room_area ====")
    value = input("Enter room size as LENGTHxWIDTH in feet (e.g. 12x10): ")
    print("Room area (sq ft):", room_area(value))

    print("\n==== Running total_wall_area ====")
    value = input("Enter wall areas separated by ; (e.g. 120;95;110): ")
    print("Total wall area (sq ft):", total_wall_area(value))


if __name__ == "__main__":
    main()
