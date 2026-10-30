---
title: "2189. 建造纸牌屋的方法数"
aliases: ["yiduobo的每日leetcode 2189.建造纸牌屋的方法数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/627556280"
zhihu_id: "627556280"
zhihu_title: "yiduobo的每日leetcode 2189.建造纸牌屋的方法数"
question_id: "2189"
question: "建造纸牌屋的方法数"
problem_url: "https://leetcode.cn/problems/number-of-ways-to-build-house-of-cards/"
created: "2023-05-07T23:05:28+08:00"
updated: "2023-05-07T23:05:28+08:00"
upvotes: 0
comments: 0
---

# 2189. 建造纸牌屋的方法数

> **[yiduobo的每日leetcode 2189.建造纸牌屋的方法数](https://zhuanlan.zhihu.com/p/627556280) · 知乎 · 2023-05-07 · 赞同 0**
> 力扣：[2189. 建造纸牌屋的方法数](https://leetcode.cn/problems/number-of-ways-to-build-house-of-cards/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2189.建造纸牌屋的方法数

[力扣](https://leetcode.cn/problems/number-of-ways-to-build-house-of-cards/)

题目中的纸牌屋搭建受限与纸牌数量以及底部落脚点的数量，那么很自然想到使用f[i][j]表示i张纸牌且当前层有j个落脚点时所有的合法放置方案数。

注意到在同一行中的纸牌数必然是3k + 2的形式，而这3k + 2张牌需要k + 1个落脚点，同时可以为下一行提供k个落脚点，那么对于f[i][j]:

1、当i % 3 \= 0，且i / 3 + 1 \= j，那么就可以将这i张牌全部放在当前行，此时可以初始化f[i][j] \= 1，否则只能初始化f[i][j] \= 0

2、接下来可以从2开始，以3位步长枚举当前层使用的纸牌数cnt。若当前的cnt / 3 + 1 \<\= j，那么就可以将这cnt张牌放在当前行，同时可以为下一行提供cnt / 3个落脚点，于是就有f[i][j] +\= f[i - cnt][cnt / 3]

最后附上python代码：

```python
class Solution(object):
    def houseOfCards(self, n):
        """
        :type n: int
        :rtype: int
        """

        f = [[None] * ((n - 2) / 3 + 2) for _ in range(n + 1)]

        def calc(now, max_line):
            if f[now][max_line] is None:
                f[now][max_line] = 0
                if (now - 2) % 3 == 0 and (now - 2) / 3 + 1 <= max_line:
                    f[now][max_line] = 1
                
                for cnt in range(2, now, 3):
                    if cnt / 3 + 1 <= max_line:
                        f[now][max_line] += calc(now - cnt, cnt / 3)
            
            return f[now][max_line]

        return calc(n, (n - 2) / 3 + 1)
```
