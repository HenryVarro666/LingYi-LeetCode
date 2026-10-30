---
title: "2498. 青蛙过河II"
aliases: ["yiduobo的每日leetcode 2498.青蛙过河II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/贪心算法", "题单/贪心算法/八-其他"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/633499527"
zhihu_id: "633499527"
zhihu_title: "yiduobo的每日leetcode 2498.青蛙过河II"
question_id: "2498"
question: "青蛙过河 II"
problem_url: "https://leetcode.cn/problems/frog-jump-ii/"
difficulty: "Medium"
rating: 1759
created: "2023-05-31T01:54:46+08:00"
updated: "2023-05-31T01:54:46+08:00"
upvotes: 0
comments: 0
---

# 2498. 青蛙过河II

> **[yiduobo的每日leetcode 2498.青蛙过河II](https://zhuanlan.zhihu.com/p/633499527) · 知乎 · 2023-05-31 · 赞同 0**
> 力扣：[2498. 青蛙过河 II](https://leetcode.cn/problems/frog-jump-ii/) · Medium · 灵茶山艾府：[间隔跳跃+简单证明](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2498.青蛙过河II

[力扣](https://leetcode.cn/problems/frog-jump-ii/)

题目要求找出正反两条不相交的路径，且路径中距离最远的两个落脚点之间的距离最短。

对于正反不相交路径的问题，常规的处理方法是将其转化成从起点开始到终点的两条不相交路径。另一方面，为了使得落脚点之间的距离最短，显然就应该将所有的落脚点都用上。而对于落脚点的分配，则应该将下一个最近的落脚点分给上一个落脚点离起点较近的那条路径，理由也很简单，因为如果分配给另一条路径，那么落脚点较近的那条路径到其下一个落脚点的距离只会更远。

根据这个结论，就可以一趟遍历，为两条路径交替分配落脚点并更新最终答案。

最后附上python代码：

```python
class Solution(object):
    def maxJump(self, stones):
        """
        :type stones: List[int]
        :rtype: int
        """

        if len(stones) <= 3:
            return stones[-1]
        
        p1 = p2 = 0
        res = 0
        for index in range(1, len(stones) - 1, 2):
            res = max(res, stones[index] - stones[p1], stones[index + 1] - stones[p2])
            p1 = index
            p2 = index + 1
        
        return max(res, stones[-1] - stones[p1], stones[-1] - stones[p2])
```
