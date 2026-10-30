---
title: "3160. 所有球里面不同颜色的数目"
aliases: ["yiduobo的每日leetcode 3160.所有球里面不同颜色的数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/704568244"
zhihu_id: "704568244"
zhihu_title: "yiduobo的每日leetcode 3160.所有球里面不同颜色的数目"
question_id: "3160"
question: "所有球里面不同颜色的数目"
problem_url: "https://leetcode.cn/problems/find-the-number-of-distinct-colors-among-the-balls/"
difficulty: "Medium"
created: "2024-06-20T23:48:42+08:00"
updated: "2024-06-20T23:48:42+08:00"
upvotes: 1
comments: 0
---

# 3160. 所有球里面不同颜色的数目

> **[yiduobo的每日leetcode 3160.所有球里面不同颜色的数目](https://zhuanlan.zhihu.com/p/704568244) · 知乎 · 2024-06-20 · 赞同 1**
> 力扣：[3160. 所有球里面不同颜色的数目](https://leetcode.cn/problems/find-the-number-of-distinct-colors-among-the-balls/) · Medium · 灵茶山艾府：[哈希表模拟（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3160.所有球里面不同颜色的数目

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-number-of-distinct-colors-among-the-balls/description/)

题目给出limit + 1个球以及一个二维数组queries。最开始这limit + 1个球都是无色的，接下来对于queries中的每次操作[x, y]，会将第x个球染成颜色y，问每次操作后不同颜色的球的数目。无色的球不计算颜色。

题目要求修改球的颜色，那么就需要使用一个哈希表color来记录每个球是什么颜色。另一方面，题目需要计算的是颜色的种数，也就是说有多少种颜色出现的次数大于等于1次，那么就还需要使用另一个哈希表freq记录每种颜色当前出现了多少次。

对于每个\[x, y\]，若x目前有颜色，就应该将freq\[color\[x\]\]减去1，若freq\[color\[x\]\]等于0，说明当前没有color\[x\]这种颜色的球，需要将其从freq中删去。接下来将color\[x\]置为y，然后将freq\[color\[x\]\]加上1，而此时不同颜色的数目就是freq的长度。

最后附上python代码：

```python
class Solution(object):
    def queryResults(self, limit, queries):
        """
        :type limit: int
        :type queries: List[List[int]]
        :rtype: List[int]
        """

        color = {}
        freq = {}
        res = []
        for x, y in queries:
            if x in color:
                freq[color[x]] -= 1
                if freq[color[x]] == 0:
                    freq.pop(color[x])
            
            color[x] = y
            freq[color[x]] = freq.get(color[x], 0) + 1
            res.append(len(freq))
        
        return res
```
