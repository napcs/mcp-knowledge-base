
from urllib.parse import unquote

def uri2path(s):
    return unquote(s).lower()
