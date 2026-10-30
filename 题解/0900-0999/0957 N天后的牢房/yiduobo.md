---
title: "957. N天后的牢房"
aliases: ["yiduobo的每日leetcode 957.N天后的牢房"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/360360322"
zhihu_id: "360360322"
zhihu_title: "yiduobo的每日leetcode 957.N天后的牢房"
question_id: "957"
question: "N天后的牢房"
problem_url: "https://leetcode.cn/problems/prison-cells-after-n-days/"
created: "2021-03-27T17:04:35+08:00"
updated: "2021-03-27T17:04:35+08:00"
upvotes: 0
comments: 0
---

# 957. N天后的牢房

> **[yiduobo的每日leetcode 957.N天后的牢房](https://zhuanlan.zhihu.com/p/360360322) · 知乎 · 2021-03-27 · 赞同 0**
> 力扣：[957. N天后的牢房](https://leetcode.cn/problems/prison-cells-after-n-days/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

957.N天后的牢房

[力扣](https://leetcode-cn.com/problems/prison-cells-after-n-days/)

乍一看这个N最多到10^9很吓人，但是仔细观察可以发现，从第1天开始，两侧的两间牢房就必然为0了，而剩下的6间牢房要么为0要么为1，也就是说之后任意一天牢房的状态撑死了也就2^6 \= 32种。

于是我们可以将这些状态进行二进制编码，然后预处理出各种状态之间是如何转化的。换言之，如果将每种状态看做图中的一个点，将转化关系看做图中的一条有向边，那么就可以得到一个32个点，每个点仅有一条出边的有向图，图中也可能存在环。接下来我们要从某个状态开始，在图中沿有向边开始向前走，一共走N步。那么我们可以先找出图中的环，一旦我们走到了某个环上，就可以将N对环长度取模，然后再走完余数的路程即可。

到达终点后，反向解码出牢房的状态即为最终答案。

我在具体实现时并没有预处理，而是使用一个字典step记录之前出现过的状态，以及该状态在第几天第一次出现，然后再使用一个队列q记录下每一天的状态。若某一天now走到了之前出现过的某个状态state，那么now - step[state]就是环的长度，而最终答案也必然出现在q当中，通过环的长度计算出余数，那么step[state]加上余数就是最终答案在队列q中的位置。

最后附上python代码：

```python
class Solution(object):
    def prisonAfterNDays(self, cells, n):
        """
        :type cells: List[int]
        :type n: int
        :rtype: List[int]
        """

        pow2 = [1, 2, 4, 8, 16, 32]

        now = 0
        for i in range(1, 7):
            if cells[i - 1] == cells[i + 1]:
                now += pow2[i - 1]
        
        q = [now]
        step = {now : 1}
        rnd = 1
        while rnd < n:
            now = q[-1]
            rnd += 1
            now_cell = [0] * 6
            for i in range(6):
                if now & pow2[i]:
                    now_cell[i] = 1

            next_cell = []
            for i in range(6):
                if i == 0:
                    next_cell.append(1 - now_cell[1])
                elif i == 5:
                    next_cell.append(1 - now_cell[4])
                elif now_cell[i - 1] == now_cell[i + 1]:
                    next_cell.append(1)
                else:
                    next_cell.append(0)
            
            next = 0
            for i in range(6):
                next += next_cell[i] * pow2[i]

            if next in step:
                start_rnd = step[next]
                loop_len = rnd - start_rnd
                final_state = q[start_rnd - 1 + (n - start_rnd) % loop_len]
                final_cell = [0] * 6
                for i in range(6):
                    if final_state & pow2[i]:
                        final_cell[i] = 1
                return [0] + final_cell + [0]
        
            q.append(next)
            step[next] = rnd

        final_state = q[-1]
        final_cell = [0] * 6
        for i in range(6):
            if final_state & pow2[i]:
                final_cell[i] = 1
        return [0] + final_cell + [0]
```
