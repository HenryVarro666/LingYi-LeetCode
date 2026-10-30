class Solution:
    def subtractProductAndSum(self, n: int) -> int:
        prod, sum = 1, 0
        while n:
            prod *= n % 10
            sum += n % 10 
            n //= 10
        return prod - sum
    


## n % 10 取个位 取余数
## n // 10 去个位 整除（floor division）
