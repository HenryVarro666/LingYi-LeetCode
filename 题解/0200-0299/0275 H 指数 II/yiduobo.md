---
title: "275. H指数II"
aliases: ["yiduobo的每日leetcode 275.H指数II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/graph", "leetcode/binary-search", "题单/二分算法", "题单/二分算法/二-二分答案"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/152526276"
zhihu_id: "152526276"
zhihu_title: "yiduobo的每日leetcode 275.H指数II"
question_id: "275"
question: "H 指数 II"
problem_url: "https://leetcode.cn/problems/h-index-ii/"
difficulty: "Medium"
created: "2020-07-01T17:36:22+08:00"
updated: "2020-07-01T17:36:22+08:00"
upvotes: 1
comments: 0
---

# 275. H指数II

> **[yiduobo的每日leetcode 275.H指数II](https://zhuanlan.zhihu.com/p/152526276) · 知乎 · 2020-07-01 · 赞同 1**
> 力扣：[275. H 指数 II](https://leetcode.cn/problems/h-index-ii/) · Medium · 灵茶山艾府：[【图解】一图掌握二分答案，四种写法（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

275.H指数II <https://leetcode-cn.com/problems/h-index-ii/>

题目保证了引用次数有序，且要求给出一种对数时间复杂度的做法，于是自然而然就想到了二分。这里二分的时候需要注意的是，当我们二分h时，需要验证的是从大到小第h篇文章的引用次数是否超过了h，而二分时的mid \= (l + r)/2表示从小到大第mid个数，因此在具体实现的时候需要进行转换，即从1到n开始进行二分，那么数组下标为n-mid的数就是数组中从大到小的第mid个数了。

最后附上python代码：

```python
class Solution(object):
    def hIndex(self, citations):
        """
        :type citations: List[int]
        :rtype: int
        """

        if not citations:
            return 0

        left = 1
        right = len(citations)
        res = 0
        while left <= right:
            mid = (left + right) / 2
            if citations[len(citations) - mid] >= mid:
                res = mid
                left = mid + 1
            else:
                right = mid - 1

        return res
```
