---
title: "2550. 猴子碰撞的方法数"
aliases: ["yiduobo的每日leetcode 2550.猴子碰撞的方法数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "题单/数学算法", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/638949751"
zhihu_id: "638949751"
zhihu_title: "yiduobo的每日leetcode 2550.猴子碰撞的方法数"
question_id: "2550"
question: "猴子碰撞的方法数"
problem_url: "https://leetcode.cn/problems/count-collisions-of-monkeys-on-a-polygon/"
difficulty: "Medium"
rating: 1663
created: "2023-06-23T23:45:05+08:00"
updated: "2023-06-23T23:45:05+08:00"
upvotes: 0
comments: 0
---

# 2550. 猴子碰撞的方法数

> **[yiduobo的每日leetcode 2550.猴子碰撞的方法数](https://zhuanlan.zhihu.com/p/638949751) · 知乎 · 2023-06-23 · 赞同 0**
> 力扣：[2550. 猴子碰撞的方法数](https://leetcode.cn/problems/count-collisions-of-monkeys-on-a-polygon/) · Medium · 灵茶山艾府：[正难则反（Python/Java/C++/Go） ](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2550.猴子碰撞的方法数

[力扣](https://leetcode.cn/problems/count-collisions-of-monkeys-on-a-polygon/)

直接计算碰撞的方法数是比较困难的，不妨反过来思考不会碰撞的方法数有多少。

可以发现，只有当所有猴子都往顺时针或者都往逆时针行动时才不会发生碰撞，也就是只有两种情况不会发生碰撞。而对于这n只猴子，一共有2^n种行动的方法，因此最终答案就是2^n - 2。

另外，由于本题的n较大，因此需要使用快速幂来计算这个2^n。

最后附上python代码：

```python
class Solution(object):
    def monkeyMove(self, n):
        """
        :type n: int
        :rtype: int
        """

        mod = 10 ** 9 + 7

        def quickPow(p):
            if p == 1:
                return 2
            
            x = quickPow(p / 2)
            x *= x
            x %= mod

            if p % 2 == 1:
                x += x
                if x >= mod:
                    x -= mod
            
            return x
        
        res = quickPow(n) - 2
        if res < 0:
            res += mod
        
        return res
```
