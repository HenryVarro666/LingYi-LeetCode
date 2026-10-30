---
title: "1788. 最大化花园的美观度"
aliases: ["yiduobo的每日leetcode 1788.最大化花园的美观度"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/hash-table", "leetcode/prefix-sum", "题单/常用数据结构", "题单/常用数据结构/一-前缀和"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/621496061"
zhihu_id: "621496061"
zhihu_title: "yiduobo的每日leetcode 1788.最大化花园的美观度"
question_id: "1788"
question: "最大化花园的美观度"
problem_url: "https://leetcode.cn/problems/maximize-the-beauty-of-the-garden/"
difficulty: "Hard"
created: "2023-04-13T00:25:47+08:00"
updated: "2023-04-13T00:25:47+08:00"
upvotes: 0
comments: 0
---

# 1788. 最大化花园的美观度

> **[yiduobo的每日leetcode 1788.最大化花园的美观度](https://zhuanlan.zhihu.com/p/621496061) · 知乎 · 2023-04-13 · 赞同 0**
> 力扣：[1788. 最大化花园的美观度](https://leetcode.cn/problems/maximize-the-beauty-of-the-garden/) · Hard · 灵茶山艾府：[Go 前缀和](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1788.最大化花园的美观度

[力扣](https://leetcode.cn/problems/maximize-the-beauty-of-the-garden/)

首先，不妨设一个候选答案最外侧两朵花的下标分别为l和r，其颜色为v，那么l一定是花园中最左侧的v，r则是花园中最右侧的v，理由是如果外侧还存在其他的v，那么就可以将l和r向外侧移动。由于可以自由选择区间内的花，因此只需留下新扩大区间中权重非负的花，这样一来即使是最坏情况总的美观度也不会比之前的情况更差。

根据这个结论，就可以一趟遍历，记录每种颜色第一次和最后一次出现的下标。接下来遍历所有颜色，若该颜色第一次和最后一次出现的位置不同，那么以这两朵花为左右边界的最优解就是这个区间内所有非负整数之和，再加上边间这两朵花的权重。

这是一个区间和问题，那么只需一趟遍历，计算出数组中的所有非负数的前缀和，利用前缀和之差来求解区间和。

最后附上python代码：

```python
class Solution(object):
    def maximumBeauty(self, flowers):
        """
        :type flowers: List[int]
        :rtype: int
        """

        first = {}
        last = {}
        n = len(flowers)
        s = []
        for index, v in enumerate(flowers):
            if v not in first:
                first[v] = index
            last[v] = index
            
            v = max(v, 0)
            if index == 0:
                s.append(v)
            else:
                s.append(v + s[-1])
        
        res = -20001
        for v in first:
            if last[v] != first[v]:
                res = max(res, s[last[v] - 1] - s[first[v]] + v + v)
        
        return res
```
