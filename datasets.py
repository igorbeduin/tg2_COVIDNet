from abc import ABC, abstractmethod

class Datasets(ABC):
    def __init__(self):
        super().__init__()
        self.count = 0

    def read(self):
        return count