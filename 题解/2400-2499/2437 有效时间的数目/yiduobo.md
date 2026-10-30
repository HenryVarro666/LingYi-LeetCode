---
title: "2437. 有效时间的数目"
aliases: ["yiduobo的每日leetcode 2437.有效时间的数目"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math", "leetcode/combinatorics", "leetcode/counting"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/583429976"
zhihu_id: "583429976"
zhihu_title: "yiduobo的每日leetcode 2437.有效时间的数目"
question_id: "2437"
question: "有效时间的数目"
problem_url: "https://leetcode.cn/problems/number-of-valid-clock-times/"
difficulty: "Easy"
created: "2022-11-14T22:33:53+08:00"
updated: "2022-11-14T22:33:53+08:00"
upvotes: 1
comments: 0
---

# 2437. 有效时间的数目

> **[yiduobo的每日leetcode 2437.有效时间的数目](https://zhuanlan.zhihu.com/p/583429976) · 知乎 · 2022-11-14 · 赞同 1**
> 力扣：[2437. 有效时间的数目](https://leetcode.cn/problems/number-of-valid-clock-times/) · Easy · 灵茶山艾府：[乘法原理：分别计算小时和分钟（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2437.有效时间的数目

[力扣](https://leetcode.cn/problems/number-of-valid-clock-times/description/)

由于题目中最多只有四个问号，那么直接暴力枚举所有可行性的话完全是可行的。我在这里采取的是分情况讨论的做法。

首先，时间的小时和分钟互相之间不会影响，因此可以分开来讨论。

接下来先讨论小时。小时的问号分布有4种情况：

1、小时的两个位置上都是问号。此时一共24种可行的选项

2、小时的十位上为问号，个位上是数字。此时需要判断个位上数字与是否小于4，若小于，那么十位上就可以取0、1、2，共3种可能，否则只能取0和1，共2种可能

3、小时的十位上是数字，各位上是问号。此时则需要判断十位上的数字是否小于2，若小于，那么个位上就可以任意选取，共10种可能；若等于，那么个位上只能取0、1、2、3，共4种可能；若大于，说明此时小时的数字有问题，可以认为小时的可能取值数为0

4、小时的两个位置上都不是问号。此时需要判断这个两位数是否大于23，若大于，则说明小时的数字有问题，置取值数为0，否则为1

接下来讨论分钟。问号的分布同样是4种情况：

1、分钟的两个位置上都是问号。此时一共60种可行的选项

2、分钟的十位上为问号，个位上是数字。无论此时的个位是什么，十位上的都可以选择0、1、2、3、4、5，共6中可能

3、分钟的十位上为数字，个位上为问号。此时需要先判断十位上的数字是否大于5，若大于，说明分钟有问题，应该置分钟的取值数为0；否则个位上可以任意取值，共10种可能

4、分钟的两个位置上都不是问号。此时同样是需要判断十位上的数字是否大于5，若大于，则置取值数为0，否则为1

最后，将小时和分钟的取值数相乘即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def countTime(self, time):
        """
        :type time: str
        :rtype: int
        """

        if time[0] == '?':
            if time[1] == '?':
                left = 24
            elif time[1] < '4':
                left = 3
            else:
                left = 2
        elif time[1] == '?':
            if time[0] == '2':
                left = 4
            elif time[0] > '2':
                left = 0
            else:
                left = 10
        elif int(time[0]) * 10 + int(time[1]) > 23:
            left = 0
        else:
            left = 1
        
        if time[3] == '?':
            if time[4] == '?':
                right = 60
            else:
                right = 6
        elif time[3] > '5':
            right = 0
        elif time[4] == '?':
            right = 10
        else:
            right = 1
        
        return left * right
```
