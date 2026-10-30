---
title: "1819. 序列中不同最大公约数的数目"
aliases: ["yiduobo的每日leetcode 1819.序列中不同最大公约数的数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/math", "leetcode/number-theory", "题单/数学算法", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/466389824"
zhihu_id: "466389824"
zhihu_title: "yiduobo的每日leetcode 1819.序列中不同最大公约数的数目"
question_id: "1819"
question: "序列中不同最大公约数的数目"
problem_url: "https://leetcode.cn/problems/number-of-different-subsequences-gcds/"
difficulty: "Hard"
rating: 2540
created: "2022-02-11T22:01:26+08:00"
updated: "2022-02-11T22:01:26+08:00"
upvotes: 0
comments: 0
---

# 1819. 序列中不同最大公约数的数目

> **[yiduobo的每日leetcode 1819.序列中不同最大公约数的数目](https://zhuanlan.zhihu.com/p/466389824) · 知乎 · 2022-02-11 · 赞同 0**
> 力扣：[1819. 序列中不同最大公约数的数目](https://leetcode.cn/problems/number-of-different-subsequences-gcds/) · Hard · 灵茶山艾府：[击败100%！枚举GCD+循环优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1819.序列中不同最大公约数的数目

[力扣](https://leetcode-cn.com/problems/number-of-different-subsequences-gcds/)

首先，最大公约数有一个性质就是若干个数的最大公约数必然等于其中某两个数的最大公约数，也就是说，nums的各个子序列可能得到的最大公约数可以通过两两枚举nums中的数对，然后计算数对的最大公约数得到。

不过在这里，由于题目中给出的n规模很大，因此直接暴力两两枚举数对的算法肯定是行不通的。注意到nums的范围虽然也不算小，但是依然处在可枚举的范围之内，那么不妨转换思路，从1到max(nums)枚举每个数，检测当前枚举到的数是否是nums中某个序列的最大公约数。

对于当前枚举到的数gcd，若nums中存在某个序列的最大公约数为gcd，那么这个序列中的数必然都是gcd的倍数。换言之，在这里可以从gcd开始，按照类似筛法的做法依次检测gcd，gcd \* 2，gcd \* 3，...，gcd \* k是否在nums中。若在nums中，那么将这个数提出来。遍历完后，就得到了nums的一个子序列，里面的所有数都是gcd的倍数。接下来只需要判断这个子序列中的数的最大公约数是否恰好就是gcd即可。

在时间复杂度方面，这里的时间复杂度应该是maxn \* (maxn / 1 + maxn / 2 + ... + maxn / maxn)，一般认为这个就是O(maxn \* log(maxn))这个级别，完全可以满足题目要求。

最后附上python代码：

```python
class Solution(object):
    def countDifferentSubsequenceGCDs(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        num_set = set(nums)
        max_num = max(nums)
        res = 0
        for gcd in range(1, max_num + 1):
            now_gcd = None
            for now in range(gcd, max_num + 1, gcd):
                if now in num_set:
                    if now_gcd is None:
                        now_gcd = now
                    else:
                        x, y = now_gcd, now
                        while x:
                            x, y = y % x, x
                        now_gcd = y
            
            if now_gcd == gcd:
                res += 1

        return res
```
