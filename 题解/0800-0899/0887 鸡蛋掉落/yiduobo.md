---
title: "887. 鸡蛋掉落"
aliases: ["yiduobo的每日leetcode 887.鸡蛋掉落"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/351757516"
zhihu_id: "351757516"
zhihu_title: "yiduobo的每日leetcode 887.鸡蛋掉落"
question_id: "887"
question: "鸡蛋掉落"
problem_url: "https://leetcode.cn/problems/super-egg-drop/"
difficulty: "Hard"
rating: 2377
created: "2021-02-20T22:03:01+08:00"
updated: "2021-02-20T22:03:01+08:00"
upvotes: 1
comments: 0
---

# 887. 鸡蛋掉落

> **[yiduobo的每日leetcode 887.鸡蛋掉落](https://zhuanlan.zhihu.com/p/351757516) · 知乎 · 2021-02-20 · 赞同 1**
> 力扣：[887. 鸡蛋掉落](https://leetcode.cn/problems/super-egg-drop/) · Hard · 灵茶山艾府：[教你一步步思考 DP：从记忆化搜索到递推到空间优化！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

887.鸡蛋掉落

[力扣](https://leetcode-cn.com/problems/super-egg-drop/)

经典的鹰蛋问题，O(KN^2)的动态规划算法是比较容易想到的。令f[i][j]表示i颗蛋j层楼，至少需要多少次尝试才能确定F。

那么对于f[i][j]，我们可以从1到j - 1枚举当前在哪一楼进行尝试，设当前枚举到k：

1、若蛋碎了，那么说明我们需要用i - 1颗蛋，在第1到第k - 1层这一共k - 1层中找出答案，于是此时需要的尝试次数为f[i - 1][k - 1] + 1

2、若蛋没碎，那么说明我们需要用i颗蛋，在第k + 1层到第j层这一共j - k层中找出答案，于是此时需要的尝试次数为f[i][j - k] + 1

当然，我们确定蛋是不是碎了，因此只能考虑最差的情况，即每次都取f[i - 1][k - 1] + 1以及f[i][j - k] + 1中较大的那个。

于是，对于f[i][j]就有f[i][j] \= min(max(f[i - 1][k - 1], f[i][j - k]) + 1)

这样一来，就得到了一种O(KN^2)的做法。

接下来则是想办法进行优化。

首先，注意到这里的状态只与上一轮的状态有关，因此可以使用01滚动数组来优化空间。

接下来，对于f[i][j]以及f[i][j +1]，显然有f[i][j + 1] >\= f[i][j]，即随着楼层的增高需要的尝试次数也在增多，这一点不需要证明。另外，直观感觉上进行尝试的楼层也应当随之增加，这里则需要给出证明。

对于f[i][j]而言，考察其组成部分f[i - 1][k - 1]以及f[i][j - k]。根据上面f[i][j + 1] >\= f[i][j]这条结论，f[i - 1][k - 1]随着k的增大是单调递增的，而f[i][j - k]则是单调递减的，因此我们在枚举的过程中，会经历一个max(f[i - 1][k - 1], f[i][j - k])逐渐变小然后再逐渐增大的过程，那么我们可以在第一次增大的时停止枚举，选择当前的k作为决策点。

对于f[i][j + 1]而言，其f[i - 1][k - 1]与f[i][j]完全一致，由于f[i][j +1 - k]>\=f[i][j - k]，因此相比与f[i][j]的f[i][j - k]来说，f[i][j + 1 - k]是整体向上移动了一些的，那么其与f[i - 1][k - 1]的交点也会随之向右侧移动一段距离。

根据这个结论，就说明了f[i][j +1]的决策点k'必然大于等于f[i][j]的决策点k，因此在每次枚举时，可以从上一个状态的决策点出发而不用从1开始，然后在f值第一次增大时停下。于是这里枚举的时间复杂度就从O(N)降到了均摊O(1)，总的时间复杂度就降到了O(KN)。

最后附上python代码：

```python
class Solution(object):
    def superEggDrop(self, K, N):
        """
        :type K: int
        :type N: int
        :rtype: int
        """

        f = [range(N + 1), [0] * (N + 1)]
        flag = 0

        for i in range(1, K):
            flag ^= 1
            now = 1
            for j in range(1, N + 1):
                while now < j and max(f[flag ^ 1][now - 1], f[flag][j - now]) >= max(f[flag ^ 1][now], f[flag][j - now - 1]):
                    now += 1
                f[flag][j] = max(f[flag ^ 1][now - 1], f[flag][j - now]) + 1
        
        return f[flag][-1]
```
