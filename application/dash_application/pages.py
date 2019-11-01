import importlib

prefix = 'application.dash_application.'

# Please create array of module names as string, one per page
# e.g., pagenames = ['myPage', 'myPage2']
pagenames = [
    'dash_multipage_index',
    'dash_multipage_1',
    'dash_multipage_2',
    'dash_multipage_3'
]

# Please do not edit this array
pages = []

# Please do not edit this loop
for name in pagenames:
    pages.append(importlib.import_module(prefix + name))
