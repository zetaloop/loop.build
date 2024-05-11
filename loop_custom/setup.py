from setuptools import setup, find_packages

setup(
    name="loop_custom",
    version="0",
    packages=find_packages(),
    entry_points={
        "mkdocs.plugins": [
            "loop_custom = loop_custom.plugin:FakePlugin",
        ]
    },
)
