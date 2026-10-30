---
title: "2580. 统计将重叠区间合并成组的方案数"
aliases: ["yiduobo的每日leetcode 2580.统计将重叠区间合并成组的方案数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/二-区间贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/642375611"
zhihu_id: "642375611"
zhihu_title: "yiduobo的每日leetcode 2580.统计将重叠区间合并成组的方案数"
question_id: "2580"
question: "统计将重叠区间合并成组的方案数"
problem_url: "https://leetcode.cn/problems/count-ways-to-group-overlapping-ranges/"
difficulty: "Medium"
rating: 1632
created: "2023-07-08T23:54:29+08:00"
updated: "2023-07-08T23:54:29+08:00"
upvotes: 0
comments: 0
---

# 2580. 统计将重叠区间合并成组的方案数

> **[yiduobo的每日leetcode 2580.统计将重叠区间合并成组的方案数](https://zhuanlan.zhihu.com/p/642375611) · 知乎 · 2023-07-08 · 赞同 0**
> 力扣：[2580. 统计将重叠区间合并成组的方案数](https://leetcode.cn/problems/count-ways-to-group-overlapping-ranges/) · Medium · 灵茶山艾府：[合并区间，附题单（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2580.统计将重叠区间合并成组的方案数

[力扣](https://leetcode.cn/problems/count-ways-to-group-overlapping-ranges/)

由于题目规定了相交的区间必须分到相同的组中，那么就需要先将相交区间全部合并，得到最终的不重叠区间列表。不妨设其中有cnt个区间，那么对于这cnt个区间而言，既可以加入到第一个组也可以加入到第二个组，因此最终答案就是2^cnt。

对于区间合并操作，则可以将所有区间按起点从小到大进行排序，接下来一趟遍历。若当前遍历到的区间与上一个区间相交，那么就将二者合并。由于当前区间的起点必然大于等于上一个区间的起点，那么此时就只需使用当前区间的终点去更新上一个区间的终点。

反之，若当前区间与上一个区间不相交，那么就说明上一个区间已经没有机会再与后续的区间相交。由于在这里只关心不重叠区间的数量，因此在这里只需将cnt加上1即可。

另外，在遍历结束后还需要将cnt额外再加上1，表示合并后的最后这个区间。

最后附上python代码：

```python
class Solution(object):
    def countWays(self, ranges):
        """
        :type ranges: List[List[int]]
        :rtype: int
        """

        cnt = 0
        lastx, lasty = None, None
        for x, y in sorted(ranges):
            if lastx is None:
                lastx, lasty = x, y
            elif lasty < x:
                cnt += 1
                lastx, lasty = x, y
            else:
                lasty = max(lasty, y)
        
        cnt += 1
        res = 1
        mod = 10 ** 9 + 7
        for _ in range(cnt):
            res += res
            if res >= mod:
                res -= mod
        
        return res
```
