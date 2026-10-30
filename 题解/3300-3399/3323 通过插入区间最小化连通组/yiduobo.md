---
title: "3323. 通过插入区间最小化连通组"
aliases: ["yiduobo的每日leetcode 3323.通过插入区间最小化连通组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2362572754"
zhihu_id: "2362572754"
zhihu_title: "yiduobo的每日leetcode 3323.通过插入区间最小化连通组"
question_id: "3323"
question: "通过插入区间最小化连通组"
problem_url: "https://leetcode.cn/problems/minimize-connected-groups-by-inserting-interval/"
created: "2024-10-21T22:53:00+08:00"
updated: "2024-10-21T22:53:00+08:00"
upvotes: 1
comments: 0
---

# 3323. 通过插入区间最小化连通组

> **[yiduobo的每日leetcode 3323.通过插入区间最小化连通组](https://zhuanlan.zhihu.com/p/2362572754) · 知乎 · 2024-10-21 · 赞同 1**
> 力扣：[3323. 通过插入区间最小化连通组](https://leetcode.cn/problems/minimize-connected-groups-by-inserting-interval/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3323.通过插入区间最小化连通组

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimize-connected-groups-by-inserting-interval/description/)

题目给出一个二维数组intervals，其中intervals\[i\] \= \[start\[i\], end\[i\]\]，表示区间i的开头和结尾。另外给出一个整数k，要求向数组中添加一个新的区间\[start\[new\], end\[new\]\]，这个区间的长度小于等于k，且添加之后intervals中的连通组最少。

连通组指的是一起覆盖了从最小点到最大点的连续范围，中间没有间隙的区间的最大集合。

首先，新添加的区间一定是添加在本来不属于用一个连通组的区间，于是可以先对所有区间按起点排序，然后对区间进行合并。

接下来，为了可以合并尽量多的连通组，新添加的区间应该顶着长度k来设置，同时这个新区间应该和其连通的最左侧区间重叠的部分最小，理由是这样一来才能尽量覆盖后续更多的区间，也就是说这个区间的起点应该设置在某个已有区间的终点。

另一方面，由于在上一步合并区间时已经排序过了，那么在这里在这里只需按顺序枚举新区间连通的最左侧区间index，随着index的向后移动，可覆盖区间的下标编号必然是单调不减的，于是可以使用一个变量p表示当前可以覆盖的下标最大的区间，那么这种情况下连通的区间数量就是p - index + 1，使用合并后区间的数量减去这个值之后更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def minConnectedGroups(self, intervals, k):
        """
        :type intervals: List[List[int]]
        :type k: int
        :rtype: int
        """
        
        intervals.sort()
        merged = []
        x, y = intervals[0]
        for nowx, nowy in intervals[1:]:
            if nowx <= y:
                y = max(y, nowy)
            else:
                merged.append([x, y])
                x, y = nowx, nowy
        
        merged.append([x, y])

        print merged

        p = 0
        res = len(merged)
        for index in range(len(merged)):
            addy = merged[index][1] + k
        
            while p < len(merged) and merged[p][0] <= addy:
                p += 1
        
            res = min(res, len(merged) - p + index + 1)
        
        return res
```
