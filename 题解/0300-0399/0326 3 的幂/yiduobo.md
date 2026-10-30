---
title: "326. 3的幂"
aliases: ["yiduobo的每日leetcode 326.3的幂"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math", "leetcode/number-theory", "题单/数学算法", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/161087968"
zhihu_id: "161087968"
zhihu_title: "yiduobo的每日leetcode 326.3的幂"
question_id: "326"
question: "3 的幂"
problem_url: "https://leetcode.cn/problems/power-of-three/"
difficulty: "Easy"
created: "2020-07-16T22:06:13+08:00"
updated: "2020-07-16T22:06:13+08:00"
upvotes: 0
comments: 0
---

# 326. 3的幂

> **[yiduobo的每日leetcode 326.3的幂](https://zhuanlan.zhihu.com/p/161087968) · 知乎 · 2020-07-16 · 赞同 0**
> 力扣：[326. 3 的幂](https://leetcode.cn/problems/power-of-three/) · Easy · 灵茶山艾府：[O(1) 数学做法，一行搞定（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

326\. 3的幂<https://leetcode-cn.com/problems/power-of-three/>

我在这里使用的是取巧的做法，具体为考虑int范围内3的幂次最大为1162261467，那么如果n大于0，且n是1162261467的约数，那么n就是3的幂。

最后附上python代码：

```
class Solution(object):
    def isPowerOfThree(self, n):
        """
        :type n: int
        :rtype: bool
        """

        return (n > 0) and (1162261467 % n == 0)
```
