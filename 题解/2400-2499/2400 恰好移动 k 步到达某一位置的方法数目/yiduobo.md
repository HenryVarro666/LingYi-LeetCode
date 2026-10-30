---
title: "2400. 恰好移动k步到达某一位置的方法数目"
aliases: ["yiduobo的每日leetcode 2400.恰好移动k步到达某一位置的方法数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/memoization", "leetcode/hash-table", "题单/动态规划", "题单/数学算法", "题单/动态规划/七-其他线性-DP", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/567271182"
zhihu_id: "567271182"
zhihu_title: "yiduobo的每日leetcode 2400.恰好移动k步到达某一位置的方法数目"
question_id: "2400"
question: "恰好移动 k 步到达某一位置的方法数目"
problem_url: "https://leetcode.cn/problems/number-of-ways-to-reach-a-position-after-exactly-k-steps/"
difficulty: "Medium"
rating: 1751
created: "2022-09-22T23:54:02+08:00"
updated: "2022-09-22T23:54:02+08:00"
upvotes: 0
comments: 0
---

# 2400. 恰好移动k步到达某一位置的方法数目

> **[yiduobo的每日leetcode 2400.恰好移动k步到达某一位置的方法数目](https://zhuanlan.zhihu.com/p/567271182) · 知乎 · 2022-09-22 · 赞同 0**
> 力扣：[2400. 恰好移动 k 步到达某一位置的方法数目](https://leetcode.cn/problems/number-of-ways-to-reach-a-position-after-exactly-k-steps/) · Medium · 灵茶山艾府：[记忆化搜索](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2400.恰好移动k步到达某一位置的方法数目

[力扣](https://leetcode.cn/problems/number-of-ways-to-reach-a-position-after-exactly-k-steps/)

首先，从startPos走到endPos至少需要endPos - startPos步，那么当k小于这个值时，步数是不够的，此时可以直接返回-1。另一方面，当步数充足时，可能出现有多出的步数的情况，此时就需要往回走消耗掉其中的一些。因为需要一来一回走两趟，那么当多出的步数是奇数时就无法刚好消耗掉所有的步数，也是直接返回-1，否则取多余步数的一半，记为back_step，也就是需要往回走的步数。

那么现在的问题就变成了从k步里面选择back_step步的方案数，因此最终答案就是C(k, back_step)，使用递推法直接进行计算就行了。

最后附上python代码：

```python
class Solution(object):
    def numberOfWays(self, startPos, endPos, k):
        """
        :type startPos: int
        :type endPos: int
        :type k: int
        :rtype: int
        """

        rest_step = k - (endPos - startPos)
        if rest_step < 0 or rest_step % 2 == 1:
            return 0
        
        back_step = rest_step / 2

        mod = 10 ** 9 + 7
        f = [[0] * (back_step + 1) for _ in range(k + 1)]
        for i in range(1, k + 1):
            for j in range(min(back_step + 1, i + 1)):
                if j == 0 or j == i:
                    f[i][j] = 1
                else:
                    f[i][j] = (f[i - 1][j - 1] + f[i - 1][j]) % mod
        
        return f[k][back_step]
```
