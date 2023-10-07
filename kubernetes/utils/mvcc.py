from collections import deque


class MVCC:

    def __init__(self, items=10):
        self.mvcc = {}
        for i in range(items):
            self.mvcc[str(i)] = deque(maxlen=2)
            self.mvcc[str(i)].append((0, 10))  # (versiom, value)