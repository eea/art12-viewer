# -*- coding: utf-8 -*-
import re
from decimal import Decimal
from markupsafe import Markup
from path import Path
from flask import current_app as app

patt = re.compile(r"(?<!\d)(\d+)(\.0*)?(?!\d)")


def str2num(s, default="", number_format="%.2f"):
    """Check if a string can be represented as integer"""
    if s is None:
        return default
    if isinstance(s, Decimal):
        buffer = number_format % s
    else:
        buffer = str(s)
    if buffer:
        return re.sub(patt, r"\1", buffer)
    else:
        return default


def inject_static_file(filepath):
    data = None
    with open(Path(app.static_folder) / filepath, "r") as f:
        data = f.read()
    return Markup(data)


# See: https://gist.github.com/berlotto/6295018
_slugify_strip_re = re.compile(r"[^\w\s-]")
_slugify_hyphenate_re = re.compile(r"[-\s]+")
_slugify_strip_multiple_spaces = re.compile(r"\s+")


def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.

    From Django's "django/template/defaultfilters.py".
    """
    import unicodedata

    if not value:
        return ""
    if not isinstance(value, str):
        value = str(value)
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    value = _slugify_strip_re.sub(" ", value).strip().lower()
    value = _slugify_strip_multiple_spaces.sub(" ", value)
    value = _slugify_hyphenate_re.sub("-", value)
    return value
