---
title: "464. 我能赢吗"
aliases: ["yiduobo的每日leetcode 464.我能赢吗"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/226019524"
zhihu_id: "226019524"
zhihu_title: "yiduobo的每日leetcode 464.我能赢吗"
question_id: "464"
question: "我能赢吗"
problem_url: "https://leetcode.cn/problems/can-i-win/"
created: "2020-09-08T20:20:06+08:00"
updated: "2020-09-08T20:20:06+08:00"
upvotes: 0
comments: 0
---

# 464. 我能赢吗

> **[yiduobo的每日leetcode 464.我能赢吗](https://zhuanlan.zhihu.com/p/226019524) · 知乎 · 2020-09-08 · 赞同 0**
> 力扣：[464. 我能赢吗](https://leetcode.cn/problems/can-i-win/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

464.我能赢吗<https://leetcode-cn.com/problems/can-i-win/>

按题目描述应该可以用博弈论的方法去解，但是我现在已经不会这一套了。注意到题目保证可选的数最多不超过20，那么如果将每个数选或者没选按照01进行编码，那么20个数最多有2^20 \= 1048576种状态，于是可以在这上面进行状态压缩动态规划。

具体来说为f[i]表示状态为i时先手是否能赢，那么对于f[i]，可以先枚举所有的数字num，然后通过i & (1\<\<num)技能知道num是否已经被选择过。然后对于没有选择过的数字，设为x，若当前选了x，那么此时的状态就由i变成了i + (1\<\<x)，那么若f[i + (1\<\<x)]为false，说明此时选择x是一种必胜策略，那么就有f[i] \= True。若找不到满足条件的x，说明此时为必败状态，则有f[i] \= False。f[0]即为最终的答案。

状态总数为2^n，每次转移需要枚举所有的数n，因此最终的时间复杂度为O(2^n \* n)。

另外，需要注意特别判断目标和为0以及选了所有的数都无法达到目标和这两种特殊情况。

最后附上python代码：

```python
class Solution(object):
    def canIWin(self, maxChoosableInteger, desiredTotal):
        """
        :type maxChoosableInteger: int
        :type desiredTotal: int
        :rtype: bool
        """

        if desiredTotal == 0:
            return True
        if (1 + maxChoosableInteger) * maxChoosableInteger / 2 < desiredTotal:
            return False

        f = [None] * (1 << maxChoosableInteger)
        return self.dfs(0, maxChoosableInteger, desiredTotal, f)

    def dfs(self, now, maxChoosableInteger, desiredTotal, f):
        if f[now] is not None:
            return f[now]
        unused_set = set()
        sum_now = 0
        for num in range(maxChoosableInteger):
            if now & (1 << num):
                sum_now += num + 1
            else:
                unused_set.add(num)

        if sum_now >= desiredTotal:
            f[now] = False
            return False

        for num in unused_set:
            if not self.dfs(now + (1 << num), maxChoosableInteger, desiredTotal, f):
                f[now] = True
                return True

        f[now] = False
        return False
```
