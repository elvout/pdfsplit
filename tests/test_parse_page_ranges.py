import pytest
from pdfsplit.console_main import parse_page_ranges


@pytest.mark.parametrize("offset", [0, 5])
def test_all_complete_intervals(offset: int) -> None:
    EXPECTED_0: list[tuple[int, int]] = [
        (0, 14),
        (24, 130),
        (130, 157),
        (199, 200),
        (249, 322),
    ]

    PAGEFILE = "tests/resources/pagefiles/all_complete_intervals.txt"
    page_ranges = parse_page_ranges(PAGEFILE, offset)

    assert len(page_ranges) == len(EXPECTED_0)
    for i in range(len(EXPECTED_0)):
        assert EXPECTED_0[i][0] + offset == page_ranges[i][0]
        assert EXPECTED_0[i][1] + offset == page_ranges[i][1]


@pytest.mark.parametrize("offset", [0, 5])
def test_all_singleton(offset: int) -> None:
    EXPECTED_0: list[tuple[int, int]] = [
        (0, 14),
        (14, 31),
        (31, 51),
        (51, 75),
        (75, 98),
        (98, 123),
    ]

    PAGEFILE = "tests/resources/pagefiles/all_singleton.txt"
    page_ranges = parse_page_ranges(PAGEFILE, offset)

    assert len(page_ranges) == len(EXPECTED_0)
    for i in range(len(EXPECTED_0)):
        assert EXPECTED_0[i][0] + offset == page_ranges[i][0]
        assert EXPECTED_0[i][1] + offset == page_ranges[i][1]


@pytest.mark.parametrize("offset", [0, 5])
def test_mixed(offset: int) -> None:
    EXPECTED_0: list[tuple[int, int]] = [
        (2, 12),
        (12, 37),
        (38, 148),
        (148, 186),
        (190, 236),
        (236, 277),
    ]

    PAGEFILE = "tests/resources/pagefiles/mixed.txt"
    page_ranges = parse_page_ranges(PAGEFILE, offset)

    assert len(page_ranges) == len(EXPECTED_0)
    for i in range(len(EXPECTED_0)):
        assert EXPECTED_0[i][0] + offset == page_ranges[i][0]
        assert EXPECTED_0[i][1] + offset == page_ranges[i][1]
