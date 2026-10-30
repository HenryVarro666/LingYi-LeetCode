---
title: "2281. 巫师的总力量和"
aliases: ["yiduobo的每日leetcode 2281.巫师的总力量和"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/math", "leetcode/prefix-sum", "leetcode/monotonic-stack", "题单/常用数据结构", "题单/单调栈", "题单/常用数据结构/一-前缀和", "题单/单调栈/三-贡献法"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/551184357"
zhihu_id: "551184357"
zhihu_title: "yiduobo的每日leetcode 2281.巫师的总力量和"
question_id: "2281"
question: "巫师的总力量和"
problem_url: "https://leetcode.cn/problems/sum-of-total-strength-of-wizards/"
difficulty: "Hard"
rating: 2621
created: "2022-08-08T14:43:44+08:00"
updated: "2022-08-08T14:43:44+08:00"
upvotes: 0
comments: 0
---

# 2281. 巫师的总力量和

> **[yiduobo的每日leetcode 2281.巫师的总力量和](https://zhuanlan.zhihu.com/p/551184357) · 知乎 · 2022-08-08 · 赞同 0**
> 力扣：[2281. 巫师的总力量和](https://leetcode.cn/problems/sum-of-total-strength-of-wizards/) · Hard · 灵茶山艾府：[单调栈 + 前缀和的前缀和（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2281.巫师的总力量和

[力扣](https://leetcode.cn/problems/sum-of-total-strength-of-wizards/)

由于题目的数据规模比较大，因此不能直接枚举所有子串。注意到题目中计算力量和取决于子序列中力量最弱的巫师，那么可以枚举每个巫师，设当前枚举到的巫师为strength[p]，那么可以先找出这个巫师左侧和右侧第一个比这个巫师力量更弱的巫师位置，分别记为l和r，那么在l + 1到r - 1之间所有的包含p这个位置的子串，都将以strength[p]为基准进行计算。

接下来分析具体的计算方式。

在区间[l + 1, r - 1]中，以p为结尾的子串有

[l + 1, p]，[l + 2, p]，...，[p - 1, p], [p, p]

这一些子串的力量总和为

strength[l + 1] + strength[l + 2] + ... + strength[p] +

strength[l + 2] + strenght[l + 3] + ... + strength[p] +

... +

strength[p - 1] + strength[p] +

strength[p]

这是由若干个区间和组成的式子，那么一个自然的想法就是将其转化为前缀和来进行计算。令f表示strength的前缀和，那么上面的式子就可以转化为

(f[p] - f[l]) + (f[p] - f[l + 1]) + ... + (f[p] - f[p - 2]) + (f[p] - f[p - 1])

将括号拆开，就有

f[p] \* (p - l) - (f[l] + f[l + 1] + ... + f[p - 1])

接下来，在区间[l + 1, r - 1]中以p + 1为结尾的子串且包含p的子串有

[l + 1, p + 1], [l + 2, p + 1], ..., [p - 1, p + 1], [p, p + 1]

同样是使用前缀和来取代区间和，就有

(f[p + 1] - f[l]) + (f[p + 1] - f[l + 1]) + ... + (f[p + 1] - f[p - 2]) + (f[p + 1] - f[p - 1])

将括号拆开，就有

f[p + 1] \* (p - l) - (f[l] + f[l + 1] + ... + f[p - 1])

以此类推，接下来会有以p + 2为结尾的子串，以p + 3为结尾的子串，等等，直到以r - 1为结尾的子串。

讲这些子串计算力量的式子全部综合起来，就是

f[p] \* (p - l) - (f[l] + f[l + 1] + ... + f[p - 1]) +

f[p + 1] \* (p - l) - (f[l] + f[l + 1] + ... + f[p - 1]) +

... +

f[r - 1] \* (p - l) - (f[l] + f[l + 1] + ... + f[p - 1])

将前面和后面的部分分别合并，就有

((f[p] + f[p + 1] + ... + f[r - 1]) \* (p - l)) - ((f[l] + f[l + 1] + ... + f[p - 1]) \* (r - p))

这是一个关于f的区间和，那么可以再使用一次前缀和。令g表示f的前缀和，那么这个式子最后就可以写成

(g[r - 1] - g[p - 1]) \* (p - l) + (g[p - 1] - g[l - 1]) \* (p - r)

在这里还可以将g[p - 1]这一项提出来，那么就有

g[r - 1] \* (p - l) + g[p - 1] \* (l - r) + g[l - 1] \* (r - p)

那么以strength[p]为基准的所有子串最终可以提供的力量和就是

(g[r - 1] \* (p - l) + g[p - 1] \* (l - r) + g[l - 1] \* (r - p)) \* strength[p]

于是可以先一趟遍历，预处理出上面的前缀和f以及二级前缀和g。接下来一趟遍历枚举所有的巫师，找出对应的l和r，然后利用上面的式子计算出最终的力量和即可。

至于最后l和r的求解，则是一个经典的单调栈问题，正反两趟遍历使用单调栈求出每个数左侧与右侧第一个更小的数的位置即可。

这里还有一个问题是由于l和r定义的是严格小于当前数的位置，因此对于相等的数将被计算多次，因此需要将l和r的定义稍微修改一下将等号的情况处理掉。我在这里将r的定义改成了右侧第一个小于等于当前数的位置，l的定义不变。

另外在使用前缀和的时候，需要注意判断左侧等于0的情况。

最后附上python代码：

```python
class Solution(object):
    def totalStrength(self, strength):
        """
        :type strength: List[int]
        :rtype: int
        """

        n = len(strength)

        stack = [0]
        right = [n] * n
        for index in range(1, n):
            while stack and strength[stack[-1]] >= strength[index]:
                right[stack[-1]] = index
                stack.pop()
            
            stack.append(index)

        stack = [n - 1]
        left = [-1] * n
        for index in range(n - 2, -1, -1):
            while stack and strength[stack[-1]] > strength[index]:
                left[stack[-1]] = index
                stack.pop()
            
            stack.append(index)
        
        f = [strength[0]]
        g = [strength[0]]
        mod = 10 ** 9 + 7
        for index in range(1, n):
            f.append((f[-1] + strength[index]) % mod)
            g.append((g[-1] + f[-1]) % mod)

        res = 0
        for index in range(n):
            l = left[index]
            r = right[index]
            now = g[r - 1] * (index - l) % mod
            if index > 0:
                now += g[index - 1] * (l - r)
                now %= mod
                if l > 0:
                    now += g[l - 1] * (r - index)
                    now %= mod
            res = (res + now * strength[index]) % mod

        return res
```
