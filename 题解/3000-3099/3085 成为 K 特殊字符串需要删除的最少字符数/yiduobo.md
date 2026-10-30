---
title: "3085. 成为K特殊字符串需要删除的最少字符数"
aliases: ["yiduobo的每日leetcode 3085.成为K特殊字符串需要删除的最少字符数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/sliding-window", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/698673134"
zhihu_id: "698673134"
zhihu_title: "yiduobo的每日leetcode 3085.成为K特殊字符串需要删除的最少字符数"
question_id: "3085"
question: "成为 K 特殊字符串需要删除的最少字符数"
problem_url: "https://leetcode.cn/problems/minimum-deletions-to-make-string-k-special/"
difficulty: "Medium"
rating: 1765
created: "2024-05-20T00:00:47+08:00"
updated: "2024-05-20T00:00:47+08:00"
upvotes: 1
comments: 0
---

# 3085. 成为K特殊字符串需要删除的最少字符数

> **[yiduobo的每日leetcode 3085.成为K特殊字符串需要删除的最少字符数](https://zhuanlan.zhihu.com/p/698673134) · 知乎 · 2024-05-20 · 赞同 1**
> 力扣：[3085. 成为 K 特殊字符串需要删除的最少字符数](https://leetcode.cn/problems/minimum-deletions-to-make-string-k-special/) · Medium · 灵茶山艾府：[先枚举，再贪心 + 滑动窗口优化（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3085.成为K特殊字符串需要删除的最少字符串

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-deletions-to-make-string-k-special/description/)

使用数组freq_list记录每种字符出现的次数，接下来从中枚举特殊字符串中字符的最小频率mi，也就是说这个字符串中的所有字符出现频率都必须出现在mi到mi + k之间。对于当前的mi，再枚举freq_list中的每种频率。若当前的频率x小于mi，那么就只能将x对应的这种字符全部删掉，需要将x累加到代价中；若x大于mi + k，那么就需要将x对应的这种字符减少到只剩下mi + k个，需要将x - (mi + k)累加到代价中。遍历完成后，使用当前代价更新答案，然后继续枚举下一种mi即可。

最后附上python代码：

```python
class Solution(object):
    def minimumDeletions(self, word, k):
        """
        :type word: str
        :type k: int
        :rtype: int
        """

        freq_list = Counter(word).values()
        res = None
        for mi in freq_list:
            cost = 0
            for x in freq_list:
                if x < mi:
                    cost += x
                elif x > mi + k:
                    cost += x - (mi + k)
            
            if res is None or res > cost:
                res = cost
        
        return res
```
