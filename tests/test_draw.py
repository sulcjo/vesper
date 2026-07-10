from engine import draw


def test_sky_places_stars_by_magnitude():
    lines = draw.render_sky([(2, 1, 1), (5, 1, 3)], width=10, height=3)
    row = lines[2]  # border + row 0 + row 1
    assert row[3] == "*"  # x=2 plus left border
    assert row[6] == "·"


def test_sky_dimensions_include_border():
    lines = draw.render_sky([], width=10, height=3)
    assert len(lines) == 5
    assert all(len(line) == 12 for line in lines)


def test_absent_region_erases_stars_and_grain():
    stars = [(4, 2, 1)]
    plain = draw.render_sky(stars, width=20, height=6)
    holed = draw.render_sky(stars, width=20, height=6, absent=(3, 1, 8, 4))
    assert "*" in plain[3]
    assert "*" not in holed[3]
    hole_rows = [line[4:10] for line in holed[2:6]]
    assert all(chunk == "      " for chunk in hole_rows)


def test_absent_region_breaks_the_border_where_it_touches():
    lines = draw.render_sky([], width=20, height=6, absent=(5, 0, 9, 3))
    assert lines[0][6:11] == "     "
    assert lines[0][1:6] == "─────"


def test_strip_renders_and_clamps_levels():
    assert draw.render_strip([0, 1, 4, 8]) == " ▁▄█"
    assert draw.render_strip([-3, 12]) == " █"


def test_gauge_renders_fraction():
    line = draw.render_gauge("GENERATOR", 0.5, width=10)
    assert "█████░░░░░" in line
    assert line.endswith(" 50%")


def test_page_wraps_long_lines_inside_border():
    page = draw.render_page(["word " * 30], width=20)
    assert all(len(line) == 24 for line in page)
    assert page[0].startswith("┌") and page[-1].startswith("└")


def test_erase_words_is_deterministic_and_leaves_original_alone():
    text = "the tea was cold before i finished it"
    once = draw.erase_words(text, 0.3, seed=7)
    twice = draw.erase_words(text, 0.3, seed=7)
    other = draw.erase_words(text, 0.3, seed=8)
    assert once == twice
    assert draw.GONE_CHAR in once
    assert once != text
    assert other != once  # different seed erases different words


def test_erase_words_zero_fraction_is_identity():
    text = "nothing missing here"
    assert draw.erase_words(text, 0.0, seed=1) == text


def test_erase_words_survives_awkward_word_counts():
    # gcd-style cycling used to be able to loop forever; six words,
    # heavy fraction, many seeds.
    text = "one two three four five six"
    for seed in range(40):
        result = draw.erase_words(text, 0.9, seed=seed)
        assert draw.GONE_CHAR in result
