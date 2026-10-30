---
title: "1496. 判断路径是否相交"
aliases: ["yiduobo的每日leetcode 1496.判断路径是否相交"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/416794858"
zhihu_id: "416794858"
zhihu_title: "yiduobo的每日leetcode 1496.判断路径是否相交"
question_id: "1496"
question: "判断路径是否相交"
problem_url: "https://leetcode.cn/problems/path-crossing/"
created: "2021-10-05T22:09:15+08:00"
updated: "2021-10-05T22:09:15+08:00"
upvotes: 1
comments: 0
---

# 1496. 判断路径是否相交

> **[yiduobo的每日leetcode 1496.判断路径是否相交](https://zhuanlan.zhihu.com/p/416794858) · 知乎 · 2021-10-05 · 赞同 1**
> 力扣：[1496. 判断路径是否相交](https://leetcode.cn/problems/path-crossing/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1496.判断路径是否相交

[力扣](https://leetcode-cn.com/problems/path-crossing/)

由于这里操作数最多是有一万，那么可以直接模拟整个行走过程，然后使用哈希表来判断是否产生相交。

最后附上python代码：

```python
class Solution(object):
    def isPathCrossing(self, path):
        """
        :type path: str
        :rtype: bool
        """

        dx = {'N': 0, 'S': 0, 'E': 1, 'W': -1}
        dy = {'N': 1, 'S': -1, 'E': 0, 'W': 0}

        nowx, nowy = 0, 0
        used = set([0])
        for char in path:
            nowx += dx[char]
            nowy += dy[char]
            if nowx * 1001 + nowy in used:
                return True

            used.add(nowx * 1001 + nowy)
        
        return False
```
