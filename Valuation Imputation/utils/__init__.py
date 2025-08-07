# intentionally empty
"""
When you add __init__.py to a folder (like utils/), you're telling Python:
“This directory should be treated as a package — you can import from it.”
Without it (especially in older versions of Python), you wouldn't be able to do:
from utils.io import load_data

"""