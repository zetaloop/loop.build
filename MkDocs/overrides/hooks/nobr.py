from bs4 import BeautifulSoup
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.pages import Page


# Hook mkdocs `on_post_page`
def on_post_page(output: str, *, page: Page, config: MkDocsConfig) -> str | None:
    soup = BeautifulSoup(output, "html5lib")

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
