---
title: "4002. 统计有效序列的数目"
aliases: ["yiduobo的每日leetcode 4002.统计有效序列的数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/combinatorics", "leetcode/number-theory", "题单/数学算法", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2065595059802732088"
zhihu_id: "2065595059802732088"
zhihu_title: "yiduobo的每日leetcode 4002.统计有效序列的数目"
question_id: "4002"
question: "统计有效序列数目"
problem_url: "https://leetcode.cn/problems/count-valid-sequences/"
difficulty: "Medium"
rating: 1912
created: "2026-07-29T00:47:35+08:00"
updated: "2026-07-29T00:47:35+08:00"
upvotes: 0
comments: 0
---

# 4002. 统计有效序列的数目

> **[yiduobo的每日leetcode 4002.统计有效序列的数目](https://zhuanlan.zhihu.com/p/2065595059802732088) · 知乎 · 2026-07-29 · 赞同 0**
> 力扣：[4002. 统计有效序列数目](https://leetcode.cn/problems/count-valid-sequences/) · Medium · 灵茶山艾府：[组合数学（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4002.统计有效序列的数目

<https://leetcode.cn/problems/count-valid-sequences/>

题目给出两个正整数n和k。

一个有效序列指的是一个由k个正整数组成的序列，满足：

- 序列中所有整数之和等于n
- 序列中所有整数的乘积为偶数

现在要求返回有效序列的数目，答案对10^9 + 7取模。

题目相当于要将n拆分为k个正整数，且这些正整数的乘积为偶数。

乘积为偶数，意味着拆分出来的正整数中至少存在一个偶数。直观感觉上，直接计算的话去重会比较麻烦，不如反过来思考，即计算出所有可能的划分方案数，减去划分出来的元素都是奇数的划分方案数，得到的就是至少存在一个偶数的划分方案数。

接下来分别考虑所有可能的划分方案数以及全部都是奇数的划分方案数。

对于这类划分方案问题，插板法是经典的做法。

首先，将n拆分为k个正整数，可以认为是一排n个小球，在这n个球的n - 1个空隙之间插入k - 1个隔板，需要注意同一个缝隙中不能插入多个隔板。这样一来，这n个球就会被分为k个非空的段，相当于n被拆分为了k个正整数。那么这里插入隔板的方案数，就是从n - 1个空隙中选择k - 1个的方案数，即C(n - 1, k - 1)。

接下来，将n拆分为k个正奇数，则可以先进行一些变形。同样是一排n个小球，插入k - 1个隔板。目标是插入隔板后，得到的k个段都包含奇数个小球。对于这k段，可以先为每一段补充一个额外的小球，这样一来每一段就都是偶数个小球。接下来，按顺序两个一组，那么问题就变成了将一共m \= (n + k) // 2组小球，分为k段的方案数。根据上面的隔板法，方案数就是C(m - 1, k - 1)。

需要注意的是，这种情况下可以认为是去掉落单的小球然后两两分组，但是这样一来，就可以出现两个隔板在同一个空隙中的情况，对于这个问题，处理方法恰好就是加入虚拟的组然后插入隔板，本质上就是上面补充额外小球的处理方法。

另外，若这里的(n + k)为奇数，那么就不可能将n划分为k个奇数，可以直接通过上面无法两个一组分组得出，也可以通过n和k的奇偶性得出。

最后，由于题目涉及到较大的组合数计算以及取模，因此在这里需要用到乘法逆元。相关的内容可以参考之前的3405题：

[yiduobo的每日leetcode 3405.统计恰好有K个相等相邻元素的数组数目](https://zhuanlan.zhihu.com/p/31401526455)

最后附上python代码：

```python
class Solution(object):
    def countValidSequences(self, n, k):
        """
        :type n: int
        :type k: int
        :rtype: int
        """
        
        inv = [1, 1]
        fac = [1, 1]
        inv_fac = [1, 1]
        mod = 10 ** 9 + 7
        for v in range(2, n):
            inv.append(-(mod // v) * inv[mod % v] % mod)
            fac.append(fac[-1] * v % mod)
            inv_fac.append(inv_fac[-1] * inv[-1] % mod)
        
        res = fac[n - 1] * inv_fac[k - 1] % mod * inv_fac[n - k] % mod
        if (n + k) % 2 == 0:
            m = (n + k) // 2
            odd = fac[m - 1] * inv_fac[k - 1] % mod * inv_fac[m - k] % mod
            res -= odd
            if res < 0:
                res += mod
        
        return res
```
