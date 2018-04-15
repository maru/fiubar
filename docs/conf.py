import os

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

extensions = []
templates_path = ['_templates']
source_suffix = ['.rst', '.md']
master_doc = 'index'
project = u'fiubar'
copyright = u'2008-2018, Maru Berezin'
version = '2.0.0'
release = '2.0.0'
exclude_trees = ['_build']
pygments_style = 'sphinx'
html_static_path = ['_static']
if not on_rtd:
    import sphinx_rtd_theme
    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
