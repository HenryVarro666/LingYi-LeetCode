---
title: "2169. 得到0的操作数"
aliases: ["yiduobo的每日leetcode 2169.得到0的操作数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math", "题单/数学算法", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/533837931"
zhihu_id: "533837931"
zhihu_title: "yiduobo的每日leetcode 2169.得到0的操作数"
question_id: "2169"
question: "得到 0 的操作数"
problem_url: "https://leetcode.cn/problems/count-operations-to-obtain-zero/"
difficulty: "Easy"
created: "2022-06-26T00:06:48+08:00"
updated: "2022-06-26T00:06:48+08:00"
upvotes: 0
comments: 0
---

# 2169. 得到0的操作数

> **[yiduobo的每日leetcode 2169.得到0的操作数](https://zhuanlan.zhihu.com/p/533837931) · 知乎 · 2022-06-26 · 赞同 0**
> 力扣：[2169. 得到 0 的操作数](https://leetcode.cn/problems/count-operations-to-obtain-zero/) · Easy · 灵茶山艾府：[O(log) 辗转相除（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2169.得到0的操作数

[力扣](https://leetcode.cn/problems/count-operations-to-obtain-zero/)

题目描述的是我国古老的求最大公约数的算法更相减损术，问求出最大公约数所需要的计算次数。

执行多次减法不如执行一次除法来得快，不妨使用高配版的辗转相除法来求解最大公约数。在过程中每一步除法的商就是采用更相减损术需要执行的减法次数，那么将每一步的商累加起来就是最终答案了。

最后附上python代码：

```python
class Solution(object):
    def countOperations(self, num1, num2):
        """
        :type num1: int
        :type num2: int
        :rtype: int
        """

        x, y = num1, num2
        if x < y:
            x, y = y, x
        
        res = 0
        while y:
            res += x / y
            x, y = y, x % y
        
        return res
```
