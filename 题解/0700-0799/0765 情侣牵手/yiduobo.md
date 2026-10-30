---
title: "765. 情侣牵手"
aliases: ["yiduobo的每日leetcode 765.情侣牵手"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/339099312"
zhihu_id: "339099312"
zhihu_title: "yiduobo的每日leetcode 765.情侣牵手"
question_id: "765"
question: "情侣牵手"
problem_url: "https://leetcode.cn/problems/couples-holding-hands/"
created: "2020-12-23T21:56:18+08:00"
updated: "2020-12-23T21:56:18+08:00"
upvotes: 0
comments: 0
---

# 765. 情侣牵手

> **[yiduobo的每日leetcode 765.情侣牵手](https://zhuanlan.zhihu.com/p/339099312) · 知乎 · 2020-12-23 · 赞同 0**
> 力扣：[765. 情侣牵手](https://leetcode.cn/problems/couples-holding-hands/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

765.情侣牵手

[力扣](https://leetcode-cn.com/problems/couples-holding-hands/)

首先，需要注意这里的情侣座并不是相邻，而是固定的(0, 1), (2, 3)...，因此对于某个座位上不成对的两个人而言，实际上只有两种交换方式。

接下来回顾一下之前做过的一道题，给出一个长度为n的数组，其中的数字为0到n - 1，要求经过最少次数的调整将数字i放到数组的第i位上。这个题目与本题有点像，但是更简单一些，因为数字交换的方向是固定的。不过从这个题目的做法上也可以得到一些灵感，即对于形成环的数字进行逐位交换。

回到本题，如果将每个座位看做图中的一个点，那么两种交换方式就可以在图中连出两条边，那么最终就可以得到一个图，其中存在一些环。对于一个长度为k的环，最优的情况就是经过k - 1次交换使得这k对情侣配对成功。

到了这里，就有了一种做法：

1、遍历当前座位，统计每个座位能与其他哪两个座位进行交换。

2、根据交换关系构图，若某个座位上的情侣已经配对，那么可以跳过，也可以给出自环，不影响最终的结果。

3、遍历图中的节点，若当前节点没有被访问过，那么就从当前节点开始往后走直到走回当前节点，期间每经过一个其他节点便将答案加一，相当于将当前座位上的人与上一个座位上的人进行了一次交换。

最后附上python代码：

```python
class Solution(object):
    def minSwapsCouples(self, row):
        """
        :type row: List[int]
        :rtype: int
        """

        n = len(row) / 2
        pos_dict = {}
        for index in range(n):
            p1 = row[index * 2] / 2
            p2 = row[index * 2 + 1] / 2
            if p1 not in pos_dict:
                pos_dict[p1] = []
            pos_dict[p1].append(index)
            if p2 not in pos_dict:
                pos_dict[p2] = []
            pos_dict[p2].append(index)

        g = {}
        for x, y in pos_dict.values():
            if x not in g:
                g[x] = set()
            if y not in g:
                g[y] = set()
            g[x].add(y)
            g[y].add(x)

        used = [False] * n
        res = 0
        for index in range(n):
            if not used[index]:
                now = index
                move_flag = True
                while move_flag:
                    used[now] = True
                    move_flag = False
                    for next in g[now]:
                        if not used[next]:
                            res += 1
                            now = next
                            move_flag = True
                            break
        
        return res
```
