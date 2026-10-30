---
title: "592. 分数加减运算"
aliases: ["yiduobo的每日leetcode 592.分数加减运算"]
tags: ["leetcode", "yiduobo", "leetcode/medium"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/267934487"
zhihu_id: "267934487"
zhihu_title: "yiduobo的每日leetcode 592.分数加减运算"
question_id: "592"
question: "分数加减运算"
problem_url: "https://leetcode.cn/problems/fraction-addition-and-subtraction/"
difficulty: "Medium"
created: "2020-10-22T23:42:59+08:00"
updated: "2020-10-22T23:42:59+08:00"
upvotes: 0
comments: 0
---

# 592. 分数加减运算

> **[yiduobo的每日leetcode 592.分数加减运算](https://zhuanlan.zhihu.com/p/267934487) · 知乎 · 2020-10-22 · 赞同 0**
> 力扣：[592. 分数加减运算](https://leetcode.cn/problems/fraction-addition-and-subtraction/) · Medium · 灵茶山艾府：[Go 库函数](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

592.分数加减运算<https://leetcode-cn.com/problems/fraction-addition-and-subtraction/>

注意到题目保证所有输入都是整数，且范围在1到10之间，而且最多只有10个分数，因此算法这边可以采用最简单暴力的通分法，即

a/b + c/d \= (a \* d + b \* c) / (b \* d)

这里我们将减号统一视为加号，例如对于a/b - c/d，我们看做a/b + (-c)/d

于是具体实现起来就只需要先按加号或者减号将每个分数分离出来，然后根据除号分离出分子和分母。接下来一趟扫描，利用上面通分的做法计算出最终的分子和分母，然后执行一次最大公约数进行约分即可。

最后附上python代码：

```python
class Solution(object):
    def fractionAddition(self, expression):
        """
        :type expression: str
        :rtype: str
        """

        flag = 1
        pos = 0
        if expression[0] == '-':
            flag = -1
            pos = 1
        
        frac_list = []
        x = 0
        y = 0
        num_flag = True
        while pos < len(expression):
            if expression[pos] == '+'  or expression[pos] == '-':
                frac_list.append([x * flag, y])
                if expression[pos] == '+':
                    flag = 1
                else:
                    flag = -1
                num_flag = True
                x = y = 0
            elif expression[pos] == '/':
                num_flag = False
            elif num_flag:
                x = x * 10 + int(expression[pos])
            else:
                y = y * 10 + int(expression[pos])

            pos += 1
        frac_list.append([x * flag, y])
        
        nowx, nowy = frac_list[0]
        for index in range(1, len(frac_list)):
            x, y = frac_list[index]
            nowx = nowx * y + nowy * x
            nowy *= y
        
        flag = 1
        if nowx < 0:
            flag = -1
            nowx = -nowx
        tmpx = nowx
        tmpy = nowy
        while tmpx:
            tmp = tmpy % tmpx
            tmpy = tmpx
            tmpx = tmp
        return '%d/%d' % (flag * nowx / tmpy, nowy / tmpy)
```
