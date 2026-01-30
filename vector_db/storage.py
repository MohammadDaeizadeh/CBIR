import numpy as np
import json
import os


class vector_db:
    def __init__(self, vector_path, meta_path):
        self.vector_path = vector_path
        self.meta_path = meta_path

        if os.path.exists(vector_path):
            self.vector_path = np.load(vector_path, allow_pickle=True).item()
        else:
            self.vector_path = {}

        if os.path.exists(meta_path):
            with open(meta_path, 'r') as f:
                self.meta_path = json.load(f)
        else:
            self.meta_path = {}

    def save(self):
        np.save(self.vector_path, self.vector_path)
        with open(self.meta_path, 'w') as f:
            json.dump(self.meta_path, f)

    def insert(self, id, vector, meta):
        self.vector_path[id] = vector
        self.meta_path[id] = meta

    def get(self, id):
        return self.vector_path.get(id), self.meta_path.get(id)

    def delete(self, id):
        self.vector_path.pop(id, None)
        self.meta_path.pop(id, None)
        self.save()