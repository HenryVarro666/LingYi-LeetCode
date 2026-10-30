---
title: "972. 相等的有理数"
aliases: ["yiduobo的每日leetcode 972.相等的有理数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/362291077"
zhihu_id: "362291077"
zhihu_title: "yiduobo的每日leetcode 972.相等的有理数"
question_id: "972"
question: "相等的有理数"
problem_url: "https://leetcode.cn/problems/equal-rational-numbers/"
created: "2021-04-04T21:48:25+08:00"
updated: "2021-04-04T21:48:25+08:00"
upvotes: 0
comments: 0
---

# 972. 相等的有理数

> **[yiduobo的每日leetcode 972.相等的有理数](https://zhuanlan.zhihu.com/p/362291077) · 知乎 · 2021-04-04 · 赞同 0**
> 力扣：[972. 相等的有理数](https://leetcode.cn/problems/equal-rational-numbers/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

972.相等的有理数

[力扣](https://leetcode-cn.com/problems/equal-rational-numbers/)

根据题目意思，这里可能包含三种类型的数字，分别为整数、有限小数以及无限循环小数。前两种处理起来相对比较简单，无限循环小数则比较麻烦。

注意到题目的最后一句“即0.1(6)或0.1666(6)或0.166(66)都是1/6的正确表示形式”，已经给出了提示，可以将无限循环小数转换为分数的形式，同时整数和有限小数也可以很方便地转换成分数的形式，

接下来，对于三种类型的数字：

1、对于整数，设其为x，那么其分数形式就是x / 1。

2、对于有限小数，设其整数部分为x，小数部分为y。设y的长度为l，那么我们可以将这个数先乘以10^l，再除以10^l，那么就可以得到(x \* 10^l + y) / 10^l，即要求的分数形式。

3、对于无线循环小数，可以使用证明0.9循环是否等于1的经典民科做法，以样例1来说明。

对于0.(52)，设x \= 0.(52)，那么100x \= 52.(52)，后者减去前者，可得

100x - x \= 52

解得x \= 52 / 99

对于0.5(25)，设x \= 0.5(25)，那么10x \= 5.(25)，1000x \= 525.(25)，后者减去前者，可得

1000x - 10x \= 520

解得x \= 520/990

总结起来就是，先将有限小数的部分按照情况2的做法乘以10^l得到x'，然后对于循环部分，设循环节长度为m，那么就是用x' \* 10^m - x'从而消除掉循环节得到最终的分数形式。

将两个数都转化为分数形式之后，设二者分别为a/b与c/d比较，那么此时只需要检测a \* d是否等于b \* c即可，甚至都不需要约分。

最后附上python代码：

```python
class Solution(object):
    def isRationalEqual(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: bool
        """

        int_s, mutli_s = self.parse(s)
        int_t, multi_t = self.parse(t)

        #print int_s, mutli_s
        #print int_t, multi_t

        return int_s * multi_t == int_t * mutli_s

    def parse(self, num):
        parts = num.split('.')
        if len(parts) == 1:
            return int(parts[0]), 1

        int_part, float_part = parts
        int_part = int(int_part)
        multi = 1

        parts = float_part.replace(')', '').split('(')
        if parts[0] != '':
            multi = 10 ** (len(parts[0]))
            int_part = int_part * multi + int(parts[0])

        if len(parts) == 1:
            return int_part, multi
        
        return int_part * (10 ** (len(parts[1])) - 1) + int(parts[1]), multi * (10 ** (len(parts[1])) - 1)
```
