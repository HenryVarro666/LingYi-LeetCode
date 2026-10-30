#   range(start, stop, step) 的含义
#。  range(n - 2, -1, -1)
# 	•	start = n - 2：从第 n-2 个位置开始
# 	•	stop = -1：一直到 大于 -1 为止（不包含 -1）（stop 永远不会被取到（开区间））
# 	•	step = -1：每次减 1（倒着走）

# i = n - 2
# while i > -1:
#     print(i)
#     i -= 1

# 👉 所以整体意思是：
# 从右往左遍历数组（但不包括最后一个元素）


# ## 暴力解法
# class Solution:
#     def trap(self, height: List[int]) -> int:
#         n = len(height)
#         res = 0
#         for i in range(1, n - 1):
#             l_max, r_max = 0, 0
#             # 找右边最高的柱子
#             for j in range(i, n):
#                 r_max = max(r_max, height[j])
#             # 找左边最高的柱子
#             for j in range(i, -1, -1):
#                 l_max = max(l_max, height[j])
#             # 如果自己就是最高的话，
#             # l_max == r_max == height[i]
#             res += min(l_max, r_max) - height[i]
#         return res


## 备忘录解法
class Solution:
    def trap(self, height):
        if len(height) == 0:
            return 0
        n = len(height)
        res = 0
        # 数组充当备忘录
        l_max = [0] * n
        r_max = [0] * n
        # 初始化 base case
        l_max[0] = height[0]
        r_max[n - 1] = height[n - 1]
        # 从左向右计算 l_max
        for i in range(1, n):
            l_max[i] = max(height[i], l_max[i - 1])
        # 从右向左计算 r_max
        for i in range(n - 2, -1, -1):
            r_max[i] = max(height[i], r_max[i + 1])
        # 计算答案
        for i in range(1, n - 1):
            res += min(l_max[i], r_max[i]) - height[i]
        return res

## 双指针解法
class Solution:
    def trap(self, height: List[int]) -> int:
        left, right = 0, len(height) - 1
        l_max, r_max = 0, 0

        res = 0
        while left < right:
            l_max = max(l_max, height[left])
            r_max = max(r_max, height[right])

            # res += min(l_max, r_max) - height[i]
            if l_max < r_max:
                res += l_max - height[left]
                left += 1
            else:
                res += r_max - height[right]
                right -= 1
        return res
    
#########################################################

# 前后缀分解
class Solution:
    def trap(self, height: List[int]) -> int:
        n = len(height)
        pre_max = [0] * n
        pre_max[0] = height[0]
        for i in range(1,n):
            pre_max[i] = max(pre_max[i-1], height[i])
        
        suf_max = [0] * n
        suf_max[-1] = height[-1]
        for i in range(n-2, -1, -1):
            suf_max[i] = max(suf_max[i+1], height[i])

        ans = 0
        for h, pre, suf in zip(height, pre_max, suf_max):
            ans += min(pre, suf) - h
        return ans

# 相向双指针
class Solution:
    def trap(self, height: List[int]) -> int:
        n = len(height)
        ans = 0
        left = 0
        right = n - 1
        pre_max = 0
        suf_max = 0
        while left < right:
            pre_max = max(pre_max, height[left])
            suf_max = max(suf_max, height[right])
            if pre_max < suf_max:
                ans += pre_max - height[left]
                left += 1
            else:
                ans += suf_max - height[right]
                right -= 1
        return ans
    

class Solution:
    def trap(self, height: List[int]) -> int:
        pre = list(accumulate(height, max))
        suf = list(accumulate(height[::-1], max))[::-1]
        return sum(min(u, v) - x for u, v, x in zip(pre, suf, height))