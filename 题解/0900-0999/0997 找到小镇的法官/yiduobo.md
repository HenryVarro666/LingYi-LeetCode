---
title: "997. 找到小镇的法官"
aliases: ["yiduobo的每日leetcode 997.找到小镇的法官"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/365498559"
zhihu_id: "365498559"
zhihu_title: "yiduobo的每日leetcode 997.找到小镇的法官"
question_id: "997"
question: "找到小镇的法官"
problem_url: "https://leetcode.cn/problems/find-the-town-judge/"
created: "2021-04-16T22:53:48+08:00"
updated: "2021-04-16T22:53:48+08:00"
upvotes: 0
comments: 0
---

# 997. 找到小镇的法官

> **[yiduobo的每日leetcode 997.找到小镇的法官](https://zhuanlan.zhihu.com/p/365498559) · 知乎 · 2021-04-16 · 赞同 0**
> 力扣：[997. 找到小镇的法官](https://leetcode.cn/problems/find-the-town-judge/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

997.找到小镇的法官

[力扣](https://leetcode-cn.com/problems/find-the-town-judge/)

如果将小镇的每个人视为有向图中的一个点，若a信任b则在图中建立一条a指向b的边，那么对于法官的这几个条件：

1、法官不信任任何人，说明法官这个点没有出边，即出度为0

2、除法官外的每个人都信任法官，说明法官这个点有n - k条入边，即入度为n - k，其中k表示小镇法官的数量

3、只有1个人同时满足条件1和条件2，那么说明小镇法官仅有1人，那么条件2也可以转化成入度为n - 1

于是现在我们就只需要统计图中每个点的入度和出度，然后找出图中入度为n - 1，出度为0的点即可。

最后附上python代码：

```python
class Solution(object):
    def findJudge(self, N, trust):
        """
        :type N: int
        :type trust: List[List[int]]
        :rtype: int
        """

        ind = [0] * N
        oud = [0] * N
        for x, y in trust:
            oud[x - 1] += 1
            ind[y - 1] += 1
        
        for x in range(N):
            if ind[x] == N - 1 and oud[x] == 0:
                return x + 1
        
        return -1
```
