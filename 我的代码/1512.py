from collections import defaultdict

class Solution:
    def numIdenticalPairs(self, nums: List[int]) -> int:
        # 题目要求统计所有满足:
        # nums[i] == nums[j] 且 i < j 的数对个数
        
        ans = 0
        
        # defaultdict(int):
        # 等价于“默认值为 0 的字典”
        # 作用：访问不存在的 key 时，不会报错，而是自动返回 0
        cnt = defaultdict(int)
        
        for x in nums:  # 当前遍历到的 x 可以看作 nums[j]
            # cnt[x] 表示：在当前 x 之前，已经出现过多少个相同的 x
            #
            # 这些之前出现过的 x，都可以和当前 x 组成一对:
            # (前面的某个位置 i, 当前这个位置 j)
            # 并且天然满足 i < j
            #
            # 所以当前这一轮新增的好数对数量就是 cnt[x]
            ans += cnt[x]
            
            # 然后再把当前 x 计入出现次数
            cnt[x] += 1
        
        return ans

#################   
## Explanation:
## https://leetcode.cn/problems/number-of-good-pairs/solutions/3047641/python3-bu-bu-hua-jian-0ms-yi-dong-by-pe-epdo/

class Solution:
    def numIdenticalPairs(self, nums: List[int]) -> int:
        counter = [0 for _ in range(101)]
        product = 1
        fractorial_map = {0: 1}
        result = 0
        for i, num in enumerate(nums):
            product *= i + 1
            fractorial_map[i + 1] = product
            counter[num] += 1
        for count in counter:
            if count > 1:
                result += fractorial_map[count] // (2 * fractorial_map[count - 2])
        return result
    

class Solution:
    def numIdenticalPairs(self, nums: List[int]) -> int:
        counter = [0 for _ in range(101)]
        result = 0
        for num in nums:
            counter[num] += 1
        for count in counter:
            result += (count) * (count - 1) // 2
        return result
    
class Solution:
    def numIdenticalPairs(self, nums: List[int]) -> int:
        counter = [0 for _ in range(101)]
        result = 0
        for num in nums:
            result += counter[num]
            counter[num] += 1
        return result