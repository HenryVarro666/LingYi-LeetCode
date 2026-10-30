---
title: "150. 逆波兰表达式求值"
aliases: ["yiduobo的每日leetcode 150.逆波兰表达式求值"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/stack", "leetcode/simulation", "题单/常用数据结构", "题单/面试经典-150-题", "题单/常用数据结构/三-栈", "题单/面试经典-150-题/栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/143116213"
zhihu_id: "143116213"
zhihu_title: "yiduobo的每日leetcode 150.逆波兰表达式求值"
question_id: "150"
question: "逆波兰表达式求值"
problem_url: "https://leetcode.cn/problems/evaluate-reverse-polish-notation/"
difficulty: "Medium"
created: "2020-05-23T22:25:41+08:00"
updated: "2020-05-23T22:26:01+08:00"
upvotes: 0
comments: 0
---

# 150. 逆波兰表达式求值

> **[yiduobo的每日leetcode 150.逆波兰表达式求值](https://zhuanlan.zhihu.com/p/143116213) · 知乎 · 2020-05-23 · 赞同 0**
> 力扣：[150. 逆波兰表达式求值](https://leetcode.cn/problems/evaluate-reverse-polish-notation/) · Medium · 灵茶山艾府：[理解题意，用栈模拟（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

150.逆波兰表达式求值<https://leetcode-cn.com/problems/evaluate-reverse-polish-notation/>

经典的栈操作题目，具体做法为遇到一个数字则将其入栈，遇到运算符则是将栈顶两个数字弹出，计算出结果之后将结果入栈。如果表达式合法，那么最后栈中会刚好剩下一个元素，即最终的答案。

印象中采用这种写法是因为电脑不太认识我们平常从左至右的算式写法，于是写成这种表达式然后利用栈会比较方便一些。

使用python2的话还有一个需要注意的地方是在执行除法时，碰到负除数的话取整方向不同，因此需要做特殊的判断。

最后附上python代码：

```python
class Solution(object):
    def evalRPN(self, tokens):
        """
        :type tokens: List[str]
        :rtype: int
        """

        stack = []

        for char in tokens:
            if char in ['+', '-', '*', '/']:
                num2 = stack.pop()
                num1 = stack.pop()
                if char == '+':
                    x = num1 + num2
                elif char == '-':
                    x = num1 - num2
                elif char == '*':
                    x = num1 * num2
                else:
                    flag = 1
                    if num1 < 0:
                        flag *= -1
                        num1 = -num1
                    if num2 < 0:
                        flag *= -1
                        num2 = -num2

                    x = num1 / num2 * flag
            else:
                x = int(char)
            
            stack.append(x)

        return stack[0]
```
