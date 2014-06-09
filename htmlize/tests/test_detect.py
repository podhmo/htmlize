import pytest
from htmlize.command import on_markdown, on_rest
candidates = [
    ["foo.rst", on_rest],
    ["FOO.RST", on_rest],
    ["foo.rest", on_rest],
    ["foo.md", on_markdown],
    ["foo.markdown", on_markdown]
]


@pytest.mark.parametrize("filename, fn", candidates)
def test_detect(filename, fn):
    from htmlize.command import detect
    assert detect(filename) == fn


candidates2 = [
    "foo.doc",
]


@pytest.mark.parametrize("filename", candidates2)
def test_must_failt(filename):
    from htmlize.command import detect, NotSupport
    with pytest.raises(NotSupport):
        detect(filename)
