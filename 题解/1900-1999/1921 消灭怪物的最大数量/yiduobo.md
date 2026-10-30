---
title: "1921. 消灭怪物的最大数量"
aliases: ["yiduobo的每日leetcode 1921.消灭怪物的最大数量"]
tags: ["leetcode", "yiduobo", "leetcode/medium"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/485029712"
zhihu_id: "485029712"
zhihu_title: "yiduobo的每日leetcode 1921.消灭怪物的最大数量"
question_id: "1921"
question: "消灭怪物的最大数量"
problem_url: "https://leetcode.cn/problems/eliminate-maximum-number-of-monsters/"
difficulty: "Medium"
created: "2022-03-21T22:45:12+08:00"
updated: "2022-03-21T22:45:12+08:00"
upvotes: 0
comments: 0
---

# 1921. 消灭怪物的最大数量

> **[yiduobo的每日leetcode 1921.消灭怪物的最大数量](https://zhuanlan.zhihu.com/p/485029712) · 知乎 · 2022-03-21 · 赞同 0**
> 力扣：[1921. 消灭怪物的最大数量](https://leetcode.cn/problems/eliminate-maximum-number-of-monsters/) · Medium · 灵茶山艾府：[按照时间排序+贪心](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1921.消灭怪物的最大数量

[力扣](https://leetcode-cn.com/problems/eliminate-maximum-number-of-monsters/)

很明显，哪只怪物先到就应该先杀哪只怪物，因此可以先计算每只怪物到达的时间，然后从小到大排序。

接下来一趟遍历，此时的数组下标恰好是开火的时间点。若当前下标对应的怪物到达时间小于等于当前的下标，那么说明此时已经来不及开火了，消灭的怪物数量恰好就是下标的数值。若所有怪物到达时间都大于对应的下标，那么就返回n。

最后附上python代码：

```python
class Solution(object):
    def eliminateMaximum(self, dist, speed):
        """
        :type dist: List[int]
        :type speed: List[int]
        :rtype: int
        """

        t = []
        n = len(dist)
        for index in range(n):
            t.append(dist[index] / speed[index])
            if dist[index] % speed[index] > 0:
                t[-1] += 1
        
        t.sort()
        for index in range(n):
            if t[index] <= index:
                return index
        
        return n
```
