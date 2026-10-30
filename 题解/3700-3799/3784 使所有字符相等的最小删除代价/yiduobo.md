---
title: "3784. 使所有字符相等的最小删除代价"
aliases: ["yiduobo的每日leetcode 3784.使所有字符相等的最小删除代价"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1986227099372102285"
zhihu_id: "1986227099372102285"
zhihu_title: "yiduobo的每日leetcode 3784.使所有字符相等的最小删除代价"
question_id: "3784"
question: "使所有字符相等的最小删除代价"
problem_url: "https://leetcode.cn/problems/minimum-deletion-cost-to-make-all-characters-equal/"
difficulty: "Medium"
created: "2025-12-25T02:08:15+08:00"
updated: "2025-12-25T02:08:20+08:00"
upvotes: 1
comments: 0
---

# 3784. 使所有字符相等的最小删除代价

> **[yiduobo的每日leetcode 3784.使所有字符相等的最小删除代价](https://zhuanlan.zhihu.com/p/1986227099372102285) · 知乎 · 2025-12-25 · 赞同 1**
> 力扣：[3784. 使所有字符相等的最小删除代价](https://leetcode.cn/problems/minimum-deletion-cost-to-make-all-characters-equal/) · Medium · 灵茶山艾府：[按照相同字母分组（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3784.使所有字符相等的最小删除代价

[3784. 使所有字符相等的最小删除代价 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-deletion-cost-to-make-all-characters-equal/)

题目给出一个长度为n的字符串s以及一个整数数组cost，其中cost[index]表示删除s[index]所需的代价。

现在要求从s中删除掉一些字符，使得剩下的s非空，且仅有相同的字符组成。

问最小的总删除代价为多少。

由于最终s中只能保留一种字符，那么最优的处理方法必然选择一种字符，保留所有的该字符，然后删掉其他的字符，那么总的删除代价就是删除所有字符的总代价，减去删除保留的字符的总代价。

于是只需一趟遍历，使用哈希表记录删除掉每种字符需要的代价，同时使用一个变量记录删除所有字符所需的总代价，那么最终答案就是总代价，减去哈希表中value的最大值。

最后附上python代码：

```python
class Solution(object):
    def minCost(self, s, cost):
        """
        :type s: str
        :type cost: List[int]
        :rtype: int
        """
        
        su = {}
        tot = 0
        for ch, co in zip(s, cost):
            su[ch] = su.get(ch, 0) + co
            tot += co
        
        return tot - max(su.values())
```
