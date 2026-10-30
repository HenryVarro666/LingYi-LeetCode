---
title: "1893. 检查是否区域内所有整数都被覆盖"
aliases: ["yiduobo的每日leetcode 1893.检查是否区域内所有整数都被覆盖"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "题单/常用数据结构", "题单/常用数据结构/二-差分"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/479018570"
zhihu_id: "479018570"
zhihu_title: "yiduobo的每日leetcode 1893.检查是否区域内所有整数都被覆盖"
question_id: "1893"
question: "检查是否区域内所有整数都被覆盖"
problem_url: "https://leetcode.cn/problems/check-if-all-the-integers-in-a-range-are-covered/"
difficulty: "Easy"
rating: 1307
created: "2022-03-11T00:07:21+08:00"
updated: "2022-03-11T00:07:21+08:00"
upvotes: 1
comments: 0
---

# 1893. 检查是否区域内所有整数都被覆盖

> **[yiduobo的每日leetcode 1893.检查是否区域内所有整数都被覆盖](https://zhuanlan.zhihu.com/p/479018570) · 知乎 · 2022-03-11 · 赞同 1**
> 力扣：[1893. 检查是否区域内所有整数都被覆盖](https://leetcode.cn/problems/check-if-all-the-integers-in-a-range-are-covered/) · Easy · 灵茶山艾府：[差分写法](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1893.检查是否区域内所有整数都被覆盖

[力扣](https://leetcode-cn.com/problems/check-if-all-the-integers-in-a-range-are-covered/)

由于题目要求区间内所有整数都被覆盖，那么如果能覆盖住，说明覆盖这个区域的区间也必然是连续的，于是在这里可以先将这些区间按起点从小到大进行排序，然后合并连续或重叠的区间，然后检测合并后的区间是否覆盖住了题目要求的区域。

当然，本题数据范围极小，随便怎么搞其实都行。

最后附上python代码：

```python
class Solution(object):
    def isCovered(self, ranges, left, right):
        """
        :type ranges: List[List[int]]
        :type left: int
        :type right: int
        :rtype: bool
        """

        merged_intervals = []
        sorted_ranges = sorted(ranges, key=lambda d:d[0])
        start, end = sorted_ranges[0]
        for x, y in sorted_ranges[1:]:
            if x <= end + 1:
                end = max(end, y)
            else:
                if start <= left and right <= end:
                    return True
                start, end = x, y

        return start <= left and right <= end
```
