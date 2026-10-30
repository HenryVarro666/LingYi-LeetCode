---
title: "1167. 连接棒材的最低费用"
aliases: ["yiduobo的每日leetcode 1167.连接棒材的最低费用"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/611597999"
zhihu_id: "611597999"
zhihu_title: "yiduobo的每日leetcode 1167.连接棒材的最低费用"
question_id: "1167"
question: "连接棒材的最低费用"
problem_url: "https://leetcode.cn/problems/minimum-cost-to-connect-sticks/"
created: "2023-03-06T03:49:38+08:00"
updated: "2023-03-06T03:49:38+08:00"
upvotes: 0
comments: 0
---

# 1167. 连接棒材的最低费用

> **[yiduobo的每日leetcode 1167.连接棒材的最低费用](https://zhuanlan.zhihu.com/p/611597999) · 知乎 · 2023-03-06 · 赞同 0**
> 力扣：[1167. 连接棒材的最低费用](https://leetcode.cn/problems/minimum-cost-to-connect-sticks/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1167.连接棒材的最低费用

[力扣](https://leetcode.cn/problems/minimum-cost-to-connect-sticks/)

非常标准的哈夫曼树构造问题，最直观的思路就是每次选择当前剩下棒子中最短的两根合并，重复此过程直到完成合并。

这个算法是正确的，但是证明起来是非常麻烦的，在这里就不展开了。具体代码实现上，可以使用一个堆来维护当前剩下的棒子，每一轮都从中取出堆顶的两根棒子，相加后更新答案并将这根合并后的棒子重新加入到堆中。重复此过程直到堆中剩余一根棒子为止。

最后附上python代码：

```python
class Solution(object):
    def connectSticks(self, sticks):
        """
        :type sticks: List[int]
        :rtype: int
        """

        res = 0
        heapq.heapify(sticks)

        while len(sticks) > 1:
            first = heapq.heappop(sticks)
            second = heapq.heappop(sticks)
            first += second
            res += first
            heapq.heappush(sticks, first)
        
        return res
```
