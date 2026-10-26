from {{package_name}} import analysis


def test_summarize():
    result = analysis.summarize([1, 2, 3])
    assert result["count"] == 3
    assert result["mean"] == 2.0
    assert result["min"] == 1
    assert result["max"] == 3


def test_summarize_empty():
    assert analysis.summarize([])["count"] == 0
