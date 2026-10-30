class Solution:
    def peakIndexInMountainArray(self, arr: List[int]) -> int:
        left, right = 0, len(arr) - 2
        while left + 1 < right:
            mid = (left + right) // 2
            if arr[mid] > arr[mid + 1]:
                right = mid
            else: 
                left = mid 
        return right