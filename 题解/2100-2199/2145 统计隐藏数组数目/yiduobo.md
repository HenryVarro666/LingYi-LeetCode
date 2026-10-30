---
title: "2145. 统计隐藏数组数目"
aliases: ["yiduobo的每日leetcode 2145.统计隐藏数组数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/prefix-sum", "题单/数学算法", "题单/数学算法/七-杂项"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/529371286"
zhihu_id: "529371286"
zhihu_title: "yiduobo的每日leetcode 2145.统计隐藏数组数目"
question_id: "2145"
question: "统计隐藏数组数目"
problem_url: "https://leetcode.cn/problems/count-the-hidden-sequences/"
difficulty: "Medium"
rating: 1614
created: "2022-06-15T22:44:14+08:00"
updated: "2022-06-15T22:44:14+08:00"
upvotes: 0
comments: 0
---

# 2145. 统计隐藏数组数目

> **[yiduobo的每日leetcode 2145.统计隐藏数组数目](https://zhuanlan.zhihu.com/p/529371286) · 知乎 · 2022-06-15 · 赞同 0**
> 力扣：[2145. 统计隐藏数组数目](https://leetcode.cn/problems/count-the-hidden-sequences/) · Medium · 灵茶山艾府：[详细数学推导（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2145.统计隐藏数组数组

[力扣](https://leetcode.cn/problems/count-the-hidden-sequences/)

在得知了数组的首个数字hidden[0]之后，就可以通过differences数组计算出hidden数组后续所有的数，并将其写成hidden[index] \= hidden[0] + delta[index]的形式。

对于题目给出的上下限，只需要任意的hidden[index]都在这个范围内，换言之，就是其中的最小值大于等于lower，最大值小于等于upper。

在这里不妨设delta[0] \= 0，那么同样可以将hidden[0]写成hidden[0] + delta[0]的形式，于是所有数中的最小值就是最小的delta[index]对应的hidden[0] + delta[index]，而最大值则是最大的delta[index]对应的hidden[0] + delta[index]，不妨将最小和最大的delta分别记为min_delta以及max_delta，那么就变成了需要满足

hidden[0] + min_delta >\= lower

hidden[0] + max_delta \<\= upper

根据上面两个不等式就可以计算出hidden[0]的上限和下限，即

lower - min_delta \<\= hidden[0] \<\= upper - max_delta

在这之间的所有hidden[0]都是可用的，因此最终答案就是upper - max_delta - (lower - min_delta) + 1了。

最后附上python代码：

```python
class Solution(object):
    def numberOfArrays(self, differences, lower, upper):
        """
        :type differences: List[int]
        :type lower: int
        :type upper: int
        :rtype: int
        """

        max_delta = min_delta = 0
        now = 0
        for diff in differences:
            now += diff
            max_delta = max(max_delta, now)
            min_delta = min(min_delta, now)
        
        max_start = upper - max_delta
        min_start = lower - min_delta

        return max(0, max_start - min_start + 1)
```
