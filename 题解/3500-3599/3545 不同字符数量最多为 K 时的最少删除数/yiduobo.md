---
title: "3545. 不同字符数量最多为K时的最少删除数"
aliases: ["yiduobo的每日leetcode 3545.不同字符数量最多为K时的最少删除数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1907606559351083140"
zhihu_id: "1907606559351083140"
zhihu_title: "yiduobo的每日leetcode 3545.不同字符数量最多为K时的最少删除数"
question_id: "3545"
question: "不同字符数量最多为 K 时的最少删除数"
problem_url: "https://leetcode.cn/problems/minimum-deletions-for-at-most-k-distinct-characters/"
difficulty: "Easy"
rating: 1211
created: "2025-05-21T22:06:13+08:00"
updated: "2025-05-21T22:06:13+08:00"
upvotes: 0
comments: 0
---

# 3545. 不同字符数量最多为K时的最少删除数

> **[yiduobo的每日leetcode 3545.不同字符数量最多为K时的最少删除数](https://zhuanlan.zhihu.com/p/1907606559351083140) · 知乎 · 2025-05-21 · 赞同 0**
> 力扣：[3545. 不同字符数量最多为 K 时的最少删除数](https://leetcode.cn/problems/minimum-deletions-for-at-most-k-distinct-characters/) · Easy · 灵茶山艾府：[从小到大贪心，简洁写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3545.不同字符数量最多为K时的最少删除数

[3545. 不同字符数量最多为 K 时的最少删除数 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-deletions-for-at-most-k-distinct-characters/description/)

题目给出一个由小写字符组成的字符串s以及一个整数k。现在要求从中删去一些字符，是的结果字符串中不同字符的数量最多为k。

问最少需要删掉多少个字符。

题目要求删去尽量少的字符，那么就应该保留出现次数最多的k种字符，于是可以先一趟遍历，使用哈希表统计每种字符出现的次数，然后将这些次数从大到小进行排序，使用s的长度减去这些次数中最大的k个即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def minDeletion(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: int
        """
        
        freq = {}
        for char in s:
            freq[char] = freq.get(char, 0) + 1
        
        return len(s) - sum(sorted(freq.values(), reverse=True)[:k])
```
