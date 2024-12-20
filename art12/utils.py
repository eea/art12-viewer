# -*- coding: utf-8 -*-
import re
from decimal import Decimal
from markupsafe import Markup
from path import Path
from flask import current_app as app

patt = re.compile(r"(?<!\d)(\d+)(\.0*)?(?!\d)")
valid_numeric = re.compile(
    r"^\s*"
    + "("
    + r"(\d\.)?\d+\s*-\s*(\d\.)?\d+"
    + r"|(>|>>|≈|<)?\s*((\d\.)?\d+)"
    + ")"
    + r"\s*$"
)
valid_ref = re.compile(
    r"^\s*"
    + "("
    + r"(\d\.)?\d+\s*-\s*(\d\.)?\d+"
    + r"|(>|>>|≈|<)?\s*((\d\.)?\d+)?|x"
    + ")"
    + r"\s*$"
)
empty_str = re.compile(r"^\s*$")


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


def str1num(s, default=""):
    return str2num(s, default=default, number_format="%.1f")


def parse_semicolon(s, sep="<br />"):
    """Replaces all semicolons found in the string ${s} with
    the given separator ${sep}"""
    if s is None:
        return s
    patt = re.compile(r";\s*")
    return patt.sub(sep, s)


def validate_field(s):
    """Checks if a field is a valid numeric or progress value"""
    if s:
        return bool(valid_numeric.match(s))
    return True


def validate_ref(s):
    """Checks if a field is a valid numeric or progress value"""
    if s:
        return bool(valid_ref.match(s))
    return True


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
