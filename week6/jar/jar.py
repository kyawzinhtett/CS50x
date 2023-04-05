class Jar:
    def __init__(self, capacity=12):
        if capacity < 0:
            raise ValueError("Capacity must be a non-negative integer")
        self._capacity = capacity
        self._cookies = 0

    def __str__(self):
        return self._cookies * "🍪"

    def deposit(self, n):
        if (n > self.capacity) or (self._cookies + n > self.capacity):
            raise ValueError("Not enough room in the jar")
        self._cookies += n

    def withdraw(self, n):
        if self._cookies < n:
            raise ValueError("Not enough cookies in the jar")
        self._cookies -= n

    @property
    def capacity(self):
        return self._capacity

    @property
    def size(self):
        return self._cookies

def main():
    jar = Jar()
    print(str(jar.capacity))
    jar.deposit(10)
    jar.withdraw(5)
    print(str(jar))

if __name__ == "__main__":
    main()