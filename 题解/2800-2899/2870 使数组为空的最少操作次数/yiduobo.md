---
title: "2870. 使数组为空的最少操作次数"
aliases: ["yiduobo的每日leetcode 2870.使数组为空的最少操作次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "题单/贪心算法", "题单/贪心算法/四-数学贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/662327591"
zhihu_id: "662327591"
zhihu_title: "yiduobo的每日leetcode 2870.使数组为空的最少操作次数"
question_id: "2870"
question: "使数组为空的最少操作次数"
problem_url: "https://leetcode.cn/problems/minimum-number-of-operations-to-make-array-empty/"
difficulty: "Medium"
rating: 1392
created: "2023-10-20T03:55:25+08:00"
updated: "2023-10-20T03:55:25+08:00"
upvotes: 0
comments: 0
---

# 2870. 使数组为空的最少操作次数

> **[yiduobo的每日leetcode 2870.使数组为空的最少操作次数](https://zhuanlan.zhihu.com/p/662327591) · 知乎 · 2023-10-20 · 赞同 0**
> 力扣：[2870. 使数组为空的最少操作次数](https://leetcode.cn/problems/minimum-number-of-operations-to-make-array-empty/) · Medium · 灵茶山艾府：[贪心+简洁写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2870.使数组为空的最少操作次数

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/minimum-number-of-operations-to-make-array-empty/)

题目中的操作只能针对相同的数字进行，也就是说不同数字应该分开考虑，尽量用最少的次数删去每一种数字然后将所有操作次数累加起来作为答案。

对于单个数字，不妨设其出现了k次。为了使得操作次数最少，那么就应该尽量执行删3操作，在这里就需要对k模3的结果进行讨论。

当k是3的倍数时，应该全部执行删3操作，此时的操作数为k / 3。

当k模3余1时，若k本来就是1，那么此时无法进行任何操作，直接返回-1，否则的话就可以拿一个3出来，配合这个余下的1得到4，然后执行两次删2操作，此时的操作数为k / 3 - 1 + 2 \= k / 3 + 1。

当k模3余2时，则只需执行一次删2操作，然后剩下的全部执行删3操作，此时的操作数为k / 3 + 1。

到了这里，就只需要一趟遍历，统计每种数字出现的次数，然后根据上面的结论计算删去每种数字所需的最少次数并累加到答案中即可。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        freq = {}
        for v in nums:
            freq[v] = freq.get(v, 0) + 1
        
        res = 0
        for v in freq:
            if freq[v] == 1:
                return -1
            else:
                res += freq[v] /3
                if freq[v] % 3 != 0:
                    res += 1
        
        return res
```
