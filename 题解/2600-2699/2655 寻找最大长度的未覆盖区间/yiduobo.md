---
title: "2655. 寻找最大长度的未覆盖区间"
aliases: ["yiduobo的每日leetcode 2655.寻找最大长度的未覆盖区间"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/647883887"
zhihu_id: "647883887"
zhihu_title: "yiduobo的每日leetcode 2655.寻找最大长度的未覆盖区间"
question_id: "2655"
question: "寻找最大长度的未覆盖区间"
problem_url: "https://leetcode.cn/problems/find-maximal-uncovered-ranges/"
created: "2023-08-04T04:12:56+08:00"
updated: "2023-08-04T04:12:56+08:00"
upvotes: 0
comments: 0
---

# 2655. 寻找最大长度的未覆盖区间

> **[yiduobo的每日leetcode 2655.寻找最大长度的未覆盖区间](https://zhuanlan.zhihu.com/p/647883887) · 知乎 · 2023-08-04 · 赞同 0**
> 力扣：[2655. 寻找最大长度的未覆盖区间](https://leetcode.cn/problems/find-maximal-uncovered-ranges/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2655.寻找最大长度的未覆盖区间

[力扣](https://leetcode.cn/problems/find-maximal-uncovered-ranges/)

经典的区间合并问题，将所有区间按起点进行排序，然后一趟遍历。若当前遍历到的区间起点在上一个区间的终点之前，或者紧挨着上一个区间的终点，那么就将这两个区间合并，同时用本区间的终点更新合并后区间的终点；反过来，说明两端区间之前存在未覆盖区域，那么这个未覆盖区域的起点就是上一个区间的终点加1，而未覆盖区域的终点则是本区间的起点减1。

另外需要注意的是，除了处理区间之间的未覆盖区域外，还需要处理边界上的未覆盖区域。若首个区间的起点不为0，那么从0到首个区间起点减1这一段也是未覆盖的。同样的，若最后一个区间的终点不为n - 1，那么从最后一个区间的终点加1到n - 1这一段也是未覆盖的。

最后附上python代码：

```python
class Solution(object):
    def findMaximalUncoveredRanges(self, n, ranges):
        """
        :type n: int
        :type ranges: List[List[int]]
        :rtype: List[List[int]]
        """

        if not ranges:
            return [[0, n - 1]]

        ranges.sort()
        res = []
        if ranges[0][0] > 0:
            res.append([0, ranges[0][0] - 1])
        
        nowx, nowy = ranges[0]
        for x, y in ranges[1:]:
            if x <= nowy + 1:
                nowy = max(nowy, y)
            else:
                res.append([nowy + 1, x - 1])
                nowx, nowy = x, y
        
        if nowy + 1 < n:
            res.append([nowy + 1, n - 1])
        
        return res
```
