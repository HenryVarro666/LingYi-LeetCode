---
title: "3021. Alice和Bob玩鲜花游戏"
aliases: ["yiduobo的每日leetcode 3021.Alice和Bob玩鲜花游戏"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/694793156"
zhihu_id: "694793156"
zhihu_title: "yiduobo的每日leetcode 3021.Alice和Bob玩鲜花游戏"
question_id: "3021"
question: "Alice 和 Bob 玩鲜花游戏"
problem_url: "https://leetcode.cn/problems/alice-and-bob-playing-flower-game/"
difficulty: "Medium"
created: "2024-04-26T23:17:12+08:00"
updated: "2024-04-26T23:17:12+08:00"
upvotes: 1
comments: 0
---

# 3021. Alice和Bob玩鲜花游戏

> **[yiduobo的每日leetcode 3021.Alice和Bob玩鲜花游戏](https://zhuanlan.zhihu.com/p/694793156) · 知乎 · 2024-04-26 · 赞同 1**
> 力扣：[3021. Alice 和 Bob 玩鲜花游戏](https://leetcode.cn/problems/alice-and-bob-playing-flower-game/) · Medium · 灵茶山艾府：[O(1) 数学公式（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3021.Alice和Bob玩鲜花游戏

[. - 力扣（LeetCode）](https://leetcode.cn/problems/alice-and-bob-playing-flower-game/description/)

题目中每次行动虽然可以选择方向，但是要求把所有鲜花都摘完，因此方向在这里无关紧要。如果鲜花的数量为奇数，那么Alice获胜，否则Bob获胜。

为了使得鲜花的总数为奇数，那么就需要当Alice选出奇数朵花，Bob选出偶数朵花，或者Alice选出偶数朵花，Bob选出奇数朵花。两人选出偶数朵花的方案数分别是n整除2以及m整除2，而奇数朵花的方案则可以用n和m分别减去偶数朵花的方案，最后使用乘法原理，二人的奇偶方案互相相乘然后相加即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def flowerGame(self, n, m):
        """
        :type n: int
        :type m: int
        :rtype: int
        """

        even_n = n // 2
        odd_n = n - even_n

        even_m = m // 2
        odd_m = m - even_m

        return even_n * odd_m + odd_n * even_m
```
