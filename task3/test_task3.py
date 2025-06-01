import pytest

from solution import appearance
import test_cases


@pytest.mark.parametrize('intervals, expected_result', [(test_cases.test_case1, 3117)])
def test_appearance(intervals, expected_result):
    assert appearance(intervals) == expected_result


@pytest.mark.parametrize('intervals, expected_result', [(test_cases.test_case2, 3577),
                                                        (test_cases.test_case3, 3565),
                                                        (test_cases.test_case4, 0),
                                                        (test_cases.test_case5, 0),
                                                        (test_cases.test_case6, 0),
                                                        (test_cases.test_case7, 0),
                                                        (test_cases.test_case8, 0),
                                                        (test_cases.test_case9, 30)])
def test_appearance_edge_cases(intervals, expected_result):
    assert appearance(intervals) == expected_result
