"""Sphinx configuration for apc-hypaship."""

import sys
from importlib.metadata import version as _version
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / 'src'))

project = 'apc-hypaship'
author = 'paw'
release = _version('apc-hypaship')
version = release

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'sphinx_autodoc_typehints',
    'sphinxcontrib.autodoc_pydantic',
    'myst_parser',
    'sphinx_rtd_theme',
    'sphinx_rtd_dark_mode',
]

source_suffix = {'.rst': 'restructuredtext', '.md': 'markdown'}
myst_enable_extensions = ['colon_fence', 'deflist']
myst_heading_anchors = 3

autodoc_member_order = 'bysource'
autodoc_default_options = {'members': True, 'show-inheritance': True}
autodoc_pydantic_model_show_json = False
autodoc_pydantic_model_show_config_summary = False
autodoc_pydantic_settings_show_json = False
autodoc_pydantic_settings_show_config_summary = False
autodoc_pydantic_field_list_validators = False
autodoc_pydantic_model_member_order = 'bysource'

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'pydantic': ('https://docs.pydantic.dev/latest', None),
}

html_theme = 'sphinx_rtd_theme'
default_dark_mode = True
