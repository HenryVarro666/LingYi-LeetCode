class Solution:
    def smallestEvenMultiple(self, n: int) -> int:
        return (n % 2 + 1) * n




class Solution:
    def smallestEvenMultiple(self, n: int) -> int:
        return n << (n & 1)
    

class Solution:
    def smallestEvenMultiple(self, n: int) -> int:
        return n if n % 2 == 0 else n * 2