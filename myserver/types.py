from mcp.server.fastmcp.resources import Resource
import os
import aiofiles

from .config import VAULT_PATH
from .utils import uri2path

class MarkdownResource(Resource):
    size: int = -1

    async def read(self) -> str | bytes:
        uri = uri2path(str(self.uri))
        
        if not uri.startswith("file://"):
            raise ValueError(f"Only file resource permits. got uri({uri})")
        
        path = uri[len('file://'):]
        file_path = os.path.join(VAULT_PATH, path)

        if not os.path.exists(file_path):
            raise ValueError(f"file_path({file_path}) not exists")
        
        async with aiofiles.open(file_path, 'r') as fd:
            contents = await fd.read()

        return contents