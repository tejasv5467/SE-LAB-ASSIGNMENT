import pytest
from hypothesis import given, strategies as st
from house_painting_quote_parser import clean_colour_name, room_area, total_wall_area


@given(st.text() | st.none())
def test_clean_colour_name_no_crash(s):
    try:
        result = clean_colour_name(s)
    except Exception as exc:
        pytest.fail(f"clean_colour_name crashed on {s!r}: {exc}")
    assert isinstance(result, str)


@given(st.text() | st.none())
def test_room_area_no_crash(s):
    try:
        result = room_area(s)
    except Exception as exc:
        pytest.fail(f"room_area crashed on {s!r}: {exc}")
    assert isinstance(result, int)
    assert result >= 0


@given(st.text() | st.none())
def test_total_wall_area_no_crash(s):
    try:
        result = total_wall_area(s)
    except Exception as exc:
        pytest.fail(f"total_wall_area crashed on {s!r}: {exc}")
    assert isinstance(result, int)
    assert result >= 0


@pytest.mark.parametrize("value, expected", [
    (" Ocean Blue ", "ocean_blue"), ("", ""), (None, "")
])
def test_colour_examples(value, expected):
    assert clean_colour_name(value) == expected


@pytest.mark.parametrize("value, expected", [
    ("12x10", 120), (" 12 X 10 ", 120), ("", 0),
    ("12x", 0), ("1x2x3", 0), ("-2x5", 0), (None, 0)
])
def test_room_examples(value, expected):
    assert room_area(value) == expected


@pytest.mark.parametrize("value, expected", [
    ("120;95;110", 325), (" 10 ; 20 ", 30),
    ("", 0), ("10;;20", 0), ("10;bad", 0), (None, 0)
])
def test_wall_examples(value, expected):
    assert total_wall_area(value) == expected
