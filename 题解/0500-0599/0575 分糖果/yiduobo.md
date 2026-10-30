---
title: "575. 分糖果"
aliases: ["yiduobo的每日leetcode 575.分糖果"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/hash-table"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/266581572"
zhihu_id: "266581572"
zhihu_title: "yiduobo的每日leetcode 575.分糖果"
question_id: "575"
question: "分糖果"
problem_url: "https://leetcode.cn/problems/distribute-candies/"
difficulty: "Easy"
created: "2020-10-18T16:03:41+08:00"
updated: "2020-10-18T16:03:41+08:00"
upvotes: 1
comments: 0
---

# 575. 分糖果

> **[yiduobo的每日leetcode 575.分糖果](https://zhuanlan.zhihu.com/p/266581572) · 知乎 · 2020-10-18 · 赞同 1**
> 力扣：[575. 分糖果](https://leetcode.cn/problems/distribute-candies/) · Easy · 灵茶山艾府：[min(|set|, n/2)](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

575.分糖果<https://leetcode-cn.com/problems/distribute-candies/>

比较基础的题目，通过set统计糖果的种类数，我们希望每种糖果都可以分给姐姐，而姐姐最多可以分到len(candies)/2个糖果，因此这两个数取较小值就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def distributeCandies(self, candies):
        """
        :type candies: List[int]
        :rtype: int
        """

        candy_set = set()
        for candy in candies:
            candy_set.add(candy)
        
        return min(len(candy_set), len(candies) / 2)
```
