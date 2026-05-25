"""data_cleaner.py v2 新增方法的全面测试。"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.data_cleaner import DataCleaner


# --- clean_html ----------------------------------------------------

def test_clean_html_strips_tags():
    assert DataCleaner.clean_html("<p>Hello <b>World</b></p>") == "Hello World"


def test_clean_html_handles_nested():
    text = "<div><p><b>A</b> <i>B</i></p></div>"
    out = DataCleaner.clean_html(text)
    assert "<" not in out
    assert "A" in out and "B" in out


def test_clean_html_decodes_entities():
    assert "&" in DataCleaner.clean_html("foo &amp; bar")
    assert " " in DataCleaner.clean_html("foo&nbsp;bar")


def test_clean_html_empty_safe():
    assert DataCleaner.clean_html("") == ""
    assert DataCleaner.clean_html(None) == ""


def test_clean_html_no_tags_passes_through():
    assert DataCleaner.clean_html("plain text") == "plain text"


def test_clean_html_collapses_whitespace():
    # 标签替换为空格后多空白合一
    assert DataCleaner.clean_html("<p>a</p>  <p>b</p>") == "a b"


# --- normalize -----------------------------------------------------

def test_normalize_collapses_internal_spaces():
    assert DataCleaner.normalize("Hello   World") == "Hello World"


def test_normalize_strips_outer():
    assert DataCleaner.normalize("  X  ") == "X"


def test_normalize_handles_newlines_tabs():
    assert DataCleaner.normalize("a\nb\tc") == "a b c"


def test_normalize_empty():
    assert DataCleaner.normalize("") == ""
    assert DataCleaner.normalize(None) == ""


def test_normalize_unicode_passes_through():
    assert DataCleaner.normalize("  中  文  ") == "中 文"


# --- remove_empty --------------------------------------------------

def test_remove_empty_basic():
    data = [
        {"title": "A", "content": "x"},
        {"title": "", "content": "x"},
        {"title": "C", "content": None},
    ]
    out = DataCleaner.remove_empty(data, fields=["title", "content"])
    assert len(out) == 1
    assert out[0]["title"] == "A"


def test_remove_empty_none_and_whitespace():
    data = [
        {"k": "value"},
        {"k": None},
        {"k": "   "},
        {"k": ""},
    ]
    out = DataCleaner.remove_empty(data, fields=["k"])
    assert len(out) == 1


def test_remove_empty_missing_field_treated_as_empty():
    data = [{"a": 1}, {"a": 2, "b": "x"}]
    out = DataCleaner.remove_empty(data, fields=["b"])
    assert len(out) == 1


def test_remove_empty_empty_input():
    assert DataCleaner.remove_empty([], fields=["x"]) == []


def test_remove_empty_all_fields_required():
    """所有指定字段都必须非空。"""
    data = [
        {"a": "x", "b": "y"},
        {"a": "x", "b": ""},
        {"a": "", "b": "y"},
    ]
    out = DataCleaner.remove_empty(data, fields=["a", "b"])
    assert len(out) == 1


# --- remove_duplicates with both modes ----------------------------

def test_remove_duplicates_dataframe_mode():
    """v1 行为：DataFrame + subset。"""
    df = pd.DataFrame({
        "a": [1, 1, 2], "b": ["x", "x", "y"],
    })
    cleaner = DataCleaner()
    out = cleaner.remove_duplicates(df)
    assert len(out) == 2


def test_remove_duplicates_dataframe_with_subset():
    df = pd.DataFrame({
        "url": ["a", "a", "b"], "title": ["X", "Y", "Z"],
    })
    cleaner = DataCleaner()
    out = cleaner.remove_duplicates(df, subset=["url"])
    assert len(out) == 2


def test_remove_duplicates_dict_mode_by_key():
    data = [
        {"url": "a", "title": "X"},
        {"url": "a", "title": "Y"},  # dup by url
        {"url": "b", "title": "Z"},
    ]
    cleaner = DataCleaner()
    out = cleaner.remove_duplicates(data, key="url")
    assert len(out) == 2
    # 应保留第一次出现
    assert out[0]["title"] == "X"


def test_remove_duplicates_dict_mode_no_key():
    """无 key → 按整个 dict 比较。"""
    data = [
        {"a": 1}, {"a": 1}, {"a": 2}, {"a": 1},
    ]
    cleaner = DataCleaner()
    out = cleaner.remove_duplicates(data)
    assert len(out) == 2


def test_remove_duplicates_invalid_type_raises():
    cleaner = DataCleaner()
    with pytest.raises(TypeError):
        cleaner.remove_duplicates("not a df or list")


# --- 静态方法可直接调（无需实例） ---------------------------------

def test_static_methods_callable_without_instance():
    assert DataCleaner.clean_html("<a>x</a>") == "x"
    assert DataCleaner.normalize(" x ") == "x"
    assert DataCleaner.remove_empty([{"x": None}], ["x"]) == []
