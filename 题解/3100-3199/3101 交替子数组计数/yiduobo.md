---
title: "3101. 交替子数组计数"
aliases: ["yiduobo的每日leetcode 3101.交替子数组计数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/dynamic-programming", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/699966765"
zhihu_id: "699966765"
zhihu_title: "yiduobo的每日leetcode 3101.交替子数组计数"
question_id: "3101"
question: "交替子数组计数"
problem_url: "https://leetcode.cn/problems/count-alternating-subarrays/"
difficulty: "Medium"
created: "2024-05-27T00:08:51+08:00"
updated: "2024-05-27T00:08:51+08:00"
upvotes: 1
comments: 0
---

# 3101. 交替子数组计数

> **[yiduobo的每日leetcode 3101.交替子数组计数](https://zhuanlan.zhihu.com/p/699966765) · 知乎 · 2024-05-27 · 赞同 1**
> 力扣：[3101. 交替子数组计数](https://leetcode.cn/problems/count-alternating-subarrays/) · Medium · 灵茶山艾府：[ 简洁写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3101.交替子数组计数

[. - 力扣（LeetCode）](https://leetcode.cn/problems/count-alternating-subarrays/description/)

由于值相同的相邻元素不能划分到同一个子数组中，因此可以先根据值相同的相邻元素将数组划分成若干子数组，这样一来每个子数组中的元素就是01交替出现的。

接下来对于一个长度为k的交替子数组，其中有k个长度为1的合法子数组，k - 1个长度为2的合法子数组，以此类推，也就是说这个长度为k的子数组中一共可以选出(k + 1) \* k / 2个合法的子数组，于是只需使用两个指针进行一趟遍历，一遍划分子数组一遍根据其长度更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def countAlternatingSubarrays(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        res = 0
        p = 0
        while p < len(nums):
            q = p + 1
            while q < len(nums) and nums[q] != nums[q - 1]:
                q += 1
            res += (q - p) * (q - p + 1) // 2
            p = q
        
        return res
```
