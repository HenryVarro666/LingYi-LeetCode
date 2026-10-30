---
title: "1306. 跳跃游戏III"
aliases: ["yiduobo的每日leetcode 1306.跳跃游戏III"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/recursion", "题单/动态规划", "题单/图论算法", "题单/动态规划/专题-跳跃游戏", "题单/图论算法/一-图的遍历"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/391583283"
zhihu_id: "391583283"
zhihu_title: "yiduobo的每日leetcode 1306.跳跃游戏III"
question_id: "1306"
question: "跳跃游戏 III"
problem_url: "https://leetcode.cn/problems/jump-game-iii/"
difficulty: "Medium"
rating: 1397
created: "2021-07-20T22:18:52+08:00"
updated: "2021-07-20T22:18:52+08:00"
upvotes: 0
comments: 0
---

# 1306. 跳跃游戏III

> **[yiduobo的每日leetcode 1306.跳跃游戏III](https://zhuanlan.zhihu.com/p/391583283) · 知乎 · 2021-07-20 · 赞同 0**
> 力扣：[1306. 跳跃游戏 III](https://leetcode.cn/problems/jump-game-iii/) · Medium · 灵茶山艾府：[有向图 DFS（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1306.跳跃游戏III

[力扣](https://leetcode-cn.com/problems/jump-game-iii/)

直接从start处开始进行bfs，每次都尝试往前跳或者往后跳。若当前不会跳出边界，且目的地没有被访问过，那么就目的地加入到bfs队列中。若bfs过程中跳到了0，那么返回true，否则返回false。

最后附上python代码：

```python
class Solution(object):
    def canReach(self, arr, start):
        """
        :type arr: List[int]
        :type start: int
        :rtype: bool
        """

        n = len(arr)
        used = [False] * n
        used[start] = True
        q = [start]
        l = 0
        r = 1
        while l < r:
            now = q[l]
            if arr[now] == 0:
                return True
            l += 1
            if now - arr[now] >= 0 and not used[now - arr[now]]:
                q.append(now - arr[now])
                used[now - arr[now]] = True
                r += 1
            if now + arr[now] < n and not used[now + arr[now]]:
                q.append(now + arr[now])
                used[now + arr[now]] = True
                r += 1
            
        return False
```
