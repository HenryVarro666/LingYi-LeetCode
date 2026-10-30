---
title: "3801. 合并有序列表的最小成本"
aliases: ["yiduobo的每日leetcode 3801.合并有序列表的最小成本"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/two-pointers", "leetcode/binary-search", "leetcode/dynamic-programming", "leetcode/meet-in-the-middle", "题单/链表-二叉树与回溯", "题单/动态规划", "题单/链表-二叉树与回溯/四-回溯", "题单/动态规划/九-状态压缩-DP-状压-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1992290954913276086"
zhihu_id: "1992290954913276086"
zhihu_title: "yiduobo的每日leetcode 3801.合并有序列表的最小成本"
question_id: "3801"
question: "合并有序列表的最小成本"
problem_url: "https://leetcode.cn/problems/minimum-cost-to-merge-sorted-lists/"
difficulty: "Hard"
rating: 2399
created: "2026-01-09T22:11:18+08:00"
updated: "2026-01-09T22:11:19+08:00"
upvotes: 1
comments: 0
---

# 3801. 合并有序列表的最小成本

> **[yiduobo的每日leetcode 3801.合并有序列表的最小成本](https://zhuanlan.zhihu.com/p/1992290954913276086) · 知乎 · 2026-01-09 · 赞同 1**
> 力扣：[3801. 合并有序列表的最小成本](https://leetcode.cn/problems/minimum-cost-to-merge-sorted-lists/) · Hard · 灵茶山艾府：[子集状压 DP + 合并有序数组 / 二分中位数 / meet in the middle](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3801.合并有序列表的最小成本

[3801. 合并有序列表的最小成本 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-cost-to-merge-sorted-lists/description/)

题目给出一个二维整数数组lists，其中每个lists[index]都是一个非递减的非空整数数组。lists的长度不超过12。

现在需要重复执行以下操作若干次。

每次操作，需要从所有剩余的列表中选择两个列表a和b，将它们合并。合并a和b的成本为len(a) + len(b) + abs(median(a) - median(b))，其中len和median分别表示列表的长度以及中位数。若列表长度为偶数，那么中位数取其左侧的中间元素。

重复以上操作，直到所有列表都合并成一个列表为止。

问合并所需的最小总成本是多少。

非常标准的状态压缩动态规划问题。令f[state]表示将状态表示为state的列表合并到一起的最小成本，那么对于f[state]，若state是2的幂次，说明其是一个单独的列表，那么就有f[state] \= 0，否则可以枚举state的所有子状态sub，那么就有f[state] \= min(f[sub] + f[state ^ sub] + len[sub] + len[state ^ sub] + abs(median[sub] - median[state ^ sub]))。

其中len[state]和median[state]分别表示状态表示为state的列表合并到一起后得到的列表，对应的长度以及中位数。由于列表本身不会变化，因此在一开始可以提前预处理出所有的len以及median。

len是很容易计算的，对于len[state]，若state是2的幂次，那么len[state]就是其对应的原生列表的长度，否则可以选择state的任意子状态sub，通过len[sub] + len[state ^ sub]得到len[state]。

而对于median的计算则稍微复杂一点。由于无法保存具体的合并后的列表，因此无法直接通过median[sub]以及median[state ^ sub]来得到median[state]，只能每次都重新计算。不过注意到lists中的原始列表都是非递减的，因此在这里可以通过二分套二分来计算。

具体来说，先二分state对应的中位数v，接下来让v在state中的每个原始列表中二分，计算每个原始列表中有多少个元素小于等于v，并将其累加到cnt中。若最终的cnt足够len[state]的一半，说明v足够大，此时应该调整v二分的上界为v，否则需要调整v二分的下降为v + 1。

得到len和median后，执行上面的状态压缩动态规划，最终答案就是f[-1]。

最后附上python代码：

```python
class Solution(object):
    def minMergeCost(self, lists):
        """
        :type lists: List[List[int]]
        :rtype: int
        """
        
        n = len(lists)
        max_state = (1 << n)

        length = [None] * max_state
        median = [None] * max_state

        f = [None] * max_state
        for index in range(n):
            state = (1 << index)
            f[state] = 0
            length[state] = len(lists[index])
            median[state] = lists[index][(len(lists[index]) - 1) // 2]

        for state in range(1, max_state):
            if f[state] is None:
                sub = state & (state - 1)
                length[state] = length[sub] + length[state ^ sub]

                while sub > (state ^ sub):
                    cost = f[sub] + f[state ^ sub] + abs(median[sub] - median[state ^ sub])
                    if f[state] is None or f[state] > cost:
                        f[state] = cost
                    sub = (sub - 1) & state
                
                f[state] += length[state]

                lo = None
                hi = None
                ll = []
                for index in range(n):
                    if state & (1 << index):
                        ll.append(index)
                        if lo is None or lo > lists[index][0]:
                            lo = lists[index][0]
                        if hi is None or hi < lists[index][-1]:
                            hi = lists[index][-1]
                
                k = (length[state] + 1) // 2
                while lo < hi:
                    v = (lo + hi) // 2
                    cnt = 0
                    for index in ll:
                        if v < lists[index][0]:
                            continue

                        left = 0
                        right = len(lists[index]) - 1
                        while left < right:
                            mid = (left + right + 1) // 2
                            if lists[index][mid] <= v:
                                left = mid
                            else:
                                right = mid - 1

                        cnt += left + 1
                        if cnt >= k:
                            break
                    
                    if cnt >= k:
                        hi = v
                    else:
                        lo = v + 1
                
                median[state] = lo
        
        return f[-1]
```
