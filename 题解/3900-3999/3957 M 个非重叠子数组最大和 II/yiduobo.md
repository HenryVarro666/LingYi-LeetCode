---
title: "3957. M个非重叠子数组最大和II"
aliases: ["yiduobo的每日leetcode 3957.M个非重叠子数组最大和II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/binary-search", "leetcode/dynamic-programming", "leetcode/prefix-sum", "leetcode/monotonic-queue", "题单/动态规划", "题单/动态规划/十一-优化-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2048539326284412487"
zhihu_id: "2048539326284412487"
zhihu_title: "yiduobo的每日leetcode 3957.M个非重叠子数组最大和II"
question_id: "3957"
question: "M 个非重叠子数组最大和 II"
problem_url: "https://leetcode.cn/problems/maximum-sum-of-m-non-overlapping-subarrays-ii/"
difficulty: "Hard"
rating: 2611
created: "2026-06-11T23:08:20+08:00"
updated: "2026-06-11T23:08:23+08:00"
upvotes: 1
comments: 0
---

# 3957. M个非重叠子数组最大和II

> **[yiduobo的每日leetcode 3957.M个非重叠子数组最大和II](https://zhuanlan.zhihu.com/p/2048539326284412487) · 知乎 · 2026-06-11 · 赞同 1**
> 力扣：[3957. M 个非重叠子数组最大和 II](https://leetcode.cn/problems/maximum-sum-of-m-non-overlapping-subarrays-ii/) · Hard · 灵茶山艾府：[拉格朗日松弛（WQS 二分）Python/Java/C++/Go](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3957.M个非重叠子数组最大和II

<https://leetcode.cn/problems/maximum-sum-of-m-non-overlapping-subarrays-ii/description/>

题目给出一个长度为n的整数数组nums，以及三个整数m、l和r，其中n不超过100000，m、l、r均不超过n。

现在要求从nums中选择至少一个，至多m个互不重叠，且长度在[l, r]范围内的子数组。

问所选子数组的总和最大可能是多少。

本题的题设与之前的3956题相同

[yiduobo的每日leetcode 3956.M个非重叠子数组最大和I](https://zhuanlan.zhihu.com/p/2048170834477442248)

但是数据规模大了两个量级，显然无法沿用之前O(mn)的算法。

对于这类有约束的最优化问题，如果能证明原函数的凸性，就可以使用wqs二分来求解。与wqs二分有关的内容比较繁杂，可以参考之前的3929题，这里就不展开了。

[yiduobo的每日leetcode 3929.最小分割分数II](https://zhuanlan.zhihu.com/p/2042013002682159313)

本题的处理方法与3929题类似，不过在这里要求计算的是最大和，因此这里的惩罚项是通过减法的方式加入到转移方程中。具体来说，转移方程在这里就变成了f[p] + s[index] - s[p] - lamb，其中前三项与3956题中使用单调队列优化的动态规划含义完全相同，最后这一项lamb就是惩罚项。

初始状况下，使用lamb \= 0先计算一次无约束的最优解best_f，并记录得到best_f所需的子数组数目cnt。若此时的cnt \<\= m，那么此时的best_f就是最终答案，反之，则需要二分这个lamb，找出最小的，且满足当前得到best_f所需的cnt恰好落在m的lamb，那么最终答案就是best_f - lamb \* m。

最后附上python代码：

```python
class Solution(object):
    def maximumSum(self, nums, m, l, r):
        """
        :type nums: List[int]
        :type m: int
        :type l: int
        :type r: int
        :rtype: int
        """
        
        n = len(nums)
        s = [0]
        for v in nums:
            s.append(s[-1] + v)

        def calc(lamb):
            f = [None] * (n + 1)
            f[0] = 0
            cnt = [0] * (n + 1)

            q = []
            head, tail = 0, 0

            best_f = None
            best_cnt = 0

            for index in range(1, n + 1):
                if head < tail and index - q[head] > r:
                    head += 1

                if index >= l and f[index - l] is not None:
                    while tail > head and f[index - l] - s[index - l] > f[q[-1]] - s[q[-1]]:
                        q.pop()
                        tail -= 1
                    q.append(index - l)
                    tail += 1
                
                f[index] = f[index - 1]
                cnt[index] = cnt[index - 1]
                
                if head < tail:
                    score = f[q[head]] + s[index] - s[q[head]] - lamb
                    if f[index] is None or f[index] < score:
                        f[index] = score
                        cnt[index] = cnt[q[head]] + 1

                    if best_cnt == 0 or best_f < score:
                        best_f = score
                        best_cnt = cnt[q[head]] + 1

            return best_f, best_cnt
        
        res, cnt = calc(0)
        if cnt <= m:
            return res

        left = 1
        right = 10 ** 18
        while left < right:
            mid = (left + right) // 2
            res, cnt = calc(mid)
            if cnt > m:
                left = mid + 1
            else:
                right = mid

        res, cnt = calc(left)

        return res + m * left
```
