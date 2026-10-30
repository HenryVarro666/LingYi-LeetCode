---
title: "2303. 计算应缴税款总额"
aliases: ["yiduobo的每日leetcode 2303.计算应缴税款总额"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/554993469"
zhihu_id: "554993469"
zhihu_title: "yiduobo的每日leetcode 2303.计算应缴税款总额"
question_id: "2303"
question: "计算应缴税款总额"
problem_url: "https://leetcode.cn/problems/calculate-amount-paid-in-taxes/"
difficulty: "Easy"
created: "2022-08-18T01:09:12+08:00"
updated: "2022-08-18T01:09:12+08:00"
upvotes: 0
comments: 0
---

# 2303. 计算应缴税款总额

> **[yiduobo的每日leetcode 2303.计算应缴税款总额](https://zhuanlan.zhihu.com/p/554993469) · 知乎 · 2022-08-18 · 赞同 0**
> 力扣：[2303. 计算应缴税款总额](https://leetcode.cn/problems/calculate-amount-paid-in-taxes/) · Easy · 灵茶山艾府：[Go 模拟（避免运算中出现浮点数）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2303.计算应缴税款总额

[力扣](https://leetcode.cn/problems/calculate-amount-paid-in-taxes/)

使用一个变量last记录上一个税级上限，然后一趟遍历。若总收入大于当前遍历到的税级上限，那么就根据当前税级上限与last之差来计算税额并累加至答案，否则根据总收入与last之差计算税额，累加至答案后直接返回。

最后附上python代码：

```python
class Solution(object):
    def calculateTax(self, brackets, income):
        """
        :type brackets: List[List[int]]
        :type income: int
        :rtype: float
        """

        last = 0
        res = 0
        for upper, percent in brackets:
            if income > upper:
                res += (upper - last) * percent / 100.0
            else:
                res += (income - last) * percent / 100.0
                break
        
            last = upper

        return res
```
