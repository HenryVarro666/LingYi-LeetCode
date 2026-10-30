---
title: "672. 灯泡开关II"
aliases: ["yiduobo的每日leetcode 672.灯泡开关II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/295116006"
zhihu_id: "295116006"
zhihu_title: "yiduobo的每日leetcode 672.灯泡开关II"
question_id: "672"
question: "灯泡开关II"
problem_url: "https://leetcode.cn/problems/bulb-switcher-ii/"
created: "2020-11-15T16:33:39+08:00"
updated: "2020-11-15T16:33:39+08:00"
upvotes: 0
comments: 0
---

# 672. 灯泡开关II

> **[yiduobo的每日leetcode 672.灯泡开关II](https://zhuanlan.zhihu.com/p/295116006) · 知乎 · 2020-11-15 · 赞同 0**
> 力扣：[672. 灯泡开关II](https://leetcode.cn/problems/bulb-switcher-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

672.灯泡开关II

[力扣](https://leetcode-cn.com/problems/bulb-switcher-ii/)

这里有四种开关操作，那么我们可以弄一个状态列表，每个操作都会让状态产生改变。

首先有一点，执行的顺序是无关紧要的，因此可以任意调整两次操作的先后进行组合。接下来，执行两次相同的操作将无事发生。最后，操作2和操作3各执行一次相当于执行了一次操作1，那么就有

操作1 + 操作2 \= （操作2 + 操作3） + 操作2 \= 操作3

操作1 + 操作3 \= （操作2 + 操作3） + 操作3 \= 操作2

有了上面这几点，我们接下来寻找状态直接的转移关系。简单起见，我们用s表示状态，a表示操作。

对于初始状态灯泡全开，设为s0，那么：

s0 + a1 \= s1

s0 + a2 \= s2

s0 + a3 \= s3

s0 + a4 \= s4

对于s1，有：

s1 + a1 \= (s0 + a1) + a1 \= s0

s1 + a2 \= (s0 + a1) + a2 \= s0 + (a1 + a2) \= s0 + a3 \= s3

s1 + a3 \= (s0 + a1) + a3 \= s0 + (a1 + a3) \= s0 + a2 \= s2

s1 + a4 \= s5

对于s2，有：

s2 + a1 \= (s0 + a2) + a1 \= s0 + (a1 + a2) \= s0 + a3 \= s3

s2 + a2 \= (s0 + a2) + a2 \= s0

s2 + a3 \= (s0 + a2) + a3 \= s0 + (a2 + a3) \= s0 + a1 \= s1

s2 + a4 \= s6

对于s3，有：

s3 + a1 \= (s0 + a3) + a1 \= s0 + (a1 + a3) \= s0 + a2 \= s2

s3 + a2 \= (s0 + a3) + a2 \= s0 + (a2 + a3) \= s0 + a1 \= s1

s3 + a3 \= (s0 + a3) + a3 \= s0

a3 + a4 \= s7

对于s4，有：

s4 + a1 \= (s0 + a4) + a1 \= (s0 + a1) + a4 \= s1 + a4 \= s5

s4 + a2 \= (s0 + a4) + a2 \= (s0 + a2) + a4 \= s2 + a4 \= s6

s4 + a3 \= (s0 + a4) + a3 \= (s0 + a3) + a4 \= s3 + a4 \= s7

s4 + a4 \= (s0 + a4) + a4 \= s0

对于s5，通过s1的第4条以及s4的第1条有s5 \= s1 + a4 \= s4 + a1，那么：

s5 + a1 \= (s4 + a1) + a1 \= s4

s5 + a2 \= (s4 + a1) + a2 \= s4 + (a1 + a2) \= s4 + a3 \= s7

s5 + a3 \= (s4 + a1) + a3 \= s4 + (a1 + a3) \= s4 + a2 \= s6

s5 + a4 \= (s1 + a4) + a4 \= s1

对于s6，通过s2的第4条以及s4的第2条有s6 \= s2 + a4 \= s4 + a2，那么：

s6 + a1 \= (s4 + a2) + a1 \= s4 + (a1 + a2) \= s4 + a3 \= s7

s6 + a2 \= (s4 + a2) + a2 \= s4

s6 + a3 \= (s4 + a2) + a3 \= s4 + (a2 + a3) \= s4 + a1 \= s5

s6 + a4 \= (s2 + a4) + a4 \= s2

对于s7，通过s3的第4条以及s4的第3条右s7 \= s3 + a4 \= s4 + a3，那么：

s7 + a1 \= (s4 + a3) + a1 \= s4 + (a1 + a3) \= s4 + a2 \= s6

s7 + a2 \= (s4 + a3) + a2 \= s4 + (a2 + a3) \= s4 + a1 \= s5

s7 + a3 \= (s4 + a3) + a3 \= s4

s7 + a4 \= (s3 + a4) + a4 \= s3

至此，0到7这一共8个状态已经形成了闭环。

我们从s0开始：

1、第一轮可以得到s1、s2、s3、s4

2、第二轮为：

s1 -> s0、s2、s3、s5

s2 -> s0、s1、s3、s6

s3 -> s0、s1、s2、s7

s4 -> s0、s5、s6、s7

那么第二轮可以得到s0、s1、s2、s3、s5、s6、s7

3、第三轮开始就可以得到s0到s7中的任意状态了

因此在理论上来说，m \= 0时答案应该为1，m \= 1时答案应该为4，m \= 2时答案应该为7，其他情况下答案都是8。

但是需要注意的是，上面时存在4种不同操作时的情况，在灯泡数量不足的时，某些操作实际上是同一种操作。

当灯泡数n \= 1时，实际上有效的只有a1这一种操作，因此答案为2

当灯泡数n \= 2是，a3和a4操作的都是灯泡1，因此实际上只有a1、a2、a3这三种操作，那么

1、第一轮之后，可以得到s1、s2、s3

2、第二轮为：

s1 -> s0、s2、s3

s2 -> s0、s1、s3

s3 -> s0、s1、s2

那么第二轮以及之后的轮次都可以得到s0、s1、s2、s3

因此n \= 2时，若m \= 0时答案应该为1，m \= 1时答案应该为3，其他情况下答案都是4。

综合起来，得到最终的结论为：

1、若n \= 0，答案为1

2、若n > 0且m \= 0，答案为1

3、若n \= 1且m > 0，答案为2

4、若n \= 2且m \= 1，答案为3

5、若n \= 2且m >\= 2，答案为4

6、若n >\=3且m \= 1，答案为4

7、若n >\=3且m \= 2，答案为7

8、其他情况下答案为8

这一题最后的代码虽然很短，但是考察状态间的转移，以及灯泡数量不足时操作重合的判断还是很有意思的。最后附上python代码：

```python
class Solution(object):
    def flipLights(self, n, m):
        """
        :type n: int
        :type m: int
        :rtype: int
        """

        if n == 0:
            return 1

        if m == 0:
            return 1

        if n == 1:
            return 2

        if n == 2:
            if m == 1:
                return 3
            else:
                return 4

        if m == 1:
            return 4
        elif m == 2:
            return 7
        else:
            return 8
```
