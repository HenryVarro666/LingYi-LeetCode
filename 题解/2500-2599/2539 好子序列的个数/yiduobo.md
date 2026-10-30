---
title: "2539. 好子序列的个数"
aliases: ["yiduobo的每日leetcode 2539.好子序列的个数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/637857322"
zhihu_id: "637857322"
zhihu_title: "yiduobo的每日leetcode 2539.好子序列的个数"
question_id: "2539"
question: "好子序列的个数"
problem_url: "https://leetcode.cn/problems/count-the-number-of-good-subsequences/"
created: "2023-06-18T22:34:41+08:00"
updated: "2023-06-18T22:34:41+08:00"
upvotes: 1
comments: 1
---

# 2539. 好子序列的个数

> **[yiduobo的每日leetcode 2539.好子序列的个数](https://zhuanlan.zhihu.com/p/637857322) · 知乎 · 2023-06-18 · 赞同 1**
> 力扣：[2539. 好子序列的个数](https://leetcode.cn/problems/count-the-number-of-good-subsequences/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2539.好子序列的个数

[力扣](https://leetcode.cn/problems/count-the-number-of-good-subsequences/)

组合数学的题目。由于子序列中各个字符是互不相关的，因此在这里就可以枚举每种字符出现的频率freq，然后对于每种字符分别统计选择freq个该字符的方案数，然后使用乘法原理计算频率为freq的好子序列数目。

具体来说，就是先使用一个哈希表cnt统计每种字符出现的次数。设这些字符出现的最大次数为ma_freq，那么好子序列中每个字符出现的频率就只能在1到ma_freq之间。

接下来从1到ma_freq枚举这个freq，对于当前枚举到的freq，若某种字符char出现的次数cnt[char]小于freq，那么就不能将其加入到子序列中，否则就有C(cnt[char], freq) + 1种可选方案，其中C(cnt[char], freq)表示从cnt[char]个char中选择freq的方案数，而最后的加1则表示还有一种方案是不选择char。

得到每种字符可选的方案数之后，将这些方案数相乘后再减1，即为每种字符出现freq次的好子序列总数。这里需要额外减1的理由是上面的计数方法总会将不选择任何字符这种情况也计算在好子序列的总数中，因此需要将这种情况减掉。

另外，本题涉及到了除法以及取模，因此需要用到乘法逆元。关于乘法逆元的说明可以参考之前的1830题，这里就不展开了。

[yiduobo：yiduobo的每日leetcode 1830.使字符串有序的最少操作次数](https://zhuanlan.zhihu.com/p/467924214)

最后附上python代码：

```python
class Solution(object):
    def countGoodSubsequences(self, s):
        """
        :type s: str
        :rtype: int
        """

        mod = 10 ** 9 + 7

        def quickPow(base, p):
            if p == 1:
                return base

            x = quickPow(base, p / 2)
            x *= x
            x %= mod
            if p & 1:
                x *= base
                x %= mod
            return x

        cnt = {}
        for char in s:
            cnt[char] = cnt.get(char, 0) + 1
        
        ma_freq = max(cnt.values())

        frac = [1]
        inv_frac = [1]
        for index in range(1, ma_freq + 1):
            frac.append(frac[-1] * index % mod)
            inv_frac.append(quickPow(frac[-1], mod - 2))
        
        res = 0
        for same_freq in range(1, ma_freq + 1):
            now = 1
            for freq in cnt.values():
                if freq >= same_freq:
                    now *= (frac[freq] * inv_frac[freq - same_freq] * inv_frac[same_freq] % mod + 1)
                    now %= mod
            
            res += now - 1
            if res < 0:
                res += mod
            if res >= mod:
                res -= mod
        
        return res
```
