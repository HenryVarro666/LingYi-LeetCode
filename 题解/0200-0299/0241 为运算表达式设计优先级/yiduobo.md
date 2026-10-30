---
title: "241. 为运算表达式设计优先级"
aliases: ["yiduobo的每日leetcode 241.为运算表达式设计优先级"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/150840854"
zhihu_id: "150840854"
zhihu_title: "yiduobo的每日leetcode 241.为运算表达式设计优先级"
question_id: "241"
question: "为运算表达式设计优先级"
problem_url: "https://leetcode.cn/problems/different-ways-to-add-parentheses/"
created: "2020-06-26T18:01:45+08:00"
updated: "2020-06-26T18:01:45+08:00"
upvotes: 0
comments: 0
---

# 241. 为运算表达式设计优先级

> **[yiduobo的每日leetcode 241.为运算表达式设计优先级](https://zhuanlan.zhihu.com/p/150840854) · 知乎 · 2020-06-26 · 赞同 0**
> 力扣：[241. 为运算表达式设计优先级](https://leetcode.cn/problems/different-ways-to-add-parentheses/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

241.为运算表达式设计优先级<https://leetcode-cn.com/problems/different-ways-to-add-parentheses/>

动态规划的题目。首先将input分割成n个数字以及n - 1个运算符，设f[i][j]表示第i个数到第j个数这一段表达式所有可能形成的答案，那么题目的答案就是f[0][n - 1]。

对于求解f[i][j]，需要枚举分割点cut_pos，优先计算出f[i][cut_pos]以及f[cut_pos][j]，然后逐个枚举f[i][cut_pos]和f[cut_pos + 1][j]中的数，加以组合得到f[i][j]。

实现方面用记忆化搜索的方式会比较方便一点，我在这里采用的普通的动态规划，因此需要先从短到长枚举表达式的长度，因为在计算较长的表达式时需要用到短的表达式的结果。

枚举表达式长度length之后，需要逐个枚举表达式的起点first，此时表达式的终点可以由长度和起点得出，然后还需要枚举分割点cut_pos，再使用上面的计算方式得出f[first][first + length - 1]。

另外需要注意这里的计算答案不需要去重。

最后附上python代码：

```python
class Solution(object):
    def diffWaysToCompute(self, input):
        """
        :type input: str
        :rtype: List[int]
        """

        nums = []
        operators = []

        now = 0
        for char in input:
            if char not in ['+', '-', '*']:
                now = now * 10 + ord(char) - 48
            else:
                nums.append(now)
                operators.append(char)
                now = 0

        nums.append(now)

        f = [[[] for _ in range(len(nums))] for _ in range(len(nums))]

        for i in range(len(nums)):
            f[i][i].append(nums[i])

        for length in range(2, len(nums) + 1):
            for first in range(len(nums) - length + 1):
                for cut_pos in range(length - 1):
                    operator_pos = first + cut_pos
                    second = operator_pos + 1
                    
                    for num1 in f[first][second - 1]:
                        for num2 in f[second][first + length - 1]:
                            if operators[operator_pos] == '+':
                                res = num1 + num2
                            elif operators[operator_pos] == '-':
                                res = num1 - num2
                            else:
                                res = num1 * num2
                            
                            f[first][first + length - 1].append(res)

        return f[0][len(nums) - 1]
```
