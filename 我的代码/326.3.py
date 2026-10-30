class Solution:
    def isPowerOfThree(self, n: int) -> bool:
        return n > 0 and 1162261467 % n == 0
    

# 如果 n 是 3 的幂。由于任何 3 的幂都是 3 ^19 的因子，所以 3 ^19 mod n = 0。或者说 n 的某个倍数等于 3 ^ 19。
# 如果 n 不是 3 的幂。那么 n 必然有不等于 3 的质因子，所以 n 的倍数不可能等于 3 ^ 19
# 这个只含质因子 3 的数，所以 3 ^ 19 mod n != 0。


class Solution:
    def isPowerOfThree(self, n: int) -> bool:
        while n and n % 3 == 0:
            n //= 3
        return n == 1