---
title: "1992. 找到所有的农场组"
aliases: ["yiduobo的每日leetcode 1992.找到所有的农场组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/499690714"
zhihu_id: "499690714"
zhihu_title: "yiduobo的每日leetcode 1992.找到所有的农场组"
question_id: "1992"
question: "找到所有的农场组"
problem_url: "https://leetcode.cn/problems/find-all-groups-of-farmland/"
difficulty: "Medium"
rating: 1539
created: "2022-04-16T16:57:11+08:00"
updated: "2022-04-16T16:57:12+08:00"
upvotes: 1
comments: 0
---

# 1992. 找到所有的农场组

> **[yiduobo的每日leetcode 1992.找到所有的农场组](https://zhuanlan.zhihu.com/p/499690714) · 知乎 · 2022-04-16 · 赞同 1**
> 力扣：[1992. 找到所有的农场组](https://leetcode.cn/problems/find-all-groups-of-farmland/) · Medium · 灵茶山艾府：[Go 模拟](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

1992.找到所有的农场组

[力扣](https://leetcode-cn.com/problems/find-all-groups-of-farmland/)

题目保证了农场组是标准的矩形，且互不相交，那么可以使用经典的floodfill来找出地图中所有的农场组。另一方面，在找农场组的过程中，对每一块农场组的bfs都是从农场组的左上角开始，而bfs必然于农场组的右下角结束，这也就意味着队列首尾的位置恰好就是题目要找的答案。

最后附上python代码：

```python
class Solution(object):
    def findFarmland(self, land):
        """
        :type land: List[List[int]]
        :rtype: List[List[int]]
        """

        m = len(land)
        n = len(land[0])

        res = []
        used = set()
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]
        for i in range(m):
            for j in range(n):
                if land[i][j] == 1 and i * n + j not in used:
                    q = [[i, j]]
                    used.add(i * n + j)
                    l = 0
                    r = 1
                    while l < r:
                        for nowx, nowy in q[l : r]:
                            for index in range(4):
                                x = nowx + dx[index]
                                y = nowy + dy[index]
                                if x >= 0 and x < m and y >= 0 and y < n and x * n + y not in used and land[x][y] == 1:
                                    used.add(x * n + y)
                                    q.append([x, y])
                    
                        l, r = r, len(q)
                    
                    res.append([q[0][0], q[0][1], q[-1][0], q[-1][1]])
        
        return res
```
