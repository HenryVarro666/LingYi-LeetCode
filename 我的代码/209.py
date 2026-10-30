# 在 while 循环结束后更新答案
class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        n = len(nums)
        ans = n+1 # 也可以写 inf
        s = left = 0
        for right, x in enumerate(nums):
            s += x
            while s - nums[left] >= target: # 尽量缩小子数组长度
                s -= nums[left]
                left += 1
            if s >= target:
                ans = min(ans, right-left+1) # 当left=right，子数组的长度为1
        return ans if ans <= n else 0

# 在 while 循环内更新答案
class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        n = len(nums)
        ans = inf
        s = left = 0
        for right, x in enumerate(nums):
            s += x
            while s >= target:
                ans = min(ans, right - left + 1)
                s -= nums[left]
                left += 1
        return ans if ans <= n else 0