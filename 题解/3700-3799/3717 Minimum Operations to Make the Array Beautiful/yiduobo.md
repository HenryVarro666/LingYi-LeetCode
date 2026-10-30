---
title: "3717. Minimum Operations to Make the Array Beautiful"
aliases: ["yiduobo的每日leetcode 3717.Minimum Operations to Make the Array Beautiful"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1963353236963594687"
zhihu_id: "1963353236963594687"
zhihu_title: "yiduobo的每日leetcode 3717.Minimum Operations to Make the Array Beautiful"
question_id: "3717"
question: "Minimum Operations to Make the Array Beautiful"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-make-the-array-beautiful/"
created: "2025-10-19T21:31:36+08:00"
updated: "2025-10-19T21:31:37+08:00"
upvotes: 2
comments: 0
---

# 3717. Minimum Operations to Make the Array Beautiful

> **[yiduobo的每日leetcode 3717.Minimum Operations to Make the Array Beautiful](https://zhuanlan.zhihu.com/p/1963353236963594687) · 知乎 · 2025-10-19 · 赞同 2**
> 力扣：[3717. Minimum Operations to Make the Array Beautiful](https://leetcode.cn/problems/minimum-operations-to-make-the-array-beautiful/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3717.Minimum Operations to Make the Array Beautiful

[3717. Minimum Operations to Make the Array Beautiful - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-operations-to-make-the-array-beautiful/description/)

题目给出一个整数数组nums，其长度不超过100，其中的元素大小在1到50之间。

若一个数组中从下标1开始的所有元素都可以被前一个元素整除，那么就称这个数组为美丽数组。

现在可以通过一次操作，将数组中下标大于等于1的任意元素增加1，问最少需要多少次操作才能使得数组变为美丽数组。

题目的数据规模一开始是两个10^5，而标程一开始给的是贪心算法，从下标1开始，对于每个元素，都通过尽量少的操作将其修正为前一个元素的倍数。这个做法明显是有问题的，例如[3, 8, 12]，按照贪心法得到的数组为[3, 9, 18]，需要7次操作，但是变为[3, 12, 12]只需要4次操作。

比较直观的理解是，无法直接通过策略决定每个元素应该去适配其左侧的元素还是去适配其右侧的元素，因此需要使用动态规划进行求解。

令f[index][x]表示将nums[0]到nums[index]这一段变为美丽数组，且最后这个元素的值为x时需要的最少操作次数，那么对于f[index][x]，需要先找出最小的大于等于nums[index + 1]，且可以被x整除的元素t，接下来从t开始，以步长为x向上迭代，使用f[index][x] + t - v来更新f[index + 1][t]。这里迭代的上限设置为max(nums) + x应该就行了，但是没想到严谨的证明方式。

计算完成后，f[-1]中的最小值即为最终答案。

另外，由于每一列的状态只与上一轮有关，因此可以通过滚动数组省去index这一维。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        ma = max(nums)
        f = {nums[0]: 0}
        for v in nums[1:]:
            g = {}
            for x in f:
                g[x] = f[x]
            f = {}

            for x in g:
                t = x
                while t < v:
                    t += x
                
                while t <= ma + x:
                    cost = g[x] + t - v
                    if t not in f or f[t] > cost:
                        f[t] = cost
                    t += x

        return min(f.values())
```
