---
title: "1267. 统计参与通信的服务器"
aliases: ["yiduobo的每日leetcode 1267.统计参与通信的服务器"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/387050213"
zhihu_id: "387050213"
zhihu_title: "yiduobo的每日leetcode 1267.统计参与通信的服务器"
question_id: "1267"
question: "统计参与通信的服务器"
problem_url: "https://leetcode.cn/problems/count-servers-that-communicate/"
created: "2021-07-06T11:20:03+08:00"
updated: "2021-07-06T11:20:03+08:00"
upvotes: 0
comments: 0
---

# 1267. 统计参与通信的服务器

> **[yiduobo的每日leetcode 1267.统计参与通信的服务器](https://zhuanlan.zhihu.com/p/387050213) · 知乎 · 2021-07-06 · 赞同 0**
> 力扣：[1267. 统计参与通信的服务器](https://leetcode.cn/problems/count-servers-that-communicate/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1267.统计参与通信的服务器

[力扣](https://leetcode-cn.com/problems/count-servers-that-communicate/)

题目要求检测有多少服务器可以与其他服务器通信，那么我们可以逆向思考，找出有多少服务器不能与其他服务器通信。

对于某台服务器，若其不能与其他服务器通信，那么这台服务器的行和列上必然只有这一台服务器，因此可以先一趟遍历，使用哈希表统计每一行和每一列上有多少台服务器，然后再进行一趟遍历，对于当前服务器，若其所在行和列上都只有一台服务器，那么说明这台服务器无法与其他服务器通信。

最后附上python代码：

```python
class Solution(object):
    def countServers(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        m = len(grid)
        n = len(grid[0])
        row = [0] * m
        col = [0] * n
        res = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j]:
                    row[i] += 1
                    col[j] += 1
                    res += 1

        for i in range(m):
            for j in range(n):
                if grid[i][j] and row[i] == 1 and col[j] == 1:
                    res -= 1
        
        return res
```
