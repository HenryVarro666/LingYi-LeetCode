---
title: "3738. 替换至多一个元素后最长非递减子数组"
aliases: ["yiduobo的每日leetcode 3738.替换至多一个元素后最长非递减子数组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/dynamic-programming", "题单/滑动窗口与双指针", "题单/动态规划", "题单/滑动窗口与双指针/六-分组循环", "题单/动态规划/六-状态机-DP", "题单/动态规划/七-其他线性-DP", "题单/动态规划/专题-前后缀分解"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1970883641824506172"
zhihu_id: "1970883641824506172"
zhihu_title: "yiduobo的每日leetcode 3738.替换至多一个元素后最长非递减子数组"
question_id: "3738"
question: "替换至多一个元素后最长非递减子数组"
problem_url: "https://leetcode.cn/problems/longest-non-decreasing-subarray-after-replacing-at-most-one-element/"
difficulty: "Medium"
rating: 1811
created: "2025-11-09T16:20:13+08:00"
updated: "2025-11-09T16:20:14+08:00"
upvotes: 2
comments: 0
---

# 3738. 替换至多一个元素后最长非递减子数组

> **[yiduobo的每日leetcode 3738.替换至多一个元素后最长非递减子数组](https://zhuanlan.zhihu.com/p/1970883641824506172) · 知乎 · 2025-11-09 · 赞同 2**
> 力扣：[3738. 替换至多一个元素后最长非递减子数组](https://leetcode.cn/problems/longest-non-decreasing-subarray-after-replacing-at-most-one-element/) · Medium · 灵茶山艾府：[三种方法：前后缀分解 / 分组循环 / 状态机 DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3738.替换至多一个元素后最长非递减子数组

[3738. 替换至多一个元素后最长非递减子数组 - 力扣（LeetCode）](https://leetcode.cn/problems/longest-non-decreasing-subarray-after-replacing-at-most-one-element/description/)

题目给出一个整数数组nums。

现在可以执行一次替换操作，将数组中的一个元素替换为任意整数。问执行至多一次替换操作后，可以得到的最长非递减子数组的长度。

由于本题需要计算的是最长的非递减子数组，因此可以先通过一趟遍历，将原始数组切分成若干段尽可能长的非递减子数组。

若仅有一个子数组，说明整个数组本来就是单调不减的，可以直接返回数组的长度。

反之，则需要通过修改元素来获取更长的子数组。对于划分出来的每个子数组，将其左侧或者右侧的第一个元素修改成更小或者更大的元素，一定能让这个子数组变长，因此对于每个子数组[x, y]，都可以使用其长度再加上1，即y - x + 2来更新答案。另一方面，如果通过修改某个元素可以将其中两个连续的子数组连接起来，那么也可以用这两个子数组长度之和来更新答案。

在这里有一个隐藏条件是通过一次修改，不可能将三个子数组连接起来。

不妨设这三个连续子数组的边界分别为[x1, y1]、[x2, y2]、[x3, y3]，那么就有nums[y1] > nums[x2]，且nums[y2] > nums[x3]。

若中间子数组的长度大于1，即y2 > x2，那么仅通过一次修改，不可能同时逆转nums[y1] > nums[x2]与nums[y2] > nums[x3]，也就是说不可能连接三个子数组。

若中间子数组的长度等于1，即y2 \= x2，那么就有nums[y1] > nums[x2] > nums[x3]。这里有三组大于关系，仅修改其中一个元素，最多只能影响其中的两组，另一组大于关系无法逆转，因此也不可能连接三个子数组。

在明确了一次修改最多只能连接两个子数组之后，就只需要一趟遍历，检测能否通过修改元素，让相邻的子数组连接起来。具体来说，对于两个连续的子数组[x1, y1]以及[x2, y2]，在这里需要检测是否可以通过修改nums[y1]或者nums[x2]，让两个子数组连接起来。在这里无需考虑长度为1的子数组，因为这种情况在初始化答案的时候已经考虑过了，因此在这里只需检测当y1 > x1时，将nums[y1]修改为nums[y1 - 1]是否小于等于nums[x2]，或者当x2 \< y2时，将nums[x2]修改为nums[x2 + 1]是否大于等于nums[y1]即可，若满足以上两个条件之一，那么就说明可以连接两个子数组，此时应该使用合并后的子数组长度，即y2 - x1 + 1更新答案。

最后附上python代码：

```python
class Solution(object):
    def longestSubarray(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        parts = []
        p = 0
        while p < len(nums):
            q = p + 1
            while q < len(nums) and nums[q] >= nums[q - 1]:
                q += 1
            parts.append([p, q - 1])
            p = q
        
        if len(parts) == 1:
            return len(nums)
    
        x1, y1 = parts[0]
        res = y1 - x1 + 2
        for x2, y2 in parts[1:]:
            res = max(res, y2 - x2 + 2)
            if (y1 > x1 and nums[y1 - 1] <= nums[x2]) or (x2 < y2 and nums[x2 + 1] >= nums[y1]):
                res = max(res, y2 - x1 + 1)
            x1, y1 = x2, y2

        return res
```
