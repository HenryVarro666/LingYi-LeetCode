---
title: "3809. 最好可到达的塔"
aliases: ["yiduobo的每日leetcode 3809.最好可到达的塔"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1996621955877578296"
zhihu_id: "1996621955877578296"
zhihu_title: "yiduobo的每日leetcode 3809.最好可到达的塔"
question_id: "3809"
question: "最好可到达的塔"
problem_url: "https://leetcode.cn/problems/best-reachable-tower/"
difficulty: "Medium"
created: "2026-01-19T20:07:26+08:00"
updated: "2026-01-19T20:07:30+08:00"
upvotes: 1
comments: 0
---

# 3809. 最好可到达的塔

> **[yiduobo的每日leetcode 3809.最好可到达的塔](https://zhuanlan.zhihu.com/p/1996621955877578296) · 知乎 · 2026-01-19 · 赞同 1**
> 力扣：[3809. 最好可到达的塔](https://leetcode.cn/problems/best-reachable-tower/) · Medium · 灵茶山艾府：[按题意模拟，简洁写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3809.最好可到达的塔

[3809. 最好可到达的塔 - 力扣（LeetCode）](https://leetcode.cn/problems/best-reachable-tower/description/)

题目给出一个二维整数数组towers，其中towers\[index\] \= \[x\[index\], y\[index\], q\[index\]\]，表示第index座塔的坐标为(x\[index\], y\[index\])，其质量因子为q\[index\]。

另外给出一个整数数组center \= [cx, cy]，表示现在所处的位置，以及一个整数radius。

若一座塔与center之间的曼哈顿距离小于等于radius，就称这座塔是可达的。

问所有可达的塔中质量因子最大的塔的坐标。若质量因子相同，则返回坐标字典序最小的塔。若没有可达的塔，则返回[-1, -1]。

按照题目要求一趟遍历计算就行了。对于当前的塔，先计算center与这座塔的曼哈顿距离，若小于等于radius，就是用这座塔来更新答案。更新的标准是质量因子更大，或者质量因子相同且坐标字典序更小。

最后附上python代码：

```python
class Solution(object):
    def bestTower(self, towers, center, radius):
        """
        :type towers: List[List[int]]
        :type center: List[int]
        :type radius: int
        :rtype: List[int]
        """
        
        ma = -1
        res = [-1, -1]
        for index, (x, y, q) in enumerate(towers):
            if abs(x - center[0]) + abs(y - center[1]) <= radius and q > ma or (q == ma and (res[0] > x or (res[0] == x and res[1] > y))):
                ma = q
                res = [x, y]
        
        return res
```
