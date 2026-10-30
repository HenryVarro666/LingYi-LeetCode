# https://leetcode.cn/problems/find-first-and-last-position-of-element-in-sorted-array/solutions/1980196/er-fen-cha-zhao-zong-shi-xie-bu-dui-yi-g-t9l9/

# 闭区间写法
class Solution:
    # lower_bound 返回最小的满足 nums[i] >= target 的下标 i
    # 如果数组为空，或者所有数都 < target，则返回 len(nums)
    # 要求 nums 是非递减的，即 nums[i] <= nums[i + 1]
    def lower_bound(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums) - 1  # 闭区间 [left, right]
        while left <= right:  # 区间不为空
            # 循环不变量：
            # nums[left-1] < target
            # nums[right+1] >= target
            mid = (left + right) // 2
            if nums[mid] >= target:
                right = mid - 1  # 范围缩小到 [left, mid-1]
            else:
                left = mid + 1  # 范围缩小到 [mid+1, right]
        # 循环结束后 left = right+1
        # 此时 nums[left-1] < target 而 nums[left] = nums[right+1] >= target
        # 所以 left 就是第一个 >= target 的元素下标
        return left

    def searchRange(self, nums: List[int], target: int) -> List[int]:
        start = self.lower_bound(nums, target)
        if start == len(nums) or nums[start] != target:
            return [-1, -1]  # nums 中没有 target
        # 如果 start 存在，那么 end 必定存在
        end = self.lower_bound(nums, target + 1) - 1
        return [start, end]
    
# 左闭右开区间写法
class Solution:
    # lower_bound 返回最小的满足 nums[i] >= target 的下标 i
    # 如果数组为空，或者所有数都 < target，则返回 len(nums)
    # 要求 nums 是非递减的，即 nums[i] <= nums[i + 1]
    def lower_bound(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums)  # 左闭右开区间 [left, right)
        while left < right:  # 区间不为空
            # 循环不变量：
            # nums[left-1] < target
            # nums[right] >= target
            mid = (left + right) // 2
            if nums[mid] >= target:
                right = mid  # 范围缩小到 [left, mid)
            else:
                left = mid + 1  # 范围缩小到 [mid+1, right)
        # 循环结束后 left = right
        # 此时 nums[left-1] < target 而 nums[left] = nums[right] >= target
        # 所以 left 就是第一个 >= target 的元素下标
        return left

    def searchRange(self, nums: List[int], target: int) -> List[int]:
        start = self.lower_bound(nums, target)  # 选择其中一种写法即可
        if start == len(nums) or nums[start] != target:
            return [-1, -1]  # nums 中没有 target
        # 如果 start 存在，那么 end 必定存在
        end = self.lower_bound(nums, target + 1) - 1
        return [start, end]
    
# 开区间写法class Solution:
    # lower_bound 返回最小的满足 nums[i] >= target 的下标 i
    # 如果数组为空，或者所有数都 < target，则返回 len(nums)
    # 要求 nums 是非递减的，即 nums[i] <= nums[i + 1]
    def lower_bound(self, nums: List[int], target: int) -> int:
        left, right = -1, len(nums)  # 开区间 (left, right)
        while left + 1 < right:  # 区间不为空
            mid = (left + right) // 2
            # 循环不变量：
            # nums[left] < target
            # nums[right] >= target
            if nums[mid] >= target:
                right = mid  # 范围缩小到 (left, mid)
            else:
                left = mid  # 范围缩小到 (mid, right)
        # 循环结束后 left+1 = right
        # 此时 nums[left] < target 而 nums[right] >= target
        # 所以 right 就是第一个 >= target 的元素下标
        return right

    def searchRange(self, nums: List[int], target: int) -> List[int]:
        start = self.lower_bound(nums, target)  # 选择其中一种写法即可
        if start == len(nums) or nums[start] != target:
            return [-1, -1]  # nums 中没有 target
        # 如果 start 存在，那么 end 必定存在
        end = self.lower_bound(nums, target + 1) - 1
        return [start, end]
    

# 开区间写法
class Solution:
    # lower_bound 返回最小的满足 nums[i] >= target 的下标 i
    # 如果数组为空，或者所有数都 < target，则返回 len(nums)
    # 要求 nums 是非递减的，即 nums[i] <= nums[i + 1]
    def lower_bound(self, nums: List[int], target: int) -> int:
        left, right = -1, len(nums)  # 开区间 (left, right)
        while left + 1 < right:  # 区间不为空
            mid = (left + right) // 2
            # 循环不变量：
            # nums[left] < target
            # nums[right] >= target
            if nums[mid] >= target:
                right = mid  # 范围缩小到 (left, mid)
            else:
                left = mid  # 范围缩小到 (mid, right)
        # 循环结束后 left+1 = right
        # 此时 nums[left] < target 而 nums[right] >= target
        # 所以 right 就是第一个 >= target 的元素下标
        return right

    def searchRange(self, nums: List[int], target: int) -> List[int]:
        start = self.lower_bound(nums, target)  # 选择其中一种写法即可
        if start == len(nums) or nums[start] != target:
            return [-1, -1]  # nums 中没有 target
        # 如果 start 存在，那么 end 必定存在
        end = self.lower_bound(nums, target + 1) - 1
        return [start, end]
    
#############################################################

# # 闭区间
# def lower_bound(nums: List[int], target: int) -> int:
#     left = 0
#     right = len(nums) - 1 # 闭区间 [left, right]
#     while left <= right: # 区间不为空
#         # left + (right - left) // 2
#         # if nums[mid] < target:
#         if nums[mid] >= target:
#             mid = (left + right) // 2
#             left = mid + 1 # [mid + 1, right]
#         else:
#             right = mid -1 # [left, mid - 1]
#     return left

# # 左闭右开区间
# def lower_bound2(nums: List[int], target: int) -> int:
#     left = 0
#     right = len(nums) # 左闭右开区间 [left, right)
#     while left < right: # 区间不为空 while left <= (right - 1):
#         # left + (right - left) // 2
#         # if nums[mid] < target:
#         if nums[mid] >= target:
#             mid = (left + right) // 2
#             left = mid + 1 # [mid + 1, right)
#         else:
#             right = mid # [left, mid]
#     return left # right


# # 开区间
# def lower_bound3(nums: List[int], target: int) -> int:
#     left = -1
#     right = len(nums) # 开区间 (left, right)
#     while left + 1 < right: # 区间不为空
#         # left + (right - left) // 2
#         # if nums[mid] < target:
#         if nums[mid] >= target:
#             mid = (left + right) // 2
#             left = mid # (mid, right)
#         else:
#             right = mid # (left, mid]
#     return right 


# >= x ---> lower_bound(x) 
# > x ---> >=(x + 1) ---> lower_bound(x + 1) 
# < x ---> >=x - 1 ---> lower_bound(x) -1
# <= x ---> >x - 1 ---> (>=x+1) -1 ---> lower_bound(x + 1) - 1 
# 要想找到 ≤target 的最后一个数，无需单独再写一个二分。我们可以先找到这个数的右边相邻数字，也就是 >target 的第一个数。在所有数都是整数的前提下，>target 等价于 ≥target+1，这样就可以复用我们已经写好的二分函数了，即 lowerBound(nums, target + 1)，算出这个数的下标后，将其减一，就得到 ≤target 的最后一个数的下标。


# 问：怎么判断我写的是哪一种二分？
# 答：看 while 循环的条件，
#     如果是 left <= right，就是闭区间；
#     如果是 left < right，就是半闭半开区间；
#     如果是 left + 1 < right，就是开区间。