---
title: "1708. 长度为K的最大子数组"
aliases: ["yiduobo的每日leetcode 1708.长度为K的最大子数组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/620275608"
zhihu_id: "620275608"
zhihu_title: "yiduobo的每日leetcode 1708.长度为K的最大子数组"
question_id: "1708"
question: "长度为K的最大子数组"
problem_url: "https://leetcode.cn/problems/largest-subarray-length-k/"
created: "2023-04-08T01:38:19+08:00"
updated: "2023-04-08T01:38:19+08:00"
upvotes: 0
comments: 0
---

# 1708. 长度为K的最大子数组

> **[yiduobo的每日leetcode 1708.长度为K的最大子数组](https://zhuanlan.zhihu.com/p/620275608) · 知乎 · 2023-04-08 · 赞同 0**
> 力扣：[1708. 长度为K的最大子数组](https://leetcode.cn/problems/largest-subarray-length-k/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1708.长度为K的最大子数组

[力扣](https://leetcode.cn/problems/largest-subarray-length-k/)

由于数组中的数字各不相同，那么字典序最大的子数组必然就是以数组中最大值开头的子数组，不过在这里还需要注意子数组的长度必须达到k，因此这个开头的下标只能在0到n - k之间，这里的n是数组的长度。于是只需找出0到n - k直接最大值的下标start_pos，那么最终答案就是nums[start_pos : start_pos + k]。

最后附上python代码：

```python
class Solution(object):
    def largestSubarray(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: List[int]
        """

        start_pos = 0
        for index in range(1, len(nums) - k + 1):
            if nums[index] > nums[start_pos]:
                start_pos = index
            
        return nums[start_pos : start_pos + k]
```
