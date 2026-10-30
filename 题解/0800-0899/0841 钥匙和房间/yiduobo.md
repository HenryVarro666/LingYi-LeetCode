---
title: "841. 钥匙和房间"
aliases: ["yiduobo的每日leetcode 841.钥匙和房间"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/347097501"
zhihu_id: "347097501"
zhihu_title: "yiduobo的每日leetcode 841.钥匙和房间"
question_id: "841"
question: "钥匙和房间"
problem_url: "https://leetcode.cn/problems/keys-and-rooms/"
created: "2021-01-27T20:53:20+08:00"
updated: "2021-01-27T20:53:20+08:00"
upvotes: 0
comments: 0
---

# 841. 钥匙和房间

> **[yiduobo的每日leetcode 841.钥匙和房间](https://zhuanlan.zhihu.com/p/347097501) · 知乎 · 2021-01-27 · 赞同 0**
> 力扣：[841. 钥匙和房间](https://leetcode.cn/problems/keys-and-rooms/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

841.钥匙和房间

[力扣](https://leetcode-cn.com/problems/keys-and-rooms/)

乍一看感觉是拓扑排序，但是可以发现，这里除0号房间之外的每个房间入度都为1，且初始必然从0号房间开始，因此无需计算每个点的入度，只需要从0开始进行bfs。在bfs过程中若拿到了编号为k的钥匙，那么就将k号房间加入到bfs队列中即可。

bfs完成后，检测最终拿到的钥匙数量或bfs队列的长度是否等于房间总数。

最后附上python代码：

```python
class Solution(object):
    def canVisitAllRooms(self, rooms):
        """
        :type rooms: List[List[int]]
        :rtype: bool
        """

        q = [0]
        l = 0
        r = 1
        used = set([0])
        while l < r:
            now = q[l]
            l += 1
            for key in rooms[now]:
                if key not in used:
                    used.add(key)
                    q.append(key)
                    r += 1
        
        return len(used) == len(rooms)
```
