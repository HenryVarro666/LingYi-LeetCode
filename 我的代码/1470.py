class Solution:
    def shuffle(self, nums: List[int], n: int) -> List[int]:
        # 创建一个长度为 2 * n，所有元素都是 0 的列表
        ans = [0] * (2 * n)
        for i in range (n):
            ans[2*i] = nums[i]
            ans[2*i + 1] = nums[n + i]
        return ans