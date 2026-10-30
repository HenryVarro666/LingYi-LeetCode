---
title: "1994. 好子集的数目"
aliases: ["yiduobo的每日leetcode 1994.好子集的数目"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/500207975"
zhihu_id: "500207975"
zhihu_title: "yiduobo的每日leetcode 1994.好子集的数目"
question_id: "1994"
question: "好子集的数目"
problem_url: "https://leetcode.cn/problems/the-number-of-good-subsets/"
created: "2022-04-17T22:07:45+08:00"
updated: "2022-04-17T22:08:14+08:00"
upvotes: 0
comments: 0
---

# 1994. 好子集的数目

> **[yiduobo的每日leetcode 1994.好子集的数目](https://zhuanlan.zhihu.com/p/500207975) · 知乎 · 2022-04-17 · 赞同 0**
> 力扣：[1994. 好子集的数目](https://leetcode.cn/problems/the-number-of-good-subsets/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

1994.好子集的数目

[力扣](https://leetcode-cn.com/problems/the-number-of-good-subsets/)

由于题目中不能出现相同的因子，而小于30的质因子总共只有2、3、5、7、11、13、17、19、23、29这10种，那么完全可以使用状态压缩动态规划，令f[state]表示当前因子组合为state时有多少种合法的子集数目，接下来的问题就变成了一个背包问题。

首先将nums中的数用dict收集起来，并剔除其中不可用的数。

接下来枚举可用的数num，设其对应的状态表示为factor，其出现在nums中的次数为cnt。再从最大可能的状态1023，到factor + 1枚举所有的state，若当前state满足state中包含了factor，即state & factor \= factor，那么就有

f[state] +\= f[state ^ factor] \* cnt

表示从这cnt个num中任选一个加入到state^factor这个集合中可以得到的集合数目

另外，还需要单独将f[factor]赋值为cnt

除了上面动态规划对于质因子的计算之外，还有因子1可以使用。由于1并不会影响集合的合法性，因此若现在有k个1，那么就有2^k中可用的选择方法，因此最终答案就是f之和乘以2^k。

最后附上python代码：

```python
class Solution(object):
    def numberOfGoodSubsets(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        mod = 10 ** 9 + 7
        cnt_dict = {}
        for num in nums:
            cnt_dict[num] = cnt_dict.get(num, 0) + 1
        
        pow2 = 1
        for index in range(cnt_dict.get(1, 0)):
            pow2 += pow2
            if pow2 >= mod:
                pow2 -= mod
        
        prime_mapping = {2:  1,
                         3:  2,
                         6:  3,
                         5:  4,
                         10: 5,
                         15: 6,
                         30: 7,
                         7:  8,
                         14: 9,
                         21: 10,
                         11: 16,
                         22: 17,
                         13: 32,
                         26: 33,
                         17: 64,
                         19:128,
                         23:256,
                         29:512}

        res = 0
        f = {x : 0 for x in range(1024)}
        
        for num, cnt in cnt_dict.items():
            if num in prime_mapping:
                factor = prime_mapping[num]
                for state in range(1023, factor, -1):
                    if (state & factor) == factor:
                        f[state] += f[state ^ factor] * cnt
                        f[state] %= mod
                f[factor] += cnt
                if f[factor] >= mod:
                    f[factor] -= mod

        return sum(f.values()) * pow2 % mod
```
