---
title: "166. 分数到小数"
aliases: ["yiduobo的每日leetcode 166.分数到小数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/math", "题单/数学算法", "题单/数学算法/七-杂项"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/144363637"
zhihu_id: "144363637"
zhihu_title: "yiduobo的每日leetcode 166.分数到小数"
question_id: "166"
question: "分数到小数"
problem_url: "https://leetcode.cn/problems/fraction-to-recurring-decimal/"
difficulty: "Medium"
created: "2020-05-28T23:33:27+08:00"
updated: "2020-05-28T23:33:27+08:00"
upvotes: 0
comments: 0
---

# 166. 分数到小数

> **[yiduobo的每日leetcode 166.分数到小数](https://zhuanlan.zhihu.com/p/144363637) · 知乎 · 2020-05-28 · 赞同 0**
> 力扣：[166. 分数到小数](https://leetcode.cn/problems/fraction-to-recurring-decimal/) · Medium · 灵茶山艾府：[模拟长除法（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

166.分数到小数<https://leetcode-cn.com/problems/fraction-to-recurring-decimal/>

根据竖式除法的计算过程可以很容易得到这一题的解决方法。

由于以7为除数的商是很典型的，那么在这里就以20除以7举例：

1、首先得出整数部分，商为2，余数为6。此时已经计算出来的商为2。

2、小数点后第一位，6乘上10，变成60，然后除以7，商为8，余数为4。此时已经计算出来的商为2.8。

3、小数点后第二位，4乘上10，变成40，然后除以7，商为5，余数为5。此时已经计算出来的商为2.85。

4、小数点后第三位，5乘上10，变成50，然后除以7，商为7，余数为1。此时已经计算出来的商为2.857。

5、小数点后第四位，1乘上10，变成10，然后除以7，商为1，余数为3。此时已经计算出来的商为2.8571。

6、小数点后第五位，3乘上10，变成30，然后除以7，商为4，余数为2。此时已经计算出来的商为2.85714。

7、小数点后第六位，2乘上10，变成20，然后除以7，商为2，余数为6。此时已经计算出来的商为2.857142。

8、可以发现，现在又变成了步骤2中的6乘上10的情况，因此就可以确定商的循环节为步骤2所对应的的小数点后第一位到步骤7所对应的小数点后第六位，即857142，因此就能得到最终的答案为2.(857142)。

于是，这个问题也可以按上面这种方式，每次记录下当前位的被除数与商，然后继续往下做除法。如果除尽了或者出现过了原来出现过的被除数，那么就找到了答案。

python2实现时需要特别注意做负数的取模运算时会取正数的结果，所以这里需要先确定答案的符号，然后将计算过程变成正数除以正数。

最后附上python代码：

```python
class Solution(object):
    def fractionToDecimal(self, numerator, denominator):
        """
        :type numerator: int
        :type denominator: int
        :rtype: str
        """

        flag = 1

        if numerator < 0:
            flag *= -1
            numerator = -numerator

        if denominator < 0:
            flag *= -1
            denominator = -denominator

        int_part = numerator / denominator
        numerator %= denominator

        if numerator == 0:
            return str(flag * int_part)

        rest_dict = {}
        cycle = ''

        rest_dict[numerator] = 0
        while numerator:
            numerator *= 10
            cycle += str(numerator / denominator)
            numerator %= denominator
            if numerator in rest_dict:
                cycle_pos = rest_dict[numerator]
                break
            else:
                rest_dict[numerator] = len(cycle)

        if flag < 0:
            res = '-'
        else:
            res=  ''

        res += str(int_part)

        if not numerator:
            res += '.' + cycle
        else:
            res += '.' + cycle[:cycle_pos] + '(' + cycle[cycle_pos:] + ')'
        return res
```
