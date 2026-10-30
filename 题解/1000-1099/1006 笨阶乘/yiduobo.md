---
title: "1006. 笨阶乘"
aliases: ["yiduobo的每日leetcode 1006.笨阶乘"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/366761422"
zhihu_id: "366761422"
zhihu_title: "yiduobo的每日leetcode 1006.笨阶乘"
question_id: "1006"
question: "笨阶乘"
problem_url: "https://leetcode.cn/problems/clumsy-factorial/"
created: "2021-04-21T21:59:03+08:00"
updated: "2021-04-21T21:59:03+08:00"
upvotes: 0
comments: 0
---

# 1006. 笨阶乘

> **[yiduobo的每日leetcode 1006.笨阶乘](https://zhuanlan.zhihu.com/p/366761422) · 知乎 · 2021-04-21 · 赞同 0**
> 力扣：[1006. 笨阶乘](https://leetcode.cn/problems/clumsy-factorial/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

1006.笨阶乘

[力扣](https://leetcode-cn.com/problems/clumsy-factorial/)

式子里面的符号是按照乘除加减循环的，那么一个自然的想法就是按照乘除加减进行分组来求解。不过注意到减号后面是乘号和除号，因此不能将减号或者乘号作为分隔，不过可以选择加号作为分隔，具体来说就是两个加号之间的部分作为一段，那么整个式子可以分成三个部分：

1、起始的N \* (N - 1) / (N - 2)

2、从N - 3开始的加减乘除段

3、剩下的不足以凑出一组加减乘除段的部分

那么在这里我们就需要先判断特殊情况，因为当N\<3时起始部分都凑不齐：

1、当N \= 1时，答案就是1

2、当N \= 2时，答案为2 \* 1 \= 2

接下来就可以考察N >\= 3的情况：

1、初始化答案为N \* (N - 1) / (N - 2)

2、接下来设now为N - 3开始，从now开始以步长为4向下进行循环，直到now小于4，即凑不出一组加减乘除位置。期间每一组的值都是+now - (now - 1) \* (now - 2) / (now - 3)，不断将这个结果累加到答案中。

3、当now \< 4时，若now为0，说明没有余下的数，否则：

3-1）当now \= 3时，还需要执行res \= res + 3 - 2 \* 1 \= res + 1

3-2）当now \= 2时，还需要执行res \= res + 2 - 1 \= res + 1

3-3）当now \= 1时，还需要执行res \= res + 1 \= res + 1

综合起来就是当now > 0 时，需要额外执行res +\= 1

最后附上python代码：

```python
class Solution(object):
    def clumsy(self, N):
        """
        :type N: int
        :rtype: int
        """

        
        if N == 1:
            return 1
        elif N == 2:
            return 2
        else:
            res = N * (N - 1) / (N - 2)
            now = N - 3
            while now >= 4:
                res += now - (now - 1) * (now - 2) / (now - 3)
                now -= 4
            
            if now > 0:
                res += 1
            
            return res
```
