from bs4 import BeautifulSoup
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page


# Hook mkdocs `on_page_content`
def on_page_content(
    html: str, *, page: Page, config: MkDocsConfig, files: Files
) -> str | None:
    soup = BeautifulSoup(html, "lxml")

    # For elements with nobr attribute, remove <br> tags
    for element in soup.find_all(attrs={"nobr": True}):
        for br in element.find_all("br"):
            br.decompose()
        # Remove nobr attribute
        del element["nobr"]

    # For <nobr> tags, remove <br> and keep the content
    for nobr in soup.find_all("nobr"):
        for br in nobr.find_all("br"):
            br.decompose()
        # Remove <nobr> tag
        nobr.unwrap()

    return str(soup)
