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
            return _badge_for_sponsors(page, files)
        elif type == "flag":
            return flag(args, page, files)
        elif type == "option":
            return option(args)
        elif type == "setting":
            return setting(args)
        elif type == "example":
            return _badge_for_example(args, page, files)
        elif type == "default":
            if args == "none":
                return _badge_for_default_none(page, files)
            elif args == "computed":
                return _badge_for_default_computed(page, files)
            else:
                return _badge_for_default(args, page, files)
        elif type == "moved":
            return _badge_for_moved(args, page, files)

        # Otherwise, raise an error
        raise RuntimeError(f"Unknown shortcode: {type}")

    # Find and replace all external asset URLs in current page
    return re.sub(r"<!-- md:(\w+)(.*?) -->", replace, markdown, flags=re.I | re.M)


# -----------------------------------------------------------------------------
# Helper functions
# -----------------------------------------------------------------------------


# Create a flag of a specific type
def flag(args: str, page: Page, files: Files):
    type, *_ = args.split(" ", 1)
    if type == "experimental":
        return _badge_for_experimental(page, files)
    elif type == "required":
        return _badge_for_required(page, files)
    elif type == "locked":
        return _badge_for_locked(page, files)
    raise RuntimeError(f"Unknown type: {type}")


# Create a linkable option
def option(type: str):
    _, *_, name = re.split(r"[.:]", type)
    return f"[`{name}`](#+{type}){{ #+{type} }}\n\n"


# Create a linkable setting - @todo append them to the bottom of the page
def setting(type: str):
    _, *_, name = re.split(r"[.*]", type)
    return f"`{name}` {{ #{type} }}\n\n[{type}]: #{type}\n\n"


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
def _badge_for_sponsors(page: Page, files: Files):
    icon = "material-heart"
    href = _resolve_path("about/sponsor.md", page, files)
    return _badge(icon=f"[:{icon}:]({href} '仅限赞助商')", type="heart")


# Create badge for version
def _badge_for_version(text: str, page: Page, files: Files):
    icon = "material-tag-outline"
    href = _resolve_path("about/symbols.md#version", page, files)
    return _badge(icon=f"[:{icon}:]({href} '最小版本')", text=f"{text}")


# Create badge for example
def _badge_for_example(text: str, page: Page, files: Files):
    return "\n".join(
        [
            _badge_for_example_download(text, page, files),
            _badge_for_example_view(text, page, files),
        ]
    )


# Create badge for example view
def _badge_for_example_view(text: str, page: Page, files: Files):
    icon = "material-folder-eye"
    href = f"https://mkdocs-material.github.io/examples/{text}/"
    return _badge(icon=f"[:{icon}:]({href} 'View example')", type="right")


# Create badge for example download
def _badge_for_example_download(text: str, page: Page, files: Files):
    icon = "material-folder-download"
    href = f"https://mkdocs-material.github.io/examples/{text}.zip"
    return _badge(
        icon=f"[:{icon}:]({href} '下载示例')",
        text=f"[`.zip`]({href})",
        type="right",
    )


# Create badge for default value
def _badge_for_default(text: str, page: Page, files: Files):
    icon = "material-water"
    href = _resolve_path("about/symbols.md#default", page, files)
    return _badge(icon=f"[:{icon}:]({href} '默认值')", text=text)


# Create badge for empty default value
def _badge_for_default_none(page: Page, files: Files):
    icon = "material-water-outline"
    href = _resolve_path("about/symbols.md#default", page, files)
    return _badge(icon=f"[:{icon}:]({href} '默认值为空')")


# Create badge for computed default value
def _badge_for_default_computed(page: Page, files: Files):
    icon = "material-water-check"
    href = _resolve_path("about/symbols.md#default", page, files)
    return _badge(icon=f"[:{icon}:]({href} '默认值动态计算')")


# Create badge for required value flag
def _badge_for_required(page: Page, files: Files):
    icon = "material-alert"
    href = _resolve_path("about/symbols.md#required", page, files)
    return _badge(icon=f"[:{icon}:]({href} '必填')")


# Create badge for experimental flag
def _badge_for_experimental(page: Page, files: Files):
    icon = "material-flask-outline"
    href = _resolve_path("about/symbols.md#experimental", page, files)
    return _badge(icon=f"[:{icon}:]({href} '实验性')")


# Create badge for locked flag
def _badge_for_locked(page: Page, files: Files):
    icon = "material-lock-outline"
    href = _resolve_path("about/symbols.md#locked", page, files)
    return _badge(icon=f"[:{icon}:]({href} '不公开')")


# Create badge for moved flag
def _badge_for_moved(text: str, page: Page, files: Files):
    icon = "material-arrow-u-right-top"
    href = _resolve_path("about/symbols.md#moved", page, files)
    return _badge(icon=f"[:{icon}:]({href} '已转移')", text=text)
