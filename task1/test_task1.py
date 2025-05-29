import pytest

from solution import sum_two


@pytest.mark.parametrize('a, b, expected_result', [(1, 2, 3),
                                                   (2, 3, 5),
                                                   (-4, 5, 1)])
def test_valid_params(a, b, expected_result):
    assert sum_two(a, b) == expected_result


@pytest.mark.parametrize('expected_exception, a, b', [(TypeError, 2.4, 3),
                                                      (TypeError, '3', 5),
                                                      (TypeError, [5], 9)])
def test_invalid_params(expected_exception, a, b):
    with pytest.raises(expected_exception):
        sum_two(a, b)
