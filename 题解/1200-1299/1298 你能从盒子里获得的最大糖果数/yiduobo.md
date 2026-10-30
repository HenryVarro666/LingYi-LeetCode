---
title: "1298. 你能从盒子里获得的最大糖果数"
aliases: ["yiduobo的每日leetcode 1298.你能从盒子里获得的最大糖果数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/depth-first-search", "leetcode/recursion", "题单/图论算法", "题单/图论算法/一-图的遍历"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/390693631"
zhihu_id: "390693631"
zhihu_title: "yiduobo的每日leetcode 1298.你能从盒子里获得的最大糖果数"
question_id: "1298"
question: "你能从盒子里获得的最大糖果数"
problem_url: "https://leetcode.cn/problems/maximum-candies-you-can-get-from-boxes/"
difficulty: "Hard"
rating: 1825
created: "2021-07-17T23:36:45+08:00"
updated: "2021-07-17T23:36:45+08:00"
upvotes: 0
comments: 0
---

# 1298. 你能从盒子里获得的最大糖果数

> **[yiduobo的每日leetcode 1298.你能从盒子里获得的最大糖果数](https://zhuanlan.zhihu.com/p/390693631) · 知乎 · 2021-07-17 · 赞同 0**
> 力扣：[1298. 你能从盒子里获得的最大糖果数](https://leetcode.cn/problems/maximum-candies-you-can-get-from-boxes/) · Hard · 灵茶山艾府：[DFS 写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1298.你能从盒子里获得的最大糖果数

[力扣](https://leetcode-cn.com/problems/maximum-candies-you-can-get-from-boxes/)

经典的bfs问题。

首先，对于初始拥有的盒子，我们将可以打开的盒子加入到bfs的队列中，并使用哈希表保存剩下暂时无法打开的盒子。

接下来，我们开始进行bfs。对于当前盒子：

1、首先收集盒子中的糖果，将其累加到答案中。

2、接下来考察盒子中的钥匙。对于当前钥匙，若其对应的盒子在哈希表中，说明我们现在可以打开这个盒子，那么将这个盒子加入到bfs的队列中，并将其从哈希表中移除；若其对应的盒子没有在哈希表中，此时则修改status中的对应位置，表示我们现在有这个盒子的钥匙。

3、最后考察盒子中的子盒子。对于当前的子盒子，若其对应的status为1，说明我们在之前某一时刻已经有了这个盒子的钥匙，那么将其加入到bfs队列中；若其对应的status为0，那么我们暂时无法打开这个盒子，于是应当将其加入到哈希表中。

bfs完成后，输出累加的糖果数即可。

最后附上python代码：

```python
class Solution(object):
    def maxCandies(self, status, candies, keys, containedBoxes, initialBoxes):
        """
        :type status: List[int]
        :type candies: List[int]
        :type keys: List[List[int]]
        :type containedBoxes: List[List[int]]
        :type initialBoxes: List[int]
        :rtype: int
        """

        n = len(status)
        q = []
        box_set = set()
        for box in initialBoxes:
            if status[box]:
                q.append(box)
            else:
                box_set.add(box)
        
        l = 0
        r = len(q)
        res = 0
        while l < r:
            now = q[l]
            res += candies[now]
            l += 1
            for key in keys[now]:
                if key in box_set:
                    q.append(key)
                    box_set.remove(key)
                    r += 1
                else:
                    status[key] = 1
            for box in containedBoxes[now]:
                if status[box]:
                    q.append(box)
                    r += 1
                else:
                    box_set.add(box)

        return res
```
