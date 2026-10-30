---
title: "1989. 捉迷藏中可捕获的最大人数"
aliases: ["yiduobo的每日leetcode 1989.捉迷藏中可捕获的最大人数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/624652989"
zhihu_id: "624652989"
zhihu_title: "yiduobo的每日leetcode 1989.捉迷藏中可捕获的最大人数"
question_id: "1989"
question: "捉迷藏中可捕获的最大人数"
problem_url: "https://leetcode.cn/problems/maximum-number-of-people-that-can-be-caught-in-tag/"
created: "2023-04-25T03:12:03+08:00"
updated: "2023-04-25T03:12:03+08:00"
upvotes: 1
comments: 0
---

# 1989. 捉迷藏中可捕获的最大人数

> **[yiduobo的每日leetcode 1989.捉迷藏中可捕获的最大人数](https://zhuanlan.zhihu.com/p/624652989) · 知乎 · 2023-04-25 · 赞同 1**
> 力扣：[1989. 捉迷藏中可捕获的最大人数](https://leetcode.cn/problems/maximum-number-of-people-that-can-be-caught-in-tag/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1989.捉迷藏中可捕获的最大人数

[力扣](https://leetcode.cn/problems/maximum-number-of-people-that-can-be-caught-in-tag/)

由于本题只要求最大的配对，而每个人都是平等的，因此在这里就可以将所有人按位置从小到大排序，然后一趟遍历，尽可能地进行配对。

对于当前遍历到的人，最优的配对方案必然是选择当前可以抓到这个人的鬼当中，位置最左侧的那一个，因为对于后续的人而言，其位置必然是更靠后的，因此其可配对的鬼的位置也是更靠后的。

有了这个结论，就可以一趟遍历，将人和鬼的位置都收集起来，这样人和鬼的位置数组就都是天然有序的。接下来对人的数组一趟遍历，并使用一个变量p记录可以抓到这个人的最左侧的鬼，若不存在这样的鬼，那么就记录这个人右侧最左侧的鬼。这样一来，就可以在均摊O(1)的时间内找到每个人对应的p，然后判断这个人能否被位于p的鬼抓到并更新答案。

最后附上python代码：

```python
class Solution(object):
    def catchMaximumAmountofPeople(self, team, dist):
        """
        :type team: List[int]
        :type dist: int
        :rtype: int
        """

        h = []
        g = []
        for index, v in enumerate(team):
            if v == 0:
                h.append(index)
            else:
                g.append(index)
        
        res = 0
        p = 0
        for index in h:
            while p < len(g) and g[p] < index - dist:
                p += 1
            
            if p == len(g):
                break
            
            if abs(g[p] - index) <= dist:
                res += 1
                p += 1
        
        return res
```
