---
title: "2849. 判断能否在给定时间到达单元格"
aliases: ["yiduobo的每日leetcode 2849.判断能否在给定时间到达单元格"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/660608223"
zhihu_id: "660608223"
zhihu_title: "yiduobo的每日leetcode 2849.判断能否在给定时间到达单元格"
question_id: "2849"
question: "判断能否在给定时间到达单元格"
problem_url: "https://leetcode.cn/problems/determine-if-a-cell-is-reachable-at-a-given-time/"
difficulty: "Medium"
created: "2023-10-11T02:53:12+08:00"
updated: "2023-10-11T02:53:12+08:00"
upvotes: 0
comments: 0
---

# 2849. 判断能否在给定时间到达单元格

> **[yiduobo的每日leetcode 2849.判断能否在给定时间到达单元格](https://zhuanlan.zhihu.com/p/660608223) · 知乎 · 2023-10-11 · 赞同 0**
> 力扣：[2849. 判断能否在给定时间到达单元格](https://leetcode.cn/problems/determine-if-a-cell-is-reachable-at-a-given-time/) · Medium · 灵茶山艾府：[先斜着走再直走，然后在终点绕圈圈（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2849.判断能否在给定时间到达单元格

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/determine-if-a-cell-is-reachable-at-a-given-time/)

首先，如果走最短的路径的时间都超过了t的话，那么答案必然是false，因此在这里就需要先计算出从起点到终点最短需要走几步。可以发现，一步斜线是比一步水平加一步竖直更优的，因此应该尽量走斜线。令x和y分别表示从起点与终点在水平方向和竖直方向的距离，那么可以走的斜线的数量就是min(x, y)，因此总的步数就是min_cost \= x + y - min(x, y)。

当min_cost > t时，答案显然为false，而对于min_cost \<\= t时则需要进一步讨论。

最直观的来看，左右横跳可以浪费掉所有的偶数步数，而往右下的一步斜线，然后再往左走一步最后往上走一步，相当于浪费了三步。综合这两点，就可以得到当t - min_cost >\= 2时，多出的步数是可以完美浪费掉的。

最后则需要讨论t \= min_cost + 1的情况。当移动路径上出现了竖直移动时，可以通过一步斜线加上一步往回走的水平移动来替代一次竖直移动；同样的，也可以利用一步斜线加上一步往回走的竖直移动来替代一次水平移动；最后一步水平移动加上一步竖直移动则可以替代一步斜线移动。综合起来，只要从起点到终点的路径上产生过移动，就必然可以浪费掉多出的一步。

换言之，只要当起点和终点重叠且t等于1时答案才为false，除此之外其他所有min_cost \<\= t的情况答案都为true。

最后附上python代码：

```python
class Solution(object):
    def isReachableAtTime(self, sx, sy, fx, fy, t):
        """
        :type sx: int
        :type sy: int
        :type fx: int
        :type fy: int
        :type t: int
        :rtype: bool
        """

        x = abs(sx - fx)
        y = abs(sy - fy)
        xy = min(x, y)
        
        min_cost = x + y - xy
        if min_cost > t:
            return False
        
        if x == 0 and y == 0 and t == 1:
            return False
        
        return True
```
