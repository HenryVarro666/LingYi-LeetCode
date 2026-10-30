---
title: "2147. 分隔长廊的方案数"
aliases: ["yiduobo的每日leetcode 2147.分隔长廊的方案数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/math", "leetcode/combinatorics", "题单/滑动窗口与双指针", "题单/数学算法", "题单/滑动窗口与双指针/六-分组循环", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/529867832"
zhihu_id: "529867832"
zhihu_title: "yiduobo的每日leetcode 2147.分隔长廊的方案数"
question_id: "2147"
question: "分隔长廊的方案数"
problem_url: "https://leetcode.cn/problems/number-of-ways-to-divide-a-long-corridor/"
difficulty: "Hard"
rating: 1915
created: "2022-06-16T22:10:52+08:00"
updated: "2022-06-16T22:10:52+08:00"
upvotes: 0
comments: 0
---

# 2147. 分隔长廊的方案数

> **[yiduobo的每日leetcode 2147.分隔长廊的方案数](https://zhuanlan.zhihu.com/p/529867832) · 知乎 · 2022-06-16 · 赞同 0**
> 力扣：[2147. 分隔长廊的方案数](https://leetcode.cn/problems/number-of-ways-to-divide-a-long-corridor/) · Hard · 灵茶山艾府：[一次遍历，简洁写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2147.分隔长廊的方案数

[力扣](https://leetcode.cn/problems/number-of-ways-to-divide-a-long-corridor/)

首先考虑特殊情况。当座位总数为奇数时，必然不存在合法的划分方案，因此直接返回0。

接下来考虑座位数为偶数的情况。由于题目要求每段内有两个座位，那么每次划分都必须至少将两个座位划分出去，同时不能涵盖到后续的第三个座位，因此实际上可以变更的就时剩下的区间中，第二个座位到第三个座位间的植物的归属。设这些植物的数量为k，那么就有(0, k), (1, k - 1), ..., (k, 0)这k + 1中划分方案，因此需要将答案乘上k + 1，并将前两个作为划分出去后继续向后考虑。

最后附上python代码：

```python
class Solution(object):
    def numberOfWays(self, corridor):
        """
        :type corridor: str
        :rtype: int
        """

        res = 1
        n = len(corridor)
        p = 0
        now = 0
        mod = 10 ** 9 + 7
        while p < n:
            res = res * (now + 1) % mod
            now = 0
            while p < n:
                if corridor[p] == 'S':
                    now += 1
                p += 1
                
                if now == 2:
                    break
            
            if now != 2:
                return 0
            
            now = 0
            while p < n and corridor[p] == 'P':
                now += 1
                p += 1
        
        return res
```
