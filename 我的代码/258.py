class Solution:
    def addDigits(self, num: int) -> int:
        return (num-1) % 9 + 1 if num else 0
    
        # if num != 0:
        #     return (num - 1) % 9 + 1
        # else:
        #     return 0

        
## 在 Python 中，if num 是 truthy 判断。对于整数来说，只有 0 是 False，其余都为 True，因此等价于 num != 0。

###

class Solution:
    def addDigits(self, num: int) -> int:
        while num >= 10:
            sum = 0
            while num:
                sum += num % 10
                num //= 10
            num = sum
        return num

