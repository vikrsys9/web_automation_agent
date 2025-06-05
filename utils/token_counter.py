class TokenCounter:
    def __init__(self):
        self.total = 0
    def add(self, text):
        self.total += max(1, len(text) // 4)
    def get_total(self):
        return self.total 