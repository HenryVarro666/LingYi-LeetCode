---
title: "2134. 最少交换次数来组合所有的1 II"
aliases: ["yiduobo的每日leetcode 2134.最少交换次数来组合所有的1 II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/一-定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/527532412"
zhihu_id: "527532412"
zhihu_title: "yiduobo的每日leetcode 2134.最少交换次数来组合所有的1 II"
question_id: "2134"
question: "最少交换次数来组合所有的 1 II"
problem_url: "https://leetcode.cn/problems/minimum-swaps-to-group-all-1s-together-ii/"
difficulty: "Medium"
rating: 1748
created: "2022-06-11T21:16:26+08:00"
updated: "2022-06-11T21:16:26+08:00"
upvotes: 0
comments: 0
---

# 2134. 最少交换次数来组合所有的1 II

> **[yiduobo的每日leetcode 2134.最少交换次数来组合所有的1 II](https://zhuanlan.zhihu.com/p/527532412) · 知乎 · 2022-06-11 · 赞同 0**
> 力扣：[2134. 最少交换次数来组合所有的 1 II](https://leetcode.cn/problems/minimum-swaps-to-group-all-1s-together-ii/) · Medium · 灵茶山艾府：[定长滑动窗口（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2134.最少交换次数来组合所有的1 II

[力扣](https://leetcode.cn/problems/minimum-swaps-to-group-all-1s-together-ii/)

之前好像遇到过类似的问题，不过不需要考虑环形的情况。对于这个问题，不妨设数组中所有1的数量为k，那么最中所有的1会被聚集到一个长度为k的区间中，也就是说需要找到一个长度为k的区间，其中0的数量尽量少。这是一个典型的定长滑动窗口问题，按常规滑动窗口的处理方法来做就行了，在这里就不展开了。

另外，对于首尾相连的情况，既可以通过对数组长度取模后判断来处理，也可以将数组复制一份拼接在末尾然后按照没有环形数组的情况进行处理。

最后附上python代码：

```python
class Solution(object):
    def minSwaps(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        n = len(nums)
        s = sum(nums)
        nums.extend(nums)
        
        now = sum(nums[:s])
        res = s - now
        for index in range(s, n - 1 + s):
            now += nums[index] - nums[index - s]
            res = min(res, s - now)
        
        return res
```
