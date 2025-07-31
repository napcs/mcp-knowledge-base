
from urllib.parse import unquote, quote

def uri2path(s):
    """Convert URI to file path, properly handling URL encoding/decoding"""
    return unquote(s)

def path2uri(path):
    """Convert file path to URI, properly handling URL encoding"""
    return quote(path, safe='/')  # Keep slashes unencoded for proper URI format
