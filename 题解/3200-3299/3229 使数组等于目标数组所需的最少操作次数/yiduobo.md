---
title: "3229. 使数组等于目标数组所需的最少操作次数"
aliases: ["yiduobo的每日leetcode 3229.使数组等于目标数组所需的最少操作次数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "题单/常用数据结构", "题单/常用数据结构/二-差分"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/720234406"
zhihu_id: "720234406"
zhihu_title: "yiduobo的每日leetcode 3229.使数组等于目标数组所需的最少操作次数"
question_id: "3229"
question: "使数组等于目标数组所需的最少操作次数"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-make-array-equal-to-target/"
difficulty: "Hard"
rating: 2067
created: "2024-09-14T21:49:24+08:00"
updated: "2024-09-14T21:49:24+08:00"
upvotes: 1
comments: 5
---

# 3229. 使数组等于目标数组所需的最少操作次数

> **[yiduobo的每日leetcode 3229.使数组等于目标数组所需的最少操作次数](https://zhuanlan.zhihu.com/p/720234406) · 知乎 · 2024-09-14 · 赞同 1**
> 力扣：[3229. 使数组等于目标数组所需的最少操作次数](https://leetcode.cn/problems/minimum-operations-to-make-array-equal-to-target/) · Hard · 灵茶山艾府：[差分数组（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3229.使数组等于目标数组所需的最少操作次数

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-operations-to-make-array-equal-to-target/description/)

题目给出两个长度相同的正整数数组nums和target，对于每次操作，可以将nums的任意子数组加上1或者减去1，问至少需要多少次操作才能使得nums等于target。

首先可以将nums与target逐位相减，得到新的diff数组，那么问题就转化成了给出一个有正有负的数组diff，每次操作可以将diff的任意子数组加上1或者减去1，问至少需要多少次操作才能将diff数组变为全0。

接下来可以明确的是，不应该对一个既有正数又有负数的子数组执行操作，例如[3, -1, 3]，如果全体执行3次减1操作，那么就需要3次加1操作才能使得-1复原，相当于执行了两倍的操作，这与在正数的部分分别执行3次减1操作所需的的操作次数是相同的。

更进一步的，如果执行操作的数组中有k段不相邻的负数，且当前执行了x次减1的操作，那么就需要k \* x次加1操作才能将这些负数扳回来。另一方面，这k段不相邻的负数可以将子数组划分成k + 1段不相邻的正数，直接对这些正数执行(k + 1) \* x次操作的效果是一样的。

根据这个结论，就可以将diff划分成若干段全正或者全负的子数组，然后分别对这些子数组进行求解。

接下来讨论如果处理全正的子数组，全负的子数组的处理方法是完全对称的。

对于一个子数组diff[i : j]，首先将diff[i]变为0就至少需要在i这个位置上执行diff[i]次操作，接下来对于diff[i + 1]，如果diff[i + 1] \<\= diff[i]，那么就可以喝到diff[i]的汤，不需要执行任何操作，反之则至少需要额外补充diff[i + 1] - diff[i]次操作。更进一步的，对于后续所有的diff[p]与diff[p - 1]，若diff[p]更大，那么就需要额外补充操作，否则就可以依靠在diff[p - 1]上执行的操作来达成diff[p]。

最后附上python代码：

```python
class Solution(object):
    def minimumOperations(self, nums, target):
        """
        :type nums: List[int]
        :type target: List[int]
        :rtype: int
        """

        diff = [x - y for x, y in zip(nums, target)]
        p = 0
        res = 0

        def calc(start, end):
            p = start
            res = abs(diff[p])
            for index in range(p + 1, q):
                if abs(diff[index]) > abs(diff[index - 1]):
                    res += abs(diff[index]) - abs(diff[index - 1])
            
            return res

        while p < len(diff):
            while p < len(diff) and diff[p] == 0:
                p += 1
            
            if p == len(diff):
                break
            
            if diff[p] > 0:
                q = p + 1
                while q < len(diff) and diff[q] > 0:
                    q += 1
            else:
                q = p + 1
                while q < len(diff) and diff[q] < 0:
                    q += 1

            res += calc(p, q)
            p = q
        
        return res
```
