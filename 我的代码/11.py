class Solution:
    def maxArea(self, height: List[int]) -> int:
        left, right = 0, len(height) - 1
        res = 0
        while left < right:
            # [left, right] 之间的矩形面积
            cur_area = min(height[left], height[right]) * (right - left)
            res = max(res, cur_area)
            # 双指针技巧，移动较低的一边
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1
        return res