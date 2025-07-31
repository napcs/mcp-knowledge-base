import json

class Config:
    def __init__(self, data):
        self.data = data

    @classmethod
    def from_json(cls, path):
        with open(path) as fd:
            data = json.load(fd)

        return cls(data)

    def __getitem__(self, name):
        return self.data.get(name, None)

config = Config.from_json('config.json')
VAULT_PATH = config['VAULT_PATH']