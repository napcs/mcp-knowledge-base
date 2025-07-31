from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import *
import glob, os

from .types import MarkdownResource
from .utils import uri2path, path2uri
from .config import VAULT_PATH

from mcp.server.fastmcp.server import logger

class ObsidianVaultServer:
    def __init__(self):
        self.app = FastMCP("obsidian-vault")

        self.resource_map = {}

        self._init_resources()
        self._init_tools()

    def _init_resources(self):
        file_list = glob.glob(os.path.join(VAULT_PATH, '*/*/*.md'))

        self.resource_map = {}
        for path in file_list:
            # Use relative path for vault portability
            relative_path = os.path.relpath(path, start=VAULT_PATH)
            uri = f"file:///{path2uri(relative_path)}"

            rsrc = MarkdownResource(
                uri=uri, #! It converts the whitespace to %20
                name=os.path.basename(path).split('.')[0],
                mime_type="text/markdown",
                size=os.path.getsize(path)
            )
            # Store using decoded URI for consistent lookup
            decoded_uri = uri2path(uri)
            self.resource_map[decoded_uri] = rsrc
            self.app.add_resource(rsrc)

    def _init_tools(self):

        @self.app.tool()
        async def list_docs() -> list[dict[str, str]]:
            '''List the names and URIs of all docs written in the the vault
            '''
            return [{'name':rsrc.name, 'uri':rsrc.uri, 'size':rsrc.size} for rsrc in self.resource_map.values()]

        @self.app.tool()
        async def get_doc_by_uri(uri:str) -> str:
            '''get contents of the docs resource by uri
            '''
            # Use uri2path for consistent URI handling
            decoded_uri = uri2path(uri)
            rsrc = self.resource_map.get(decoded_uri, None)
            if not rsrc:
                raise ValueError(f"Not a registered resource URI")

            return await rsrc.read()

    def run(self):
        self.app.run(transport='stdio')

