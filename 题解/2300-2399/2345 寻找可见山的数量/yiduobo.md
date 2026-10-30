---
title: "2345. 寻找可见山的数量"
aliases: ["yiduobo的每日leetcode 2345.寻找可见山的数量"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/630213891"
zhihu_id: "630213891"
zhihu_title: "yiduobo的每日leetcode 2345.寻找可见山的数量"
question_id: "2345"
question: "寻找可见山的数量"
problem_url: "https://leetcode.cn/problems/finding-the-number-of-visible-mountains/"
created: "2023-05-18T00:14:41+08:00"
updated: "2023-05-18T00:14:41+08:00"
upvotes: 0
comments: 0
---

# 2345. 寻找可见山的数量

> **[yiduobo的每日leetcode 2345.寻找可见山的数量](https://zhuanlan.zhihu.com/p/630213891) · 知乎 · 2023-05-18 · 赞同 0**
> 力扣：[2345. 寻找可见山的数量](https://leetcode.cn/problems/finding-the-number-of-visible-mountains/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2345.寻找可见山的数量

[力扣](https://leetcode.cn/problems/finding-the-number-of-visible-mountains/)

注意到山都是标准的等腰直角三角形，那么一座山的顶峰被另一座山覆盖等价于其底边被另一座山的底边完全包含，于是问题就转化成了给出若干区间，求没有被其他区间完全包围的区间。

对于这个问题，只需将区间按照端点从小到大进行排序，然后一趟遍历即可。需要特别注意本题可能出现两座完全重叠的山峰，这种情况下两座山都不能计入答案。

最后附上python代码：

```python
class Solution(object):
    def visibleMountains(self, peaks):
        """
        :type peaks: List[List[int]]
        :rtype: int
        """

        intervals = []
        for x, y in peaks:
            intervals.append([x - y, x + y])
        
        last_x, last_y = None, None
        check_same = False
        res = len(peaks)
        for x, y in sorted(intervals, key=lambda d:(d[0], -d[1])):
            if last_x is None:
                last_x, last_y = x, y
            else:
                if not check_same and last_x == x and last_y == y:
                    check_same = True
                    res -= 1

                if last_x <= x and y <= last_y:
                    res -= 1
                else:
                    last_x, last_y = x, y
                    check_same = False
                
        return res
```
