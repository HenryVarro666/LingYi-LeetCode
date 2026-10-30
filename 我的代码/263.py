class Solution:
    def isUgly(self, n: int) -> bool:
        if n <= 0:
            return False
        while n % 3 == 0:
            n //= 3 
        while n % 5 ==0:
            n //= 5
        return n & (n-1) == 0
    


# a //= b
# a = a // b
# 一边做整除，一边更新变量