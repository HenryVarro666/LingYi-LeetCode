---
title: "3238. 求出胜利玩家的数目"
aliases: ["yiduobo的每日leetcode 3238.求出胜利玩家的数目"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/720581177"
zhihu_id: "720581177"
zhihu_title: "yiduobo的每日leetcode 3238.求出胜利玩家的数目"
question_id: "3238"
question: "求出胜利玩家的数目"
problem_url: "https://leetcode.cn/problems/find-the-number-of-winning-players/"
difficulty: "Easy"
created: "2024-09-17T23:36:45+08:00"
updated: "2024-09-17T23:36:45+08:00"
upvotes: 1
comments: 0
---

# 3238. 求出胜利玩家的数目

> **[yiduobo的每日leetcode 3238.求出胜利玩家的数目](https://zhuanlan.zhihu.com/p/720581177) · 知乎 · 2024-09-17 · 赞同 1**
> 力扣：[3238. 求出胜利玩家的数目](https://leetcode.cn/problems/find-the-number-of-winning-players/) · Easy · 灵茶山艾府：[两种方法：两次遍历/一次遍历（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3238.求出胜利玩家的数目

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-number-of-winning-players/description/)

题目给出一个整数n，表示有n个玩家参与游戏。同时给出一个二维数组pick，其中pick\[i\] \= \[x\[i\], y\[i\]\]表示x\[i\]玩家获得了一个颜色为y\[i\]的球。若玩家i获得任意一种同色球的数目严格大于i个，那么i就是胜利玩家。问最终由多少个胜利玩家。

直接按照题目要求模拟即可。先对pick数组进行一趟遍历，使用哈希表统计每个玩家获取的每种颜色的球的数量，接下来再遍历每个玩家的编号，若当前玩家获得的同色球的最大数目大于当前玩家的编号，则更新答案。

最后附上python代码：

```python
class Solution(object):
    def winningPlayerCount(self, n, pick):
        """
        :type n: int
        :type pick: List[List[int]]
        :rtype: int
        """

        balls = [{} for _ in range(n)]
        for x, y in pick:
            balls[x][y] = balls[x].get(y, 0) + 1

        res = 0
        for index in range(n):
            if balls[index] and max(balls[index].values()) > index:
                res += 1

        return res
```
