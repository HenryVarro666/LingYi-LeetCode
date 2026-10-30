---
title: "3890. 可由多种立方和构造的整数"
aliases: ["yiduobo的每日leetcode 3890.可由多种立方和构造的整数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/binary-search", "leetcode/enumeration", "leetcode/ordered-set", "leetcode/sorting"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2024487617970848770"
zhihu_id: "2024487617970848770"
zhihu_title: "yiduobo的每日leetcode 3890.可由多种立方和构造的整数"
question_id: "3890"
question: "可由多种立方和构造的整数"
problem_url: "https://leetcode.cn/problems/integers-with-multiple-sum-of-two-cubes/"
difficulty: "Medium"
created: "2026-04-06T14:08:45+08:00"
updated: "2026-04-06T14:08:46+08:00"
upvotes: 2
comments: 0
---

# 3890. 可由多种立方和构造的整数

> **[yiduobo的每日leetcode 3890.可由多种立方和构造的整数](https://zhuanlan.zhihu.com/p/2024487617970848770) · 知乎 · 2026-04-06 · 赞同 2**
> 力扣：[3890. 可由多种立方和构造的整数](https://leetcode.cn/problems/integers-with-multiple-sum-of-two-cubes/) · Medium · 灵茶山艾府：[枚举 + 计数（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3890.可由多种立方和构造的整数

<https://leetcode.cn/problems/integers-with-multiple-sum-of-two-cubes/description/>

题目给出一个整数n，其大小不超过10^9。

对于一个整数x，若存在至少两组不同的正整数对(a, b)，满足a \<\= b，且x \= a^3 + b^3，那么就称x为好整数。

要求找出所有小于等于n的好整数，并按照升序排序返回。

由于n不超过10^9，而好整数是立方和的形式，那么就意味着a和b都不可能超过1000，因此在这里可以直接暴力枚举所有可能的(a, b)，然后利用哈希表记录所有立方和出现的次数。枚举完成后，遍历哈希表，取出其中次数大于1的数即可。

最后附上python代码：

```python
class Solution(object):
    def findGoodIntegers(self, n):
        """
        :type n: int
        :rtype: List[int]
        """
        
        cnt = {}
        a = 1
        while a ** 3 * 2 <= n:
            b = a + 1
            v = a ** 3 + b ** 3
            while v <= n:
                cnt[v] = cnt.get(v, 0) + 1
                b += 1
                v = a ** 3 + b ** 3
            a += 1
        
        good = []
        for v in cnt:
            if cnt[v] > 1:
                good.append(v)
        
        good.sort()
        res = []
        for v in good:
            if v <= n:
                res.append(v)
        return res
```
