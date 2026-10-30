---
title: "1247. 交换字符使得字符串相同"
aliases: ["yiduobo的每日leetcode 1247.交换字符使得字符串相同"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/385514808"
zhihu_id: "385514808"
zhihu_title: "yiduobo的每日leetcode 1247.交换字符使得字符串相同"
question_id: "1247"
question: "交换字符使得字符串相同"
problem_url: "https://leetcode.cn/problems/minimum-swaps-to-make-strings-equal/"
difficulty: "Medium"
rating: 1597
created: "2021-06-30T22:53:43+08:00"
updated: "2021-06-30T22:53:43+08:00"
upvotes: 0
comments: 0
---

# 1247. 交换字符使得字符串相同

> **[yiduobo的每日leetcode 1247.交换字符使得字符串相同](https://zhuanlan.zhihu.com/p/385514808) · 知乎 · 2021-06-30 · 赞同 0**
> 力扣：[1247. 交换字符使得字符串相同](https://leetcode.cn/problems/minimum-swaps-to-make-strings-equal/) · Medium · 灵茶山艾府：[没想明白？一张图秒懂！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1247.交换字符使得字符串相同

[力扣](https://leetcode-cn.com/problems/minimum-swaps-to-make-strings-equal/)

由于字符串中只有x和y两种字符，那么我们只要将两个字符串的x调整成一样，那么其他的y必然都是一样的。

于是我们首先可以统计两个串中x的数目，分别记为x1和x2。另外，在过程中统计两个字符串中不一样的字符数目，记为diff。

首先可以明确的是，若x1 + x2为奇数，那么无论如何都不可能让两个字符串中的x数目一致，因此直接返回-1即可。

接下来考虑要如何将两个字符串匹配上。

两个字符串当中，x数目之间的差别p \= abs(x1 - x2)，那么此时需要p / 2次操作使得两个字符串中x和y的数目一致。在这个过程中，则可以顺带解决掉p组diff中的差别，那么此时的diff就变成了diff - p。

若这个数目小于0，说明可以在配平x和y数目的过程中就完成整个字符串的匹配，因此答案就是p / 2。

若这个数目大于0，则还需要一些额外操作来完成字符串的匹配。我们可以使用一次操作，将一次位置上的差别变为x和y数目上的差别，例如xy和yx，可以交换其中一组x和y，变为xx和yy，此时就从0个字符差别，2组位置差别变成了2个字符差别，0组位置差别。此时实际上就就变成了p \= 2，diff \= 2，于是又可以使用p / 2 \= 1次操作处理掉字符差别和位置差别。

也就是说，使用2次操作可以解决掉4个diff中的差别，因此若diff是4的倍数，那么最终答案就是diff / 4 \* 2 + p / 2，否则就是diff / 4 \* 2 + 2 + p / 2。

最后附上python代码：

```python
class Solution(object):
    def minimumSwap(self, s1, s2):
        """
        :type s1: str
        :type s2: str
        :rtype: int
        """

        l = len(s1)
        x1 = x2 = 0
        diff = 0
        for index in range(l):
            char1 = s1[index]
            char2 = s2[index]
            if char1 == 'x':
                x1 += 1
            if char2 == 'x':
                x2 += 1
            if char1 != char2:
                diff += 1
        
        if (x1 + x2) % 2 != 0:
            return -1
        
        res = abs(x1 - x2) / 2
        diff -= abs(x1 - x2)
        if diff < 0:
            diff = 0
        res += diff / 4 * 2
        if diff % 4 > 0:
            res += 2
        return res
```
