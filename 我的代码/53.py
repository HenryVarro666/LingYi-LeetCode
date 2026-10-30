class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        ans = -inf
        min_pre_sum = pre_sum = 0
        for x in nums:
            pre_sum += x
            ans = max(ans, pre_sum - min_pre_sum)
            min_pre_sum = min(min_pre_sum, pre_sum)
        return ans
        

############
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        f = [0] * len(nums)
        f[0] = nums[0]
        for i in range(1,len(nums)):
            f[i] = max(f[i-1],0) + nums[i]
        return max(f)
        
###########
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        ans = -inf
        f = 0
        for x in nums:
            f = max(f,0) + x
            ans = max(ans, f)
        return ans
        


