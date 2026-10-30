---
title: "573. 松鼠模拟"
aliases: ["yiduobo的每日leetcode 573.松鼠模拟"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/601537471"
zhihu_id: "601537471"
zhihu_title: "yiduobo的每日leetcode 573.松鼠模拟"
question_id: "573"
question: "松鼠模拟"
problem_url: "https://leetcode.cn/problems/squirrel-simulation/"
created: "2023-01-28T23:20:29+08:00"
updated: "2023-01-28T23:20:29+08:00"
upvotes: 0
comments: 0
---

# 573. 松鼠模拟

> **[yiduobo的每日leetcode 573.松鼠模拟](https://zhuanlan.zhihu.com/p/601537471) · 知乎 · 2023-01-28 · 赞同 0**
> 力扣：[573. 松鼠模拟](https://leetcode.cn/problems/squirrel-simulation/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

573.松鼠模拟

[力扣](https://leetcode.cn/problems/squirrel-simulation/)

注意到松鼠每次只能携带一颗松果，那么除了第一颗松果外，其他所有松果的收集路径必然都是从树出发来到松果的坐标，再返回树的坐标，因此最终答案就是

松鼠到某颗松果的距离 + 这颗松果到树的距离 + 树到其他所有松果的距离 \* 2

对于这个式子，如果补上一项树到首颗松果的距离，那么就是

松鼠到某颗松果的距离 - 树到这颗松果的距离 + C

这里C是常数，为所有松果到树的距离之和乘以2

对于上面这个式子，为了使其最小，只需枚举第一颗松果是哪一颗，然后计算路径长度取最小值即可。

最后附上python代码：

```python
class Solution(object):
    def minDistance(self, height, width, tree, squirrel, nuts):
        """
        :type height: int
        :type width: int
        :type tree: List[int]
        :type squirrel: List[int]
        :type nuts: List[List[int]]
        :rtype: int
        """

        s = 0
        for x, y in nuts:
            s += abs(tree[0] - x) + abs(tree[1] - y)
        
        s += s
        res = None
        for x, y in nuts:
            now = s - abs(tree[0] - x) - abs(tree[1] - y) + abs(squirrel[0] - x) + abs(squirrel[1] - y)
            if res is None or res > now:
                res = now
        
        return res
```
