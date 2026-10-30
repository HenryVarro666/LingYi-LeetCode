---
title: "3352. 统计小于N的K可约简整数"
aliases: ["yiduobo的每日leetcode 3352.统计小于N的K可约简整数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/十-数位-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/26399841385"
zhihu_id: "26399841385"
zhihu_title: "yiduobo的每日leetcode 3352.统计小于N的K可约简整数"
question_id: "3352"
question: "统计小于 N 的 K 可约简整数"
problem_url: "https://leetcode.cn/problems/count-k-reducible-numbers-less-than-n/"
difficulty: "Hard"
rating: 2451
created: "2025-02-26T02:27:35+08:00"
updated: "2025-02-26T02:27:35+08:00"
upvotes: 1
comments: 1
---

# 3352. 统计小于N的K可约简整数

> **[yiduobo的每日leetcode 3352.统计小于N的K可约简整数](https://zhuanlan.zhihu.com/p/26399841385) · 知乎 · 2025-02-26 · 赞同 1**
> 力扣：[3352. 统计小于 N 的 K 可约简整数](https://leetcode.cn/problems/count-k-reducible-numbers-less-than-n/) · Hard · 灵茶山艾府：[线性 DP + 数位 DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3352.统计小于N的K可约简整数

[3352. 统计小于 N 的 K 可约简整数 - 力扣（LeetCode）](https://leetcode.cn/problems/count-k-reducible-numbers-less-than-n/description/)

题目给出一个二进制字符串s，表示数字n的二进制形式，另外给出一个整数k。接下来定义一次操作为对于某个整数x，将x替换为x二进制表示中1的数量。若n可以在最多k次操作下约简到1，则称n为k可约简整数。

例如对于x \= 6，对应的二进制为110，其中有两个1，那么在一次操作后，其将被替换成2。接下来对于2，对应的二进制为10，其中有一个1，在另一次操作后，其将被替换成1。

问所有小于n的正整数中有多少个k可约简整数。

题目中s的长度可以达到800位，也就是说n最多是一个800位的二进制数，暴力枚举显然是不行的，必须从数位上先办法解决。

对于这个800位，意味这对于任意在1到n之间的整数，在执行一次操作之后就会变为一个1到800之间的整数，因此在这里可以反过来思考，不妨设s的长度为m，那么就可以先从1遍历到m，计算出将这些数变为1所需的操作数，将对应的结果记为数组f，其中f[one]表示将one约简到1所需的操作数。

接下来再次从1遍历到m，若当前的f[one] + 1小于等于k，那么对于所有的满足一下三个条件的数，经过一次操作先变为one，然后经过f[one]次操作变为1，这样一来总的操作数就是f[one] + 1，而这个数应该被计入答案中。这三个条件分别是：

1、这个数的二进制表示的位数不超过m位

2、这个数的二进制表示中恰好有one个1

3、这个数小于n

由于存在条件3的限制，对于这个问题使用数位动态规划是比较合适的做法。

---

令g[level][rest_one][flag]表示目前填充到第level位，后续还有rest_one个1需要填充进去，且目前已经填充的前缀与s的前缀的大小关系为flag时的合法填充方案。其中flag为true时表示已填充的前缀与s的前缀相等，而flag为false则表示已填充的前缀小于s的前缀。

接下来对于g[level][rest_one][flag]：

1、首先考虑边界情况：若level等于m，说明已经填充完毕，此时需要检测rest_one是否为0，且flag是否为false，因为在这里要求1全部用完，且二进制表示小于n。若都满足，则g[level][rest_one][flag]为1，否则为0。

2、接下来考虑一般情况，具体来说，可以分别考虑在第level位上填充1或者0将会发生什么：

2-1）首先考虑填充1，在这里有一个前提条件是rest_one > 0，接下来：

2-1-1）若flag为false：

这种情况下，直接在第level位上填充1是没有问题的，且同时接下来的flag依然为false，于是就有

g[level][rest_one][flag] +\= g[level + 1][rest_one - 1][flag]

2-1-2）若flag为true，且s[level]为1：

这种情况下也可以在第level位上填充1，但是填充后的前缀与s的前缀依然是相等的，因此接下来的flag依然为true，于是同样有

g[level][rest_one][flag] +\= g[level + 1][rest_one - 1][flag]

2-1-3）其他情况：

其他情况下level这一位都不能填充1，因为填充1之后得到的数必然大于n

2-2）然后考虑填充0。无论哪种情况都可以填充0，不过填充0时依然要考虑对flag的影响：

2-2-1）若flag为true，且s[level]为0：

这种情况下在第level位上填充0，填充后的前缀与s的前缀依然是相等的，因此接下来的flag依然为true，于是有

g[level][rest_one][flag] +\= g[level + 1][rest_one][flag]

2-2-2）其他情况：

其他所有的情况下后续的flag都为false，于是有

g[level][rest_one][flag] +\= g[level + 1][rest_one][false]

---

这样一来，二进制长度不超过m，且其中有one个1，同时小于n的整数数量就是g[1][one - 1][true] + g[1][one][false]，分别表示在最高位上分别填充1和0时可以得到的合法填充方案数。若f[one] + 1小于等于k，就可以将上面这个和累加到答案中。

另外在具体实现上，使用记忆化搜索来求解g写起来更方便。

最后附上python代码：

```python
class Solution(object):
    def countKReducibleNumbers(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: int
        """
        
        m = len(s)
        f = [0, 0]
        for v in range(2, m + 1):
            x = v
            one = 0
            while x:
                x -= x & -x
                one += 1
            f.append(f[one] + 1)
        
        g = [[[None] * 2 for _ in range(m + 1)] for _ in range(m)]
        res = 0
        mod = 10 ** 9 + 7

        def dfs(level, rest_one, flag, g):
            if level == m:
                if rest_one == 0 and flag == 0:
                    return 1
                return 0

            if g[level][rest_one][flag] is None:
                g[level][rest_one][flag] = 0
                if rest_one > 0:
                    if not flag:
                        g[level][rest_one][flag] += dfs(level + 1, rest_one - 1, flag, g)
                        g[level][rest_one][flag] %= mod
                    elif s[level] == '1':
                        g[level][rest_one][flag] += dfs(level + 1, rest_one - 1, flag, g)
                        g[level][rest_one][flag] %= mod
                
                if flag and s[level] == '0':
                    g[level][rest_one][flag] += dfs(level + 1, rest_one, flag, g)
                    g[level][rest_one][flag] %= mod
                else:
                    g[level][rest_one][flag] += dfs(level + 1, rest_one, 0, g)
                    g[level][rest_one][flag] %= mod
            
            return g[level][rest_one][flag]

        for one in range(1, m + 1):
            if f[one] + 1 <= k:
                res = (res + dfs(1, one - 1, 1, g) + dfs(1, one, 0, g)) % mod
        
        return res
```
