from pathlib import Path
import sys

home_dir = Path(__file__).parent.parent.parent.absolute()
sys.path.insert(0, str(home_dir))

autodoc_mock_imports = [
    "geocoder",
    "pandas"
]

# -- Project information -----------------------------------------------------
project = 'utdf2gmns'
copyright = '2022-2023, Xiangyong Luo, Xuesong (Simon) Zhou'
author = 'Xiangyong Luo, Xuesong (Simon) Zhou'

# The full version, including alpha/beta/rc tags
release = '0.2.5'


extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon']  # 'sphinx.ext.napoleon'
root_doc = 'index'
language = 'en'
source_suffix = {'.rst': 'restructuredtext'}

# Add any paths that contain templates here, relative to this directory.
templates_path = []
html_static_path = []


# -- Options for EPUB output
epub_show_urls = 'footnote'
