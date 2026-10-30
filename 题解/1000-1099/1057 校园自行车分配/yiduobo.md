---
title: "1057. 校园自行车分配"
aliases: ["yiduobo的每日leetcode 1057.校园自行车分配"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/607304170"
zhihu_id: "607304170"
zhihu_title: "yiduobo的每日leetcode 1057.校园自行车分配"
question_id: "1057"
question: "校园自行车分配"
problem_url: "https://leetcode.cn/problems/campus-bikes/"
created: "2023-02-17T23:10:41+08:00"
updated: "2023-02-17T23:10:41+08:00"
upvotes: 0
comments: 0
---

# 1057. 校园自行车分配

> **[yiduobo的每日leetcode 1057.校园自行车分配](https://zhuanlan.zhihu.com/p/607304170) · 知乎 · 2023-02-17 · 赞同 0**
> 力扣：[1057. 校园自行车分配](https://leetcode.cn/problems/campus-bikes/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1057.校园自行车分配

[力扣](https://leetcode.cn/problems/campus-bikes/)

题目自行车分配的规则是按照曼哈顿距离为第一关键字，工人编号为第二关键字，自行车编号为第三关键字来进行的，那么最自然的想法就是两两枚举工人和自行车，计算出曼哈顿距离之后与工人编号以及自行车编号组合起来加入到数组中，然后对数组进行一趟排序。

排序后遍历所有的人车配对，若当前的工人还没有被分配自行车，且当前自行车还没有被分配出去，那么就将当前的自行车分配给当前的工人。判断工人是否被分配过自行车，或者自行车是否已经被分配出去则可以利用集合来进行判断。

最后附上python代码：

```python
class Solution(object):
    def assignBikes(self, workers, bikes):
        """
        :type workers: List[List[int]]
        :type bikes: List[List[int]]
        :rtype: List[int]
        """

        match = []
        n = len(workers)
        m = len(bikes)

        for i in range(n):
            for j in range(m):
                match.append([abs(workers[i][0] - bikes[j][0]) + abs(workers[i][1] - bikes[j][1]), i, j])
        
        match.sort()
        used_worker = set()
        used_bike = set()
        res = [None] * n
        for _, i, j in match:
            if i not in used_worker and j not in used_bike:
                res[i] = j
                used_worker.add(i)
                used_bike.add(j)
        
        return res
```
