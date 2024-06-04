# Copyright (c) 2016-2024 Martin Donath <martin.donath@squidfunk.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

from __future__ import annotations

import posixpath
import re

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import File, Files
from mkdocs.structure.pages import Page
from re import Match

# -----------------------------------------------------------------------------
# Hooks
# -----------------------------------------------------------------------------


# @todo
def on_page_markdown(markdown: str, *, page: Page, config: MkDocsConfig, files: Files):

    # Replace callback
    def replace(match: Match):
        type, args = match.groups()
        args = args.strip()
        if type == "version":
            return _badge_for_version(args, page, files)
        elif type == "sponsors":
            return _badge_for_sponsors(args, page, files)
        elif type == "moved":
            return _badge_for_moved(args, page, files)
        elif type == "experimental":
            return _badge_for_experimental(args, page, files)
        elif type == "locked":
            return _badge_for_locked(args, page, files)

        # Otherwise, raise an error
        raise RuntimeError(f"Unknown shortcode: {type}")

    # Find and replace all external asset URLs in current page
    return re.sub(r"<!-- md:(\w+)(.*?) -->", replace, markdown, flags=re.I | re.M)


# -----------------------------------------------------------------------------


# Resolve path of file relative to given page - the posixpath always includes
# one additional level of `..` which we need to remove
def _resolve_path(path: str, page: Page, files: Files):
    path, anchor, *_ = f"{path}#".split("#")
    try:
        file: File | None = files.get_file_from_path(path)
        if path:
            assert file
            path = _resolve(file, page)
        else:
            raise FileNotFoundError
    except:
        print(f"\033[33mWARNING\033[0m -  Failed to resolve path: {path}")
    return "#".join([path, anchor]) if anchor else path


# Resolve path of file relative to given page - the posixpath always includes
# one additional level of `..` which we need to remove
def _resolve(file: File, page: Page):
    path = posixpath.relpath(file.src_uri, page.file.src_uri)
    return posixpath.sep.join(path.split(posixpath.sep)[1:])


# -----------------------------------------------------------------------------


# Create badge
def _badge(icon: str, text: str = "", type: str = ""):
    classes = f"mdx-badge mdx-badge--{type}" if type else "mdx-badge"
    return "".join(
        [
            f'<span class="{classes}">',
            *([f'<span class="mdx-badge__icon">{icon}</span>'] if icon else []),
            *([f'<span class="mdx-badge__text">{text}</span>'] if text else []),
            f"</span>",
        ]
    )


# Create sponsors badge
def _badge_for_sponsors(text: str, page: Page, files: Files):
    icon = "material-heart"
    href = _resolve_path("about/sponsor.md", page, files)
    return _badge(icon=f"[:{icon}:]({href} '仅限赞助商')", type="heart", text=text)


# Create badge for version
def _badge_for_version(text: str, page: Page, files: Files):
    icon = "material-tag-outline"
    href = _resolve_path("about/symbols.md#version", page, files)
    return _badge(icon=f"[:{icon}:]({href} '版本')", text=text)


# Create badge for experimental flag
def _badge_for_experimental(text: str, page: Page, files: Files):
    icon = "material-flask-outline"
    href = _resolve_path("about/symbols.md#experimental", page, files)
    return _badge(icon=f"[:{icon}:]({href} '实验性')", text=text)


# Create badge for locked flag
def _badge_for_locked(text: str, page: Page, files: Files):
    icon = "material-lock-outline"
    href = _resolve_path("about/symbols.md#locked", page, files)
    return _badge(icon=f"[:{icon}:]({href} '不公开')", text=text)


# Create badge for moved flag
def _badge_for_moved(text: str, page: Page, files: Files):
    icon = "material-arrow-u-right-top"
    href = _resolve_path("about/symbols.md#moved", page, files)
    return _badge(icon=f"[:{icon}:]({href} '已转移')", text=text)
