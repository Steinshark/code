class bigint:
    def __init__(self,n):

        self.container = [0 for i in n]
        self.len = len(n)
        for i in range(len(n)):
            self.container[i] = int(n[i])
    def __sub__(self,n):
        pass
    def __add__(self,n):
        if n > self:
            return -1
        larger = max(self.len,n.len)
        smaller = min(self.len,n.len)
        overflows = [0 for i in larger.len]
        diff = larger.len = smaller.len

        for index in larger.container:
            if index + smaller.len >= larger.len:
                sum = larger.container[i] + smaller.container[i+diff]


    def __gt__(self,n):
        if self.len > n.len:
            return self
        elif self.len == n.len:
            for i in range(self.len):
                if self.container[i] > n.container[i]:
                    return True
                elif self.container[i] == n.container[i]:
                    continue
                elif self.container[i] < n.container[i]:
                    return False
            return False

        elif self.len < n.len:
            return self


c = bigint('12343145235')
print(c.container)
