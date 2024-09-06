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

        # Find function by name str
        def get_func(name: str):
            if f"_badge_for_{name}" not in globals():
                raise RuntimeError(f"Unknown shortcode: {name}")
            return globals()[f"_badge_for_{name}"]

        groups = match.groups()
        if len(groups) == 2:
            type, args = groups
            text = args.strip()
            return get_func(type)(text, page, files)
        elif len(groups) == 3:
            type, href, args = groups
            text = args.strip()
            return get_func(type)(text, page, files, href)
        else:
            raise RuntimeError(f"Invalid number of groups: {len(groups)}")

    # Find and replace all external asset URLs in current page
    markdown = re.sub(r"<!-- md:(\w+)(.*?) -->", replace, markdown, flags=re.I | re.M)
    markdown = re.sub(
        r"<!-- \[md:(\w+)\]\((.*?)\)(.*?) -->", replace, markdown, flags=re.I | re.M
    )
    return markdown


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


def _badge_for_sponsors(
    text: str,
    page: Page,
    files: Files,
    href: str | None = None,
):
    icon = "material-heart"
    link = "about/sponsor.md"
    href = href or _resolve_path(link, page, files) + " '仅限赞助商'"
    return _badge(icon=f"[:{icon}:]({href})", type="heart", text=text)


def _badge_for_version(
    text: str,
    page: Page,
    files: Files,
    href: str | None = None,
):
    icon = "material-tag-outline"
    link = "about/symbols.md#version"
    href = href or _resolve_path(link, page, files) + " '版本'"
    return _badge(icon=f"[:{icon}:]({href})", text=text)


def _badge_for_experimental(
    text: str,
    page: Page,
    files: Files,
    href: str | None = None,
):
    icon = "material-flask-outline"
    link = "about/symbols.md#experimental"
    href = href or _resolve_path(link, page, files) + " '实验性'"
    return _badge(icon=f"[:{icon}:]({href})", text=text)


def _badge_for_locked(
    text: str,
    page: Page,
    files: Files,
    href: str | None = None,
):
    icon = "material-lock-outline"
    link = "about/symbols.md#locked"
    href = href or _resolve_path(link, page, files) + " '不公开'"
    return _badge(icon=f"[:{icon}:]({href})", text=text)


def _badge_for_moved(
    text: str,
    page: Page,
    files: Files,
    href: str | None = None,
):
    icon = "material-arrow-u-right-top"
    link = "about/symbols.md#moved"
    href = href or _resolve_path(link, page, files) + " '已转移'"
    return _badge(icon=f"[:{icon}:]({href})", text=text)


def _badge_for_closed(
    text: str,
    page: Page,
    files: Files,
    href: str | None = None,
):
    icon = "material-close"
    link = "about/symbols.md#closed"
    href = href or _resolve_path(link, page, files) + " '已停止'"
    return _badge(icon=f"[:{icon}:]({href})", text=text)


def _badge_for_autoupdate(
    text: str,
    page: Page,
    files: Files,
    href: str | None = None,
):
    icon = "material-autorenew"
    link = "about/symbols.md#autoupdate"
    href = href or _resolve_path(link, page, files) + " '自动更新'"
    return _badge(icon=f"[:{icon}:]({href})", text=text)
