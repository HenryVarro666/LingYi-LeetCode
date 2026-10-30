---
title: "LCP 46. 志愿者调配"
aliases: ["yiduobo的每日leetcode LCP46.志愿者调配"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/576473449"
zhihu_id: "576473449"
zhihu_title: "yiduobo的每日leetcode LCP46.志愿者调配"
question_id: "LCP 46"
question: "志愿者调配"
problem_url: "https://leetcode.cn/problems/05/"
created: "2022-10-23T19:48:34+08:00"
updated: "2022-10-23T19:48:34+08:00"
upvotes: 0
comments: 0
---

# LCP 46. 志愿者调配

> **[yiduobo的每日leetcode LCP46.志愿者调配](https://zhuanlan.zhihu.com/p/576473449) · 知乎 · 2022-10-23 · 赞同 0**
> 力扣：[LCP 46. 志愿者调配](https://leetcode.cn/problems/05/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP46.志愿者调配

[力扣](https://leetcode.cn/problems/05ZEDJ/)

题目给出n个未知数，这些数的和为totalNum。接下来，在经过m轮线性变换之后，知道了后n - 1个数在变换后的结果，问这n个未知数是什么。

乍一看是n个未知数n个方程的问题，但是这里的n规模非常大，需要另想办法。

注意到题目已经给出了最后一轮后n - 1的数的值，那么不妨只设一个未知数v表示第0个数最后一轮的值，然后从后往前倒推。

由于是线性变换，那么往回推到最上面那一轮时将会得到n个关于v的线性表达式。接下来只需将这n个式子系数和常数累加起来，就能通过totalNum求出v，从而推导出这n个数一开始的值是什么了。

最后附上python代码：

```python
class Solution(object):
    def volunteerDeployment(self, finalCnt, totalNum, edges, plans):
        """
        :type finalCnt: List[int]
        :type totalNum: int
        :type edges: List[List[int]]
        :type plans: List[List[int]]
        :rtype: List[int]
        """

        num_list = [[1, 0]]
        for num in finalCnt:
            num_list.append([0, num])
        
        g = {}
        for x, y in edges:
            if x not in g:
                g[x] = set()
            if y not in g:
                g[y] = set()
            g[x].add(y)
            g[y].add(x)

        for op, x in plans[::-1]:
            if op == 1:
                num_list[x][0] *= 2
                num_list[x][1] *= 2
            elif op == 2:
                for y in g.get(x, set()):
                    num_list[y][0] -= num_list[x][0]
                    num_list[y][1] -= num_list[x][1]
            else:
                for y in g.get(x, set()):
                    num_list[y][0] += num_list[x][0]
                    num_list[y][1] += num_list[x][1]

        tot_a = tot_b = 0
        for index in range(len(num_list)):
            tot_a += num_list[index][0]
            tot_b += num_list[index][1]
        
        v = (totalNum - tot_b) / tot_a
        res = [num_list[index][0] * v + num_list[index][1] for index in range(len(num_list))]
        return res
```
