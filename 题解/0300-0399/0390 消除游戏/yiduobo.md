---
title: "390. 消除游戏"
aliases: ["yiduobo的每日leetcode 390.消除游戏"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/math", "leetcode/simulation", "题单/位运算", "题单/数学算法", "题单/位运算/九-其他", "题单/数学算法/七-杂项"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/172533019"
zhihu_id: "172533019"
zhihu_title: "yiduobo的每日leetcode 390.消除游戏"
question_id: "390"
question: "消除游戏"
problem_url: "https://leetcode.cn/problems/elimination-game/"
difficulty: "Medium"
rating: 3782
created: "2020-08-08T00:00:06+08:00"
updated: "2020-08-08T00:00:06+08:00"
upvotes: 0
comments: 2
---

# 390. 消除游戏

> **[yiduobo的每日leetcode 390.消除游戏](https://zhuanlan.zhihu.com/p/172533019) · 知乎 · 2020-08-08 · 赞同 0**
> 力扣：[390. 消除游戏](https://leetcode.cn/problems/elimination-game/) · Medium · 灵茶山艾府：[从 O(log n) 到 O(1)（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

390.消除游戏<https://leetcode-cn.com/problems/elimination-game/>

找规律的题目。

我们定义第一次操作为正序操作时，处理1到n的最终结果为f[n]，而第一次操作为逆序操作，处理1到n的最终结果为g[n]，那么题目就是要求f[n]的值

那么对于f[n]，第一步是正序删去其中的奇数项，那么此时还剩下

2，4，6，...，(n / 2) \* 2

这里的除法为整除。如果将剩下的数都除以2，那么就可以得到f[n] \= g[n/2] \* 2

接下来对于g[n]，则需要对n分奇偶进行讨论。

当n为奇数时：

此时将删去1到n中所有的奇数项，剩下所有的偶数项，即

2，4，6，...，n - 1

同样的，如果对剩下的数都除以2，就有g[n] \= f[n / 2] \* 2

当n为偶数时：

此时将删去1到n中所有的偶数项，剩下所有的奇数项，即

1，3，5，...，n - 1

如果此时将剩下的数都加一然后除以2，就有g[n] \= f[n / 2] \* 2 - 1

到了这里，就可以从f[n]开始反复在f[n]与g[n]之间迭代，直到n \= 1为止。

最后附上python代码：

```python
class Solution(object):
    def lastRemaining(self, n):
        """
        :type n: int
        :rtype: int
        """

        return self.calc(n, True)

    def calc(self, now, flag):
        if now == 1:
            return 1

        if flag:
            return 2 * self.calc(now / 2, False)
        else:
            return 2 * self.calc(now / 2, True) - 1 + now % 2
```
