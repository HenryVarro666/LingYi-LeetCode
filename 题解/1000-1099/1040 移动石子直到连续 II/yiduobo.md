---
title: "1040. 移动石子直到连续II"
aliases: ["yiduobo的每日leetcode 1040.移动石子直到连续II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/two-pointers", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/贪心算法", "题单/滑动窗口与双指针/二-不定长滑动窗口", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/370525958"
zhihu_id: "370525958"
zhihu_title: "yiduobo的每日leetcode 1040.移动石子直到连续II"
question_id: "1040"
question: "移动石子直到连续 II"
problem_url: "https://leetcode.cn/problems/moving-stones-until-consecutive-ii/"
difficulty: "Medium"
rating: 2456
created: "2021-05-07T23:54:21+08:00"
updated: "2021-05-07T23:54:21+08:00"
upvotes: 3
comments: 0
---

# 1040. 移动石子直到连续II

> **[yiduobo的每日leetcode 1040.移动石子直到连续II](https://zhuanlan.zhihu.com/p/370525958) · 知乎 · 2021-05-07 · 赞同 3**
> 力扣：[1040. 移动石子直到连续 II](https://leetcode.cn/problems/moving-stones-until-consecutive-ii/) · Medium · 灵茶山艾府：[【图解】下跳棋（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1040.移动石子直到连续II

[力扣](https://leetcode-cn.com/problems/moving-stones-until-consecutive-ii/)

之前1033题的进阶版，依然是分成最大和最小来进行讨论。

首先需要对stones进行排序，方便后续的计算。

接下来考虑最大的情况：

当前总的区间长度为stones[-1] - stones[0] + 1，其中有len(stones)个格子已经被占用掉了，那么理论上还有stones[-1] - stones[0] + 1 - len(stones)个空位可以使用。

在进行首次移动时，我们可以选择移动stones[0]或者stones[-1]。

若移动stones[0]，为了保有尽量多的空位，那么我们可以将stones[0]移动到stones[1]之后的最近的空位，或者移动到stones[-1]之前的最近的空位。无论如何，从stones[0]到stones[1]之间的空位都将被浪费掉，同时还会使用掉stones[0]新占用的空位。接下来，整个stones的排布就应该是

stones[1]，stones[2]，...，stones[k]，stones[0]，...

其中stones[1]到stones[0]这一段必然是填满了的，那么之后每一次操作，我们都可以从stones[1]开始逐个向后滚动，即先将stones[1]移动到stones[0]之后最近的空位，然后将stones[2]移动到stones[1]之后最近的空位，依次类推。每一轮除了新占用的位置之后都不会额外浪费掉空位，因此这里剩下多少空位，就可以执行多少轮。

那么这里的最大轮次应该是

stones[-1] - stones[0] + 1 - len(stones) - (stones[1] - stones[0] + 1 - 2)

其中后面括号中的部分表示首次移动stones[0]浪费掉的空格数

若移动stones[-1]，与移动stones[0]是完全等价的，那么此时的最大轮次应该是：

stones[-1] - stones[0] + 1 - len(stones) - (stones[-1] - stones[-2] + 1 - 2)

那么总的最大轮次就是二者取最大值

最后还需要考虑最小的情况。

依然是先考察特殊情况：

1、若stones一开始就是连续，那么答案为0

2、若stones是形如样例2这种，只有一个端点不连续，其这个端点与最近点之间的空格数大于1的，那么答案为2

然后再考察一般情况。由于最终结果是一个长度为len(stones)的连续区间，那么我们只要找到一个涵盖最多stones的区间，然后逐个将不再该区间内的stones移动进来即可。这里的移动一定是合法的，因为若该区间两端已经有stones，那么之后的移动都是移动到区间两端之间，必然是可行的。若区间两端还没有stones，则可以先将stones[0]以及stones[-1]移动到区间的两端。由于排除了特殊情况2，因此必然可以处理好区间的两端，然后剩下的移动就都是移动到区间两端之间了

而对于涵盖最多stones区间的求解，则可以是滑动窗口来求解。设最终求得的区间内有k个stones，那么答案为len(stones) - k

最后附上python代码：

```python
class Solution(object):
    def numMovesStonesII(self, stones):
        """
        :type stones: List[int]
        :rtype: List[int]
        """

        stones = sorted(stones)
        n = len(stones)

        ma = stones[-1] - stones[0] + 1 - n - min(stones[1] - stones[0] + 1 - 2, stones[-1] - stones[-2] + 1 - 2)

        if stones[-1] - stones[0] + 1 == n:
            mi = 0
        elif stones[-2] - stones[0] + 1 == (n - 1) and stones[-1] - stones[-2] > 2:
            mi = 2
        elif stones[-1] - stones[1] + 1 == (n - 1) and stones[1] - stones[0] > 2:
            mi = 2
        else:
            mi = ma
            l = r = 0
            while l < n:
                while r + 1 < n and stones[r + 1] - stones[l] + 1 <= n:
                    r += 1
                mi = min(mi, n - (r - l + 1))
                l += 1
        
        return [mi, ma]
```
