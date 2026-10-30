---
title: "547. 朋友圈"
aliases: ["yiduobo的每日leetcode 547.朋友圈"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/261247376"
zhihu_id: "261247376"
zhihu_title: "yiduobo的每日leetcode 547.朋友圈"
question_id: "547"
question: "朋友圈"
problem_url: "https://leetcode.cn/problems/friend-circles/"
created: "2020-10-10T22:51:43+08:00"
updated: "2020-10-10T22:51:43+08:00"
upvotes: 0
comments: 0
---

# 547. 朋友圈

> **[yiduobo的每日leetcode 547.朋友圈](https://zhuanlan.zhihu.com/p/261247376) · 知乎 · 2020-10-10 · 赞同 0**
> 力扣：[547. 朋友圈](https://leetcode.cn/problems/friend-circles/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

547.朋友圈<https://leetcode-cn.com/problems/friend-circles/>

类似种子染色法的题目，遍历每个人，若这个人当前不属于任何圈子，那么说明这个人的朋友也不属于任何圈子，否则从这个人的朋友必然可以遍历到这个人。于是可以从这个人开始执行bfs或者dfs，将这个人的朋友加入到当前这个人的圈子。

当所有人的圈子都划分好之后，返回圈子的总数即可。

最后附上python代码：

```python
class Solution(object):
    def findCircleNum(self, M):
        """
        :type M: List[List[int]]
        :rtype: int
        """

        n = len(M)
        now_color = 0
        color = [None] * n
        for index in range(n):
            if color[index] is None:
                q = [index]
                l = 0
                r = 1
                color[index] = now_color
                while l < r:
                    now = q[l]
                    l += 1
                    for friend, relation in enumerate(M[now]):
                        if relation == 1 and color[friend] is None:
                            q.append(friend)
                            color[friend] = now_color
                            r += 1
                now_color += 1
        
        return now_color
```
