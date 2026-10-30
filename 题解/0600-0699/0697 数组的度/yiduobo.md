---
title: "697. 数组的度"
aliases: ["yiduobo的每日leetcode 697.数组的度"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/314251733"
zhihu_id: "314251733"
zhihu_title: "yiduobo的每日leetcode 697.数组的度"
question_id: "697"
question: "数组的度"
problem_url: "https://leetcode.cn/problems/degree-of-an-array/"
created: "2020-11-26T22:33:23+08:00"
updated: "2020-11-26T22:33:40+08:00"
upvotes: 0
comments: 0
---

# 697. 数组的度

> **[yiduobo的每日leetcode 697.数组的度](https://zhuanlan.zhihu.com/p/314251733) · 知乎 · 2020-11-26 · 赞同 0**
> 力扣：[697. 数组的度](https://leetcode.cn/problems/degree-of-an-array/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

697.数组的度

[力扣](https://leetcode-cn.com/problems/degree-of-an-array/)

题目要求从数组中找出最短的连续子数组，包含原数组中所有的某个数x，其中x满足其出现次数是原数组中最多的。于是我们可以统计每个数出现的次数以及第一次first和最后一次出现的位置last。统计完成后，可以得到出现次数最多的数有哪些，依次枚举其中的每一个数x，那么要包含所有的x且最短，那么就需要选择first[x]到last[x]这一段，计算其长度，其中最短的即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def findShortestSubArray(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        first = {}
        last = {}
        cnt = {}

        max_cnt = 0

        for index, num in enumerate(nums):
            cnt[num] = cnt.get(num, 0) + 1
            if num not in first:
                first[num] = index
            last[num] = index
            max_cnt = max(max_cnt, cnt[num])

        res = len(nums)
        for num in cnt:
            if cnt[num] == max_cnt:
                res = min(res, last[num] - first[num] + 1)

        return res
```
