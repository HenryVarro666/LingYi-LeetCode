---
title: "1025. 除数博弈"
aliases: ["yiduobo的每日leetcode 1025.除数博弈"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/369192289"
zhihu_id: "369192289"
zhihu_title: "yiduobo的每日leetcode 1025.除数博弈"
question_id: "1025"
question: "除数博弈"
problem_url: "https://leetcode.cn/problems/divisor-game/"
created: "2021-04-30T23:48:36+08:00"
updated: "2021-04-30T23:48:36+08:00"
upvotes: 1
comments: 0
---

# 1025. 除数博弈

> **[yiduobo的每日leetcode 1025.除数博弈](https://zhuanlan.zhihu.com/p/369192289) · 知乎 · 2021-04-30 · 赞同 1**
> 力扣：[1025. 除数博弈](https://leetcode.cn/problems/divisor-game/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1025.除数博弈

[力扣](https://leetcode-cn.com/problems/divisor-game/)

动态规划的做法是很容易想到的。令f[i]表示对于数字i先手是必胜还是必败，那么我们可以枚举i的所有约数j，然后若其中某个f[i - j]为必败，那么f[i]就是必胜。若所有f[i - j]都是必胜，那么f[i]就是必败。

在利用这个做法打出n\<\=10的情况后，可以发现实际上所有偶数的情况都是必胜的，而所有奇数的情况都是必败的，这应该不是巧合。那么可以试着证明当N为偶数时必胜，否则必败。

1、首先边界条件，n \= 1时和n \= 2时都符合假设

2、接下来考察n > 2的情况。设此时当n满足n \< k时，都满足假设，那么对于n \= k而言：

若此时n为奇数，那么n的所有约数必然都是奇数，那么不论如何操作，之后的局面都是后手面对偶数的情况，因此此时有先手必败

若此时n为偶数，由于必然有n \= n \* 1，那么此时只需要将选择约数1，将n变为n - 1即可。此时后手面对的n - 1为奇数，因此先手必胜

由此可知，当N为偶数时先手必胜，否则先手必败。

最后附上python代码：

```python
class Solution(object):
    def divisorGame(self, n):
        """
        :type n: int
        :rtype: bool
        """

        return n % 2 == 0
```
