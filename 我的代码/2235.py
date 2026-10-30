class Solution:
    def sum(self, num1: int, num2: int) -> int:
        return num1 + num2

# 力扣评测机对每个测试数据，都会重新创建一个 Solution 对象
print(Solution().sum(12, 5))   # 示例 1
print(Solution().sum(-10, 4))  # 示例 2