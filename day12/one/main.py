

class SafeIter(list):

    def __init__(self, vals: list[int]):
        super().__init__(vals)
        self.idx = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.idx < len(self):
            val = self[self.idx]
            self.idx += 1
        else:
            val = None
        
        return val



i = SafeIter([1, 2, 3])

[print(next(i)) for _ in range(5)]