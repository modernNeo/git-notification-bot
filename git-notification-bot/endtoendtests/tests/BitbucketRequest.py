import json


class BitbucketRequest:

    def __init__(self, file_path):
        f = json.load(open(file_path, 'r'))
        self.headers = f['headers']
        self.data = f['data']
