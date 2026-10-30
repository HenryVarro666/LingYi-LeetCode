# 167
class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        left = 0
        right = len(numbers) - 1
        while left < right:
            s = numbers[left] + numbers[right]
            if s == target:
                return [left + 1, right + 1]
            if s > target:
                right -= 1
            else:
                left += 1


class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        left = 0
        right = len(numbers) - 1
        while left < right:
            s = numbers[left] + numbers[right]
            if s == target:
                break
            if s > target:
                right -= 1
            else:
                left += 1
        return [left + 1, right + 1]

# 15
class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        nums.sort()
        ans = []
        n = len(nums)
        for i in range(n - 2):
            x = nums[i]
            if i > 0 and x == nums[i-1]:
                continue
            j = i + 1
            k = n - 1
            while j < k:
                s = x + nums[j] + nums[k]
                if s > 0:
                    k -= 1
                elif s < 0:
                    j += 1
                else:
                    ans.append([x, nums[j],nums[k]])
                    j += 1
                    while j < k and nums[j] == nums[j-1]:
                        j += 1
                    k -= 1
                    while k > j and nums[k] == nums[k+1]:
                        k -= 1
        return ans                


class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        nums.sort()
        ans = []
        n = len(nums)
        for i in range(n-2):
            x = nums[i]
            if i > 0 and x == nums[i-1]:
                continue
            if x + nums[i+1] + nums[i+2] > 0:
                break
            if x + nums[-2] + nums[-1] < 0:
                continue
            j = i + 1
            k = n - 1
            while j < k:
                s = x + nums[j] + nums[k]
                if s > 0:
                    k -= 1
                elif s < 0:
                    j += 1
                else:
                    ans.append([x, nums[j], nums[k]])
                    j += 1
                    while j < k and nums[j] == nums[j - 1]:
                        j += 1
                    k -= 1
                    while k > j and nums[k] == nums[k+1]:
                        k -= 1
        return ans
                
