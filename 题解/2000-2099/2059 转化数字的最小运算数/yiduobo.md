---
title: "2059. 转化数字的最小运算数"
aliases: ["yiduobo的每日leetcode 2059.转化数字的最小运算数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/breadth-first-search", "leetcode/graph", "leetcode/bfs", "题单/图论算法", "题单/图论算法/一-图的遍历"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/514134702"
zhihu_id: "514134702"
zhihu_title: "yiduobo的每日leetcode 2059.转化数字的最小运算数"
question_id: "2059"
question: "转化数字的最小运算数"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-convert-number/"
difficulty: "Medium"
rating: 1850
created: "2022-05-13T23:44:02+08:00"
updated: "2022-05-13T23:44:02+08:00"
upvotes: 0
comments: 0
---

# 2059. 转化数字的最小运算数

> **[yiduobo的每日leetcode 2059.转化数字的最小运算数](https://zhuanlan.zhihu.com/p/514134702) · 知乎 · 2022-05-13 · 赞同 0**
> 力扣：[2059. 转化数字的最小运算数](https://leetcode.cn/problems/minimum-operations-to-convert-number/) · Medium · 灵茶山艾府：[BFS 简洁写法](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2059.转化数字的最小运算数

[力扣](https://leetcode.cn/problems/minimum-operations-to-convert-number/)

由于题目保证了运算的中间结果只会在0到1000之间，因此可以直接从start开始进行bfs，只将在0到1000之内的且没有被使用过的数添加到bfs的队列中。

枚举当前这一轮bfs中的所有数，对于当前处理的数now，枚举nums中的所有数并与now进行加、减、异或操作，得到结果next。若next恰好等于goal，那么当前bfs的轮次就是答案。若next在0到1000之间，且之前没有被使用过，那么就将其加入到bfs队列中。

最后附上python代码：

```python
class Solution(object):
    def minimumOperations(self, nums, start, goal):
        """
        :type nums: List[int]
        :type start: int
        :type goal: int
        :rtype: int
        """

        l = 0
        r = 1
        q = [start]
        used = set([start])

        step = 0
        while l < r:
            step += 1
            for now in q[l : r]:
                for num in nums:
                    for opt in range(3):
                        if opt == 0:
                            next = now + num
                        elif opt == 1:
                            next = now - num
                        else:
                            next = now ^ num
    
                        if next == goal:
                            return step
                        elif next >= 0 and next <= 1000 and next not in used:
                            used.add(next)
                            q.append(next)
            
            l, r = r, len(q)

        return -1
```
