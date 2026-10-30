---
title: "2327. 知道秘密的人数"
aliases: ["yiduobo的每日leetcode 2327.知道秘密的人数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/dynamic-programming", "leetcode/prefix-sum", "题单/常用数据结构", "题单/动态规划", "题单/常用数据结构/二-差分", "题单/动态规划/十一-优化-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/558304359"
zhihu_id: "558304359"
zhihu_title: "yiduobo的每日leetcode 2327.知道秘密的人数"
question_id: "2327"
question: "知道秘密的人数"
problem_url: "https://leetcode.cn/problems/number-of-people-aware-of-a-secret/"
difficulty: "Medium"
created: "2022-08-26T23:58:24+08:00"
updated: "2022-08-26T23:58:24+08:00"
upvotes: 0
comments: 0
---

# 2327. 知道秘密的人数

> **[yiduobo的每日leetcode 2327.知道秘密的人数](https://zhuanlan.zhihu.com/p/558304359) · 知乎 · 2022-08-26 · 赞同 0**
> 力扣：[2327. 知道秘密的人数](https://leetcode.cn/problems/number-of-people-aware-of-a-secret/) · Medium · 灵茶山艾府：[两种 O(n) 做法：差分数组/前缀和（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2327.知道秘密的人数

[力扣](https://leetcode.cn/problems/number-of-people-aware-of-a-secret/)

本题与经典的兔子生小兔子的问题非常相似，但是有一点细微的差别，我一开始直接套用经典的做法果然就错了。

对于兔子生小兔子的问题，一般是令f[i]表示当前还存活的兔子数目，然后由

f[i] \= f[i - 1] + 新出生的兔子 - 死亡的兔子

在这里新出生的兔子就是f[i - born]，死亡的兔子就是f[i - death]

对于本题，如果直接套用上面的做法，令f[i]表示到时刻i位置知道秘密的人数，那么就有f[i] \= f[i - 1] + f[i - delay] - f[i - forget]。但是本题的不同之处在于一个人在到达遗忘的天数时会先遗忘，且这个人在时刻i并不能传播出新的秘密，也就是说上面这个递推式中，f[i - delay]的这些人当中，已经有f[i - forget]个人无法在时刻i传递秘密。

一个自然的想法就是利用f[i - forget]来修正f[i - delay]，此时的式子就变成了

f[i] \= f[i - 1] + (f[i - delay] - f[i - forget]) - f[i - forget])

但是很遗憾，这样做也是有问题的，因为最后这一项f[i - forget]可能会出现重复。

以样例来说明。在这6天内，直到秘密的人员情况分别为

A、A、AB、ABC、BCD、BCDEF

从f[3] \= ABC到f[4] \= BCD是符合上面的公式的。在f[3] \= ABC的基础上，f[2]中的AB将传播秘密，但是由于f[0]中的A到了遗忘的时间，因此最终传播的人应该是f[2] - f[0] \= B。另一方面，A自身被遗忘了，因此就有

f[4] \= f[3] + (f[2] - f[0]) - f[0] \= 3

符合预期

但是到了f[4]推导f[5]时就会出现问题。在f[4] \= BCD的基础上，f[3]中的ABC将传播秘密，但是由于f[1]中的A已经到了遗忘的时间，因此最终传播的人应该是f[3] - f[1] \= BC。需要注意的是，此时的f[4]中已经是没有A的了，但是根据上面的式子，依然会减去f[1] \= A这一项，此时就有

f[5] \= f[4] + (f[3] - f[1]) - f[1] \= 4

对应到BCDEF - A，相当于平白无故多减去了一次A

简单总结，就是f[i] \= f[i - 1] + (f[i - delay] - f[i - forget]) - f[i - forget]这个式子中，最后这一项可能对同一个目标进行执行多次。直觉上，如果想要区分f[i - forget]中哪些已经被遗忘过了可能是比较麻烦的，但是注意到式子中f[i - delay] - f[i - forget]这一项是没有任何问题的，那么不妨更改一下f的定义。令f[i]表示到时刻i，知道或曾经知道秘密的总人数。根据这个定义，就可以抛弃掉最后重复计算的这一项f[i - forget]，得到f[i] \= f[i - 1] + f[i - delay] - f[i - forget]

需要注意的是，虽然这个式子与一开始的递推式完全一致，但是此时f表达的含义已经完全不同了。

在计算得到f[n]之后，对于f[n]中的人而言，在f[n - forget]中出现过的人在时刻n必然是不记得秘密的，而剩下的人则都还记得，因此最终答案就是f[n] - f[n - forget]。

最后附上python代码：

```python
class Solution(object):
    def peopleAwareOfSecret(self, n, delay, forget):
        """
        :type n: int
        :type delay: int
        :type forget: int
        :rtype: int
        """

        mod = 10 ** 9 + 7
        f = [0, 1]
        for index in range(2, n + 1):
            f.append(f[-1])
            if index >= delay:
                f[index] += f[index - delay]
                if f[index] >= mod:
                    f[index] -= mod
                if index >= forget:
                    f[index] -= f[index - forget]
                    if f[index] < 0:
                        f[index] += mod
                

        res = f[n]
        if n >= forget:
            res -= f[n - forget]
            if res < 0:
                res += mod
        
        return res
```
