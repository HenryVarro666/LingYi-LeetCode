---
title: "2647. 把三角形染成红色"
aliases: ["yiduobo的每日leetcode 2647.把三角形染成红色"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/647167652"
zhihu_id: "647167652"
zhihu_title: "yiduobo的每日leetcode 2647.把三角形染成红色"
question_id: "2647"
question: "把三角形染成红色"
problem_url: "https://leetcode.cn/problems/color-the-triangle-red/"
created: "2023-08-01T01:17:17+08:00"
updated: "2023-08-01T01:17:17+08:00"
upvotes: 0
comments: 0
---

# 2647. 把三角形染成红色

> **[yiduobo的每日leetcode 2647.把三角形染成红色](https://zhuanlan.zhihu.com/p/647167652) · 知乎 · 2023-08-01 · 赞同 0**
> 力扣：[2647. 把三角形染成红色](https://leetcode.cn/problems/color-the-triangle-red/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2647.把三角形染成红色

[力扣](https://leetcode.cn/problems/color-the-triangle-red/)

本题与之前遇到过的LCP70题完全相同，直接照搬当时的处理方法即可。

[yiduobo：yiduobo的每日leetcode LCP70.沙地治理](https://zhuanlan.zhihu.com/p/580567934)

最后附上python代码：

```python
class Solution(object):
    def colorRed(self, n):
        """
        :type n: int
        :rtype: List[List[int]]
        """

        res = [[1, 1]]
        if n == 1:
            return res
        
        for index in range(1, n * 2, 2):
            res.append([n, index])
        
        nowx = n - 1
        nowy = 1
        d = 1
        bound = (n - 1) * 2
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
