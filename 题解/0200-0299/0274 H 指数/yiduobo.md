---
title: "274. H指数"
aliases: ["yiduobo的每日leetcode 274.H指数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/graph", "leetcode/counting-sort", "题单/面试经典-150-题", "题单/面试经典-150-题/数组-/-字符串"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/152240076"
zhihu_id: "152240076"
zhihu_title: "yiduobo的每日leetcode 274.H指数"
question_id: "274"
question: "H 指数"
problem_url: "https://leetcode.cn/problems/h-index/"
difficulty: "Medium"
created: "2020-06-30T22:51:24+08:00"
updated: "2020-06-30T22:51:24+08:00"
upvotes: 0
comments: 0
---

# 274. H指数

> **[yiduobo的每日leetcode 274.H指数](https://zhuanlan.zhihu.com/p/152240076) · 知乎 · 2020-06-30 · 赞同 0**
> 力扣：[274. H 指数](https://leetcode.cn/problems/h-index/) · Medium · 灵茶山艾府：[没看懂题意？一张图秒懂（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

274.H指数<https://leetcode-cn.com/problems/h-index/>

首先，h至多为文章的总数，于是当一篇文章的引用次数多于文章的总数时，我们可以将引用次数置为文章总数，这样一来就将文章的引用次数都缩减到文章总数的范围当中了。

接下来，使用一个dict储存每个引用数对应的文章篇数，然后从文章总数开始，从大到小枚举h，通过后缀和的方式判断当前枚举的h是否满足引用数大于等于h的文章总数是否大于等于h即可。

最后附上python代码：

```python
class Solution(object):
    def hIndex(self, citations):
        """
        :type citations: List[int]
        :rtype: int
        """

        count = {}
        for num in citations:
            if num > len(citations):
                num = len(citations)
            count[num] = count.get(num, 0) + 1

        total = 0
        for num in range(len(citations), -1, -1):
            if total + count.get(num, 0) >= num:
                return num
            total += count.get(num, 0)

        return 0
```
