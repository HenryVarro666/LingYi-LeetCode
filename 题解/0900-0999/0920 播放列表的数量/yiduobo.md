---
title: "920. 播放列表的数量"
aliases: ["yiduobo的每日leetcode 920.播放列表的数量"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/355875025"
zhihu_id: "355875025"
zhihu_title: "yiduobo的每日leetcode 920.播放列表的数量"
question_id: "920"
question: "播放列表的数量"
problem_url: "https://leetcode.cn/problems/number-of-music-playlists/"
created: "2021-03-09T22:43:26+08:00"
updated: "2021-03-09T22:43:26+08:00"
upvotes: 0
comments: 0
---

# 920. 播放列表的数量

> **[yiduobo的每日leetcode 920.播放列表的数量](https://zhuanlan.zhihu.com/p/355875025) · 知乎 · 2021-03-09 · 赞同 0**
> 力扣：[920. 播放列表的数量](https://leetcode.cn/problems/number-of-music-playlists/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

920.播放列表的数量

[力扣](https://leetcode-cn.com/problems/number-of-music-playlists/)

看上去应该可以使用组合数学相关的知识来解决，但是暂时也只想到了最初的一步。

由于要求每首歌至少播放一次，那么实际上就是要求在1到n的某个排列中插入一些数字，同时要求满足插入的间隔。由于这里每首歌都是等价的，因此实际上可以只考虑对于顺序排列的1到n，有多少种满足插入间隔的插入方法。求解之后将这个方法数乘以n阶乘就是最终答案。

到了这一步就没有什么思路了，感觉跟二项式定理以及母函数之类的有一定的关联，但是似乎也不太好套用上去。

退而求其次，选择老老实实用动态规划来做。

设f[i][j]表示由i个不同的数字构成长度为j的序列有多少种，那么对于f[i][j]：

1、假设序列中的第j数字是这一次才加入到序列中，那么可以得知之前已经使用了i - 1个数字，因此第i个数字可以从剩下的n - i + 1个数字中任意选择，于是有

f[i][j] +\= f[i - 1][j - 1] \* (n - i + 1)

2、假设序列中的第j个数字之前已经被使用过了，由于最近使用的k个数字不能再使用，因此只能在剩下的j - k个数字中选择，于是有

f[i][j] +\= f[i][j - 1] \* (j - k)

此时要求j必须大于等于k

初始化f[0][0] \= 1，而最后的f[n][l]就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def numMusicPlaylists(self, N, L, K):
        """
        :type N: int
        :type L: int
        :type K: int
        :rtype: int
        """

        f = [[0] * (L + 1) for _ in range(N + 1)]
        mod = 10 ** 9 + 7

        f[0][0] = 1
        for i in range(1, N + 1):
            for j in range(1, L + 1):
                f[i][j] = f[i - 1][j - 1] * (N - i + 1)
                if i >= K:
                    f[i][j] += f[i][j - 1] * (i - K)
                f[i][j] %= mod

        return f[-1][-1]
```
