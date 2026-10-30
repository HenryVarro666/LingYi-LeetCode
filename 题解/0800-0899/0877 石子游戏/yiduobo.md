---
title: "877. 石子游戏"
aliases: ["yiduobo的每日leetcode 877.石子游戏"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/brainteaser", "leetcode/game-theory", "题单/动态规划", "题单/数学算法", "题单/贪心算法", "题单/动态规划/十四-博弈-DP", "题单/数学算法/四-博弈论", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/350564957"
zhihu_id: "350564957"
zhihu_title: "yiduobo的每日leetcode 877.石子游戏"
question_id: "877"
question: "石子游戏"
problem_url: "https://leetcode.cn/problems/stone-game/"
difficulty: "Medium"
rating: 1590
created: "2021-02-15T23:21:34+08:00"
updated: "2021-02-15T23:21:34+08:00"
upvotes: 1
comments: 0
---

# 877. 石子游戏

> **[yiduobo的每日leetcode 877.石子游戏](https://zhuanlan.zhihu.com/p/350564957) · 知乎 · 2021-02-15 · 赞同 1**
> 力扣：[877. 石子游戏](https://leetcode.cn/problems/stone-game/) · Medium · 灵茶山艾府：[为什么先手必胜？](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

877.石子游戏

[力扣](https://leetcode-cn.com/problems/stone-game/)

首先，对于只有两堆石头的情况，显然是先手必胜。

接下来，对于四堆石头的情况，有下面几种情况：

1、先手拿了第0堆石头

1-1）后手拿了第1堆石头，那么此时可能形成的组合为：

**先手：0 + 2，后手：1 + 3**

或者

先手：0 + 3，后手：1 + 2

1-2）后手拿了第3堆石头，那么此时可能形成的组合为：

**先手：0 + 2，后手：1 + 3**

或者

先手：0 + 1，后手：2 + 3

2、先手拿了第3堆石头

2-1）后手拿了第0堆石头，那么此时可能形成的组合为：

**先手：1 + 3，后手：0 + 2**

或者

先手：2 + 3，后手：0 + 1

2-2）后手拿了第2堆石头，那么此时可能形成的组合为：

先手：0 + 3，后手：1 + 2

或者

**先手：1 + 3，后手：0 + 2**

综合上面的情况可以发现，当先手第一轮拿第0块石头时，其必然可以拿到0 + 2的组合；而当先手第一轮拿第3块石头时，其必然可以拿到1 + 3的组合。由于总的石头数量为奇数，那么0 + 2和组合以及1 + 3的组合中必然有一个比较大的，因此先手可以选择拿其中较大的那个组合达成胜利。

继续往后推广，注意到上面的4堆石头的情况下，先手是可以保证自己拿到全奇数或者全偶数的石头的，那么当有n堆石头时：

1、若先手拿了第0块石头，那么后手只能拿第1块或者第n - 1块石头，而此时先手则可以顺势拿走第2块或者第n - 2块石头，以此类推。这说明在n块石头的情况下，先手依然可以保证拿到所有偶数的石头

2、与上面类似，先手也可以保证拿到所有奇数的石头

因此无论n等于多少，若将其按奇偶划分成两个部分，先手都可以保证拿到较多的那一个部分，因此先手总是必胜的。

最后附上python代码：

```python
class Solution(object):
    def stoneGame(self, piles):
        """
        :type piles: List[int]
        :rtype: bool
        """

        return True
```
