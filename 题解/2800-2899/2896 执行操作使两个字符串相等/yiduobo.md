---
title: "2896. 执行操作使两个字符串相等"
aliases: ["yiduobo的每日leetcode 2896.执行操作使两个字符串相等"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/brainteaser", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/663183867"
zhihu_id: "663183867"
zhihu_title: "yiduobo的每日leetcode 2896.执行操作使两个字符串相等"
question_id: "2896"
question: "执行操作使两个字符串相等"
problem_url: "https://leetcode.cn/problems/apply-operations-to-make-two-strings-equal/"
difficulty: "Medium"
rating: 2172
created: "2023-10-25T02:34:21+08:00"
updated: "2023-10-25T02:34:21+08:00"
upvotes: 0
comments: 0
---

# 2896. 执行操作使两个字符串相等

> **[yiduobo的每日leetcode 2896.执行操作使两个字符串相等](https://zhuanlan.zhihu.com/p/663183867) · 知乎 · 2023-10-25 · 赞同 0**
> 力扣：[2896. 执行操作使两个字符串相等](https://leetcode.cn/problems/apply-operations-to-make-two-strings-equal/) · Medium · 灵茶山艾府：[两种方法：从 O(n^2) 到 O(n)（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2896.执行操作使两个字符串相等

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/apply-operations-to-make-two-strings-equal/)

拿到题目的第一反应是贪心，也就是从左向右一趟遍历，每次找出最靠前的两个不匹配的1，将其中一个翻转到另一个所在的位置。这个做法在不存在x代价操作的情况下应该是没有问题，但是如果存在x代价操作，贪心的前提就不成立了。考虑到题目的数据规模较大，在这里就应该想办法向动态规划靠拢。

如果想使用动态规划，有一个不好处理的地方就是x代价操作的目标是不好选定的，那么不妨简化一下思路，将其视为一种无差别消除的机会。也就是说，对于某个不匹配的s1[index]和s2[index]，可以使用x的代价，将二者变为匹配，同时还有一次免费强制匹配的机会留给后续的字符串使用。基于这一点，在加上常规的相邻字符同时翻转，就可以得到一种状态表示：令f[index][reversed][free]表示要使得s1和s2在下标0到index这一段前缀匹配上，同时当前是否翻转了s1[index]和s1[index + 1]，且还剩下free次无差别消除的机会时，所需的最小代价。

f数组的初始值都为空，表示无法到达该状态。那么对于f[index]：

1、首先是边界情况：

若s1[0]与s2[0]相同，那么就有f[0][0][0] \= 0，也就是直接跳过下标0，什么都不需要做，此时的代价为0。

反之，则有f[0][1][0] \= 1，表示在这里可以翻转s1[0]与s1[1]，此时的代价为1。除此之外，还有f[0][0][1] \= x，表示在这里使用代价x操作无差别消除下标0的不匹配，同时留下一次免费消除的机会给后面的字符串使用，此时的代价为x。

除此之外，其他的f[0][reversed][free]都应该为空。

2、接下是index > 0且s1[index]与s2[index]相同的情况：

2-1）若存在某个f[index - 1][0][free]不为空，那么可以在此基础上直接跳过下标index，于是就有f[index][0][free] \= f[index - 1][0][free]

2-2）若存在某个f[index - 1][1][free]不为空，那么可以在此基础上将s1[index]与s1[index + 1]同时翻转，抵消掉之前翻转的影响，于是就有f[index][1][free] \= f[index - 1][1][free] + 1

于是在这里就应该枚举所有的free，求解上面的f[index][0][free]以及f[index][1][free]

3、最后是index > 0且s1[index]与s2[index]不同的情况：

3-1）若存在某个f[index - 1][0][free]不为空，且free > 0。此时就可以使用一次无差别消除，那么就有f[index][0][free - 1] \= min(f[index][0][free - 1], f[index - 1][0][free])

3-2）若存在某个f[index - 1][0][free]不为空，且free \< n / 2，此时就可以使用代价x操作，那么就有f[index][0][free + 1] \= min(f[index][0][free + 1], f[index - 1][0][free] + x)。这里free \< n / 2的理由是长度为n的字符串中使用无法别消除的次数不应该超过n / 2次

3-3）若存在某个f[index - 1][0][free]不为空，那么在这里也可以让s1[index]与s1[index + 1]翻转，于是就有f[index][1][free] \= min(f[index][1][free], f[index - 1][0][free] + 1)

3-4）若存在某个f[index - 1][1][free]不为空，那么由于s1[index]已经与s1[index - 1]在上一步一起翻转过了，那么在这里无需任何操作，于是就有f[index][0][free] \= min(f[index][0][free], f[index - 1][1][free])

在这里同样是枚举所有的free，求解上面的f[index][0][free]以及f[index][1][free]

值得一提的是，上面有几种情况是无需考虑的，也就是当前以及匹配上时，不需要画蛇添足额外进行翻转或者代价x操作。

计算完成后，若f[-1][0][0]为空，说明无解，此时则应该返回-1，否则就应该返回f[-1][0][0]作为最终答案。这里reversed为0很好理解，而free为0则是因为不匹配的1总是成对出现的，因此当某一个位置使用了无差别x操作后，必然另一个位置可以享受到这次免费的消除，如果最后都没有使用过的话显然是划不来的。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, s1, s2, x):
        """
        :type s1: str
        :type s2: str
        :type x: int
        :rtype: int
        """

        n = len(s1)

        f = [[[None] * (n / 2 + 1) for _ in range(2)] for _ in range(n)]
        if s1[0] == s2[0]:
            f[0][0][0] = 0
        else:
            f[0][1][0] = 1
            if n >= 2:
                f[0][0][1] = x
        
        for index in range(1, n):
            if s1[index] == s2[index]:
                for free in range(n / 2 + 1):
                    if f[index - 1][0][free] is not None:
                        f[index][0][free] = f[index - 1][0][free]
                    if f[index - 1][1][free] is not None:
                        f[index][1][free] = f[index - 1][1][free] + 1
            
            else:
                for free in range(n / 2 + 1):
                    if f[index - 1][0][free] is not None:
                        if free > 0 and (f[index][0][free - 1] is None or f[index][0][free - 1] > f[index - 1][0][free]):
                            f[index][0][free - 1] = f[index - 1][0][free]
                        if free < n / 2 and (f[index][0][free + 1] is None or f[index][0][free + 1] > f[index - 1][0][free] + x):
                            f[index][0][free + 1] = f[index - 1][0][free] + x
                        if f[index][1][free] is None or f[index][1][free] > f[index - 1][0][free]:
                            f[index][1][free] = f[index - 1][0][free] + 1
                    
                    if f[index - 1][1][free] is not None and (f[index][0][free] is None or f[index][0][free] > f[index - 1][1][free]):
                        f[index][0][free] = f[index - 1][1][free]
        
        if f[-1][0][0] is None:
            return -1
        return f[-1][0][0]
```
