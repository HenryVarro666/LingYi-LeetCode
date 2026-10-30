---
title: "LCP 70. 沙地治理"
aliases: ["yiduobo的每日leetcode LCP70.沙地治理"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/580567934"
zhihu_id: "580567934"
zhihu_title: "yiduobo的每日leetcode LCP70.沙地治理"
question_id: "LCP 70"
question: "沙地治理"
created: "2022-11-05T03:13:56+08:00"
updated: "2022-11-05T03:13:56+08:00"
upvotes: 0
comments: 0
---

# LCP 70. 沙地治理

> **[yiduobo的每日leetcode LCP70.沙地治理](https://zhuanlan.zhihu.com/p/580567934) · 知乎 · 2022-11-05 · 赞同 0**
> 力扣：LCP 70. 沙地治理

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP70.沙地治理

[力扣](https://leetcode.cn/problems/XxZZjK/)

找规律的题目。我在这里采用的是贪心法，但是没有想出办法证明我的构造方法一定是最优的。

首先，三角形的三个角都必须要种树，因为这三个位置只与另外一个三角形相邻。

接下来，从贪心的角度除法，如果某个三角形已经与另一个绿洲三角形相邻，那么不到万不得已就不应该在这个三角形中种树，因为这样一来就浪费掉了这两个三角形相邻的那条边。方便起见，从底边开始向上考虑。

首先，底边应该每隔一个空位种树，也就是在底边的所有正三角形种树。接下来，底边的所有倒三角形都会在相邻的两个正三角形的影响下变为绿洲。

接下来对于倒数第二行，所有正三角形的底边与最后一行倒三角形的顶边相邻，因此原则上不应该在这些位置上种树。对于倒数第二行的倒三角，第一个倒三角上应该种树。第一个倒三角种上树之后，第一个正三角以及第二个正三角都会变为绿洲，因此第二个倒三角不应该种树，而是应该在第三个倒三角种树，通过第三个倒三角将第三个正三角变为绿洲，然后通过第二个和第三个正三角将第二个倒三角变为绿洲。

更一般的，在这里可以使用一个标记near_flag表示对于当前处理的倒三角是否已经被相邻的正三角影响到一条边。若near_flag为true，那么就应该标记下一个倒三角，否则就标记当前倒三角，并将near_flag置为true。

除此之外，有一种特殊情况就是来到当前行的末尾时，如果触发了near_flag，那么就应该标记当前倒三角正上方的正三角从而避免浪费，因此在具体处理是，应该是从倒数第二行开始，沿之字型从下往上进行填充。

最后附上python代码：

```python
class Solution(object):
    def sandyLandManagement(self, size):
        """
        :type size: int
        :rtype: List[List[int]]
        """

        res = [[1, 1]]
        if size == 1:
            return res
        
        for index in range(1, size * 2, 2):
            res.append([size, index])
        
        nowx = size - 1
        nowy = 1
        d = 1
        bound = (size - 1) * 2
        near_flag = False
        while nowx != 1:
            #nowy为奇数表示当前位于正三角
            if nowy % 2 == 1:
                nowy += d
                #若nowy是当前行处理的最后一个正三角，那么就往上移动一行，同时之前的near_flag会因此而失效
                if nowy == bound:
                    d = -d
                    nowx -= 1
                    near_flag = False
                    if d > 0:
                        nowy = 2
                        bound = nowx * 2
                    else:
                        nowy = (nowx - 1) * 2
                        bound = 0

            #若当前位置是倒三角，且触发了near_flag
            elif near_flag:
                #特殊情况，即当前倒三角是本行的最后处理的倒三角
                if nowy + d + d == bound:
                    d = -d
                    nowx -= 1
                    if d > 0:
                        nowy = 1
                        bound = nowx * 2
                    else:
                        nowy = nowx * 2 - 1
                        bound = 0
                    
                    #将上一行的第一个处理的正三角种上树
                    if nowx > 1:
                        res.append([nowx, nowy])
                    nowy += d
                else:
                    nowy += d
                    near_flag = False
            
            #没有触发near_flag，那么就种树，并将near_flag置为true
            else:
                res.append([nowx, nowy])
                near_flag = True
                nowy += d
        
        return res
```
