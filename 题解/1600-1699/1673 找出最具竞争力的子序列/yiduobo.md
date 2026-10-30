---
title: "1673. 找出最具竞争力的子序列"
aliases: ["yiduobo的每日leetcode 1673.找出最具竞争力的子序列"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/stack", "leetcode/greedy", "题单/单调栈", "题单/单调栈/四-最小字典序"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/444023653"
zhihu_id: "444023653"
zhihu_title: "yiduobo的每日leetcode 1673.找出最具竞争力的子序列"
question_id: "1673"
question: "找出最具竞争力的子序列"
problem_url: "https://leetcode.cn/problems/find-the-most-competitive-subsequence/"
difficulty: "Medium"
rating: 1802
created: "2021-12-11T14:29:03+08:00"
updated: "2021-12-11T14:29:04+08:00"
upvotes: 1
comments: 0
---

# 1673. 找出最具竞争力的子序列

> **[yiduobo的每日leetcode 1673.找出最具竞争力的子序列](https://zhuanlan.zhihu.com/p/444023653) · 知乎 · 2021-12-11 · 赞同 1**
> 力扣：[1673. 找出最具竞争力的子序列](https://leetcode.cn/problems/find-the-most-competitive-subsequence/) · Medium · 灵茶山艾府：[跟着我过一遍示例 2，你就明白怎么做了（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1673.找出最具竞争力的子序列

[力扣](https://leetcode-cn.com/problems/find-the-most-competitive-subsequence/)

由于题目要求的是字典序最小的序列，那么自然是希望将小的数放到序列的前面。另外这里有长度为k的限制，因此也不能无脑将小的数放在序列的前面，因为这样的话可能导致凑不出k个数的序列。

总结一下，就是在保证剩余数字充足的前提下，答案序列满足单调递增。那么可以从头开始向后一趟扫描，使用单调栈来维护当前的答案序列。

对于当前位置上的数，若其小于栈顶元素，且后续的剩余数字充足，那么就将栈顶元素弹出。重复此过程直到栈为空，或者其大于栈顶元素，又或者剩余的数字不足了为止。这里剩余数字充足指的是弹出栈顶元素后，栈中序列的长度加上剩下的所有数字至少有k个。

接下来将这个数压入栈中，然后继续向后扫描即可。

扫描完成后，栈底的k个元素就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def mostCompetitive(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: List[int]
        """

        stack = []
        n = len(nums)
        for index in range(n):
            while stack and nums[stack[-1]] > nums[index] and len(stack) - 1 + n - index >= k:
                stack.pop()
            stack.append(index)
        
        while len(stack) > k:
            stack.pop()
        
        return [nums[index] for index in stack]
```
