---
title: "1687. 从仓库到码头运输箱子"
aliases: ["yiduobo的每日leetcode 1687.从仓库到码头运输箱子"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/446379870"
zhihu_id: "446379870"
zhihu_title: "yiduobo的每日leetcode 1687.从仓库到码头运输箱子"
question_id: "1687"
question: "从仓库到码头运输箱子"
problem_url: "https://leetcode.cn/problems/delivering-boxes-from-storage-to-ports/"
created: "2021-12-17T00:22:56+08:00"
updated: "2021-12-17T00:22:57+08:00"
upvotes: 0
comments: 0
---

# 1687. 从仓库到码头运输箱子

> **[yiduobo的每日leetcode 1687.从仓库到码头运输箱子](https://zhuanlan.zhihu.com/p/446379870) · 知乎 · 2021-12-17 · 赞同 0**
> 力扣：[1687. 从仓库到码头运输箱子](https://leetcode.cn/problems/delivering-boxes-from-storage-to-ports/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1687.从仓库到码头运输箱子

[力扣](https://leetcode-cn.com/problems/delivering-boxes-from-storage-to-ports/)

朴素动态规划的做法是很容易想到的。令f[i]表示前i个箱子所需要的最少运输次数，那么对于f[i]，若0到i - 1之间的某个j满足i - j \<\= maxBoxes，且weight[j + 1] + weight[j + 2] + ... + weight[i] \<\= maxWeight，就可以将j + 1到i这些箱子一次性装车运输。此时就有

f[i] \= min(f[i], f[j] + cost(j + 1, i))

其中cost表示将j + 1到i这些箱子一次性装车运输所需的代价。

这里一共有两个地方需要想办法得到，一个是左边界j的值，另一个是cost(j + 1, i)的值。接下来分别讨论这两个地方：

首先是j的值。

注意到随着i的向后移动，j也必然是跟着向后移动的，因此可以使用滑动窗口的思路，维护一个当前可同时装车的区间，并随着i的向后移动调整区间的左边界。而对于j的两个条件，其中i - j \<\= maxBoxes是比较好判断的，而对于weight[j + 1] + weight[j + 2] + ... + weight[i]这个式子，由于其是一个区间和的式子，那么可以预处理出前缀和w_s，对应的结果就是w_s[i] - w_s[j]。

接下来考虑如何求解cost(j + 1, i)。

对于cost(j + 1, i)，首先单独运输第j + 1件货物需要来回一共两趟。

接下来考虑之后的j + 2。如果其目的地与j + 1相同，那么此时不会产生额外的运输次数，否则需要额外从j + 1到目的地到j + 2的目的地走一趟，对应的就是运输趟数需要加上1。也就是说若port[j + 2] \= port[j + 1]，那么cost(j + 2, i) \= cost(j + 1, i)，否则cost(j + 2, i) \= cost(j + 1, i) + 1。

更一般的，若j + 1到i之间存在某个k，满足port[k] !\= port[k + 1]，那么在运输完k之后需要一趟额外的行程从port[k]走到port[k + 1]来完成k + 1的运输。也就是说，cost(j + 1, i)实际上记录的就是从j + 1到i之间位置相邻但目的地不同的货物，因此只需要计算出这个值，再加上最开始出发以及最后返回的两趟就是最终的cost(j + 1, i)

这同样是一个区间问题，那么也可以用类似前缀和的思路求解。

令cnt[i]表示0到i之间有多少对相邻但目的地不同的货物，对于cnt[i]而言，若port[i] \= port[i - 1]。那么就有cnt[i] \= cnt[i - 1]，否则cnt[i] \= cnt[i - 1] + 1

而对于cost(j + 1, i)，则有cost(j + 1, i) \= cnt[i] - cnt[j] + 2，这里的2表示最开始出发以及最后返回这两趟。

直到了j和cost(j +1, i)的求法，就大致得出了一种可行的做法，但是由于状态转移的复杂度为O(n)，那么实际上这是一个O(n^2)的做法，在题目给出的数据规模下肯定是行不通的。

在观察状态转移方程f[i] \= min(f[i], f[j] + cost(j + 1, i))，如果用cnt带入cost，那么就有

f[i] \= min(f[i], f[j] + cnt[i] - cnt[j] + 2)

可以发现，这里f[j] + cnt[i] - cnt[j] + 2这个式子当中cnt[i]和2都已经固定住了，实际上要找的就是区间中最小的f[j] - cnt[j]。这个区间最值问题当然可以各种logn级的数据结构来解决例如线段树，不过在这里采用单调栈是更好的做法。

不妨设现在存在两个位置p和q，满足p \< q且f[p] - cnt[p] >\= f[q] - cnt[q]，那么p这个位置就不可能再去更新后续的状态了，因为p \< q，所以若p在可行的区间内，那么q也必然在可行的区间内。另外观察状态转移方程，如果通过p来更新i那么代价为f[p] - cnt[p] + cnt[i] + 2，而通过q来更新则为f[q] - cnt[q] + cnt[i] + 2，由于这里f[p] - cnt[p] \<\= f[q] - cnt[q]，那么通过q来更新的结果必然不必通过p来更新更差，因此后续的更新就无须再考虑p这个位置了。

根据这个结论，在更新的过程中可以维护一个单调栈，其中越靠近栈底就越靠前，但对应的f - cnt就越小。另外，由于确定可行区间是一个滑动窗口，那么与之结合之后就变成了一个双向队列。

那么现在的做法就是从头开始向后一趟扫描，对于f[index]：

1、首先考察双向队列的队首位置是否已经超出了当前可行区间的左边界，主要检测两点。第一个是当前位置index - deque\[0\]是否小于等于maxBoxes，第二个是w_s\[index\] - w_s\[deque\[0\]\]是否小于等于maxWeight，若其中一个不满足，说明deque\[0\]以及不在合法区间内，那么将其弹出队列，然后继续检测新的deque\[0\]，直到满足上面两个条件或者双向队列为空。

2、接下来更新f\[index\]。首先初始化f\[index\] \= f\[index - 1\] + 2，表示第index件货物单独装车。接下来若deque不为空，那么根据定义，合法区间内f\[deque\[0\]\] - cnt\[deque\[0\]\]是最小的，因此还可以使用f\[deque\[0\]\] + cnt\[index\] - cnt\[deque\[0\]\] + 2来更新f\[index\]。

3、接下来使用f\[index\] - cnt\[index\]来更新deque。若此时的f\[index\] - cnt\[index\] \<\= f\[deque\[-1\]\] - cnt\[deque\[-1\]\]，说明此时双向队列的尾部代表的位置已经没用了，那么将其弹出队列，然后检测新的队尾位置。重复这个过程直到不满足上面的不等式，或者双向队列为空。最后还需要将index加入到队列的尾部。

扫描完成后，f[-1]就是最终答案。

此时状态转移的复杂度为O(1)，而每个位置最多进出双向队列一次，因此均摊下来也是O(1)，所以最终的时间复杂度就从O(n^2)优化到了O(n)。

最后附上python代码：

```python
class Solution(object):
    def boxDelivering(self, boxes, portsCount, maxBoxes, maxWeight):
        """
        :type boxes: List[List[int]]
        :type portsCount: int
        :type maxBoxes: int
        :type maxWeight: int
        :rtype: int
        """

        cnt = [0]
        w_s = [0]
        n = len(boxes)
        for index in range(n):
            cnt.append(cnt[-1])
            if index > 0 and boxes[index][0] != boxes[index - 1][0]:
                cnt[-1] += 1
            
            w_s.append(w_s[-1] + boxes[index][1])

        cnt.append(cnt[-1])

        f = [0]
        stack = [0]
        l = 0
        for index in range(n):
            while l < len(stack) and (index + 1 - stack[l] > maxBoxes or w_s[index + 1] - w_s[stack[l]] > maxWeight):
                l += 1

            f.append(f[-1] + 2)
            if l < len(stack):
                f[-1] = min(f[-1], f[stack[l]] + cnt[index + 1] - cnt[stack[l] + 1] + 2)

            while len(stack) > l and f[stack[-1]] - cnt[stack[-1] + 1] >= f[-1] - cnt[index + 2]:
                stack.pop()
            
            stack.append(index + 1)

        return f[-1]
```
