---
title: "2232. 向表达式添加括号后的最小结果"
aliases: ["yiduobo的每日leetcode 2232.向表达式添加括号后的最小结果"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/string", "leetcode/enumeration", "leetcode/bao-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/543737746"
zhihu_id: "543737746"
zhihu_title: "yiduobo的每日leetcode 2232.向表达式添加括号后的最小结果"
question_id: "2232"
question: "向表达式添加括号后的最小结果"
problem_url: "https://leetcode.cn/problems/minimize-result-by-adding-parentheses-to-expression/"
difficulty: "Medium"
created: "2022-07-20T00:04:50+08:00"
updated: "2022-07-20T00:04:50+08:00"
upvotes: 0
comments: 0
---

# 2232. 向表达式添加括号后的最小结果

> **[yiduobo的每日leetcode 2232.向表达式添加括号后的最小结果](https://zhuanlan.zhihu.com/p/543737746) · 知乎 · 2022-07-20 · 赞同 0**
> 力扣：[2232. 向表达式添加括号后的最小结果](https://leetcode.cn/problems/minimize-result-by-adding-parentheses-to-expression/) · Medium · 灵茶山艾府：[暴力枚举所有插入括号的位置](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2232.向表达式添加括号后的最小结果

[力扣](https://leetcode.cn/problems/minimize-result-by-adding-parentheses-to-expression/)

由于题目中表达式的长度不超过10，那么完全可以直接枚举左右括号的位置。

当确定了括号的位置后，表达式将被分成三个部分，分别是左括号左侧的数l1，左括号右侧的数l2与右括号左侧的数r1的和，以及右括号右侧的数r2。其中第二部分的两个加数l2和r1不能为空，而l1和r2是可以为空的，因此在枚举括号位置的时候需要注意边界。

再然后，就只需要使用l1 \* (l2 + r1) \* r2更新最终答案了。

最后附上python代码：

```python
class Solution(object):
    def minimizeResult(self, expression):
        """
        :type expression: str
        :rtype: str
        """

        left, right = expression.split('+')

        mi = int(left) + int(right)
        res_l = 0
        res_r = len(right)
        for lb in range(0, len(left)):
            if lb == 0:
                l1 = 1
            else:
                l1 = int(left[:lb])
            
            l2 = int(left[lb:])
        
            for rb in range(1, len(right) + 1):
                if rb == len(right):
                    r2 = 1
                else:
                    r2 = int(right[rb:])
                
                r1 = int(right[:rb])

                if l1 * (l2 + r1) * r2 < mi:
                    mi = l1 * (l2 + r1) * r2
                    res_l = lb
                    res_r = rb
        
        return left[:res_l] + '(' + left[res_l:] + '+' + right[:res_r] + ')' + right[res_r:]
```
