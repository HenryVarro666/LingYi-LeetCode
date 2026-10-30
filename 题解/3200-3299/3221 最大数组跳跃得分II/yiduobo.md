---
title: "3221. 最大数组跳跃得分II & 3222. 求出硬币游戏的赢家"
aliases: ["yiduobo的每日leetcode 3221.最大数组跳跃得分II && 3222.求出硬币游戏的赢家", "3221. 最大数组跳跃得分II", "3222. 求出硬币游戏的赢家"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math", "leetcode/game-theory"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/719423658"
zhihu_id: "719423658"
zhihu_title: "yiduobo的每日leetcode 3221.最大数组跳跃得分II && 3222.求出硬币游戏的赢家"
question_id: ["3221", "3222"]
question: ["最大数组跳跃得分II", "求出硬币游戏的赢家"]
problem_url: ["https://leetcode.cn/problems/maximum-array-hopping-score-ii/", "https://leetcode.cn/problems/find-the-winning-player-in-coin-game/"]
difficulty: "Easy"
created: "2024-09-10T23:45:55+08:00"
updated: "2024-09-10T23:45:55+08:00"
upvotes: 0
comments: 0
---

# 3221. 最大数组跳跃得分II & 3222. 求出硬币游戏的赢家

> **[yiduobo的每日leetcode 3221.最大数组跳跃得分II && 3222.求出硬币游戏的赢家](https://zhuanlan.zhihu.com/p/719423658) · 知乎 · 2024-09-10 · 赞同 0**
> 力扣：[3221. 最大数组跳跃得分II](https://leetcode.cn/problems/maximum-array-hopping-score-ii/)
> 力扣：[3222. 求出硬币游戏的赢家](https://leetcode.cn/problems/find-the-winning-player-in-coin-game/) · Easy · 灵茶山艾府：[O(1) 数学做法（Python/Java/C++/C/Go/JS/Rust）](../3222%20求出硬币游戏的赢家/灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3221.最大数组跳跃得分II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-array-hopping-score-ii/description/)

本题与之前的3205题相同，但是数据规模较大。之前的算法是O(n)的，可以直接套用。

[yiduobo：yiduobo的每日leetcode 3205.最大数组跳跃得分I](https://zhuanlan.zhihu.com/p/707553192)

3222.求出硬币游戏的赢家

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-winning-player-in-coin-game/description/)

题目给出两个正整数x和y，分别表示当前有x枚75元的硬币以及y枚10元的硬币。现在alice和bob轮流从中取出价值和为115元的硬币，直到某一方无法再取。问谁是游戏的赢家。

注意到115元只能由一枚75元以及四枚10元组成，因此在这里并没有策略这一说，只需按部就班来取就行了。最终可以取的轮次就是min(x, y // 4)，若这个轮次为奇数，那么赢家就是alice，否则就是bob。

最后附上python代码：

```python
class Solution(object):
    def losingPlayer(self, x, y):
        """
        :type x: int
        :type y: int
        :rtype: str
        """

        rnd = min(x, y // 4)
        if rnd % 2 == 1:
            return 'Alice'
        else:
            return 'Bob'
```
