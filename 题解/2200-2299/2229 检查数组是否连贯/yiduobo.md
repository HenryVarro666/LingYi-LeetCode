---
title: "2229. 检查数组是否连贯"
aliases: ["yiduobo的每日leetcode 2229.检查数组是否连贯"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/628134166"
zhihu_id: "628134166"
zhihu_title: "yiduobo的每日leetcode 2229.检查数组是否连贯"
question_id: "2229"
question: "检查数组是否连贯"
problem_url: "https://leetcode.cn/problems/check-if-an-array-is-consecutive/"
created: "2023-05-09T22:38:35+08:00"
updated: "2023-05-09T22:38:35+08:00"
upvotes: 0
comments: 0
---

# 2229. 检查数组是否连贯

> **[yiduobo的每日leetcode 2229.检查数组是否连贯](https://zhuanlan.zhihu.com/p/628134166) · 知乎 · 2023-05-09 · 赞同 0**
> 力扣：[2229. 检查数组是否连贯](https://leetcode.cn/problems/check-if-an-array-is-consecutive/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2229.检查数组是否连贯

[力扣](https://leetcode.cn/problems/check-if-an-array-is-consecutive/)

首先，数组中不能出现相同的数字，因此可以将数组中的数都加入到集合中，若集合的长度与数组长度不同，那么说明存在重复元素，此时的答案为false。

接下来，若数组不重复且连贯，那么数组中的最大值与最小值之差必然为数组长度减1，那么只需检测数组最大值和最小值之差是否恰好等于数组长度减1即可。

最后附上python代码：

```python
class Solution(object):
    def isConsecutive(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """

        vis = set(nums)
        return max(nums) - min(nums) + 1 == len(vis) == len(nums)
```
