---
title: "3339. 查找K偶数数组的数量"
aliases: ["yiduobo的每日leetcode 3339.查找K偶数数组的数量"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/25214164304"
zhihu_id: "25214164304"
zhihu_title: "yiduobo的每日leetcode 3339.查找K偶数数组的数量"
question_id: "3339"
question: "查找K偶数数组的数量"
problem_url: "https://leetcode.cn/problems/find-the-number-of-k-even-arrays/"
created: "2025-02-21T03:07:45+08:00"
updated: "2025-02-21T03:08:15+08:00"
upvotes: 0
comments: 0
---

# 3339. 查找K偶数数组的数量

> **[yiduobo的每日leetcode 3339.查找K偶数数组的数量](https://zhuanlan.zhihu.com/p/25214164304) · 知乎 · 2025-02-21 · 赞同 0**
> 力扣：[3339. 查找K偶数数组的数量](https://leetcode.cn/problems/find-the-number-of-k-even-arrays/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3339.查找K偶数数组的数量

[3339. 查找 K 偶数数组的数量 - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-number-of-k-even-arrays/)

题目给出三个整数n、m和k，若一个数组arr中恰好有k个下标满足(arr[i] \* arr[i + 1]) - arr[i] - arr[i + 1]为偶数，那么就称arr是k偶数的。

问长度为n，所有元素取值范围在1到m之间的k偶数数组的数量。

首先分析题目中式子的奇偶性。

对于(arr[i] \* arr[i + 1]) - arr[i] - arr[i + 1]，可以发现，当且仅当arr[i]和arr[i + 1]都是偶数时，式子的结果才是偶数。也就是说题目的问题实际上就是问长度为n，所有元素取值范围在1到m之间，且恰好又k组相邻偶数对的数组的数量。

接下来就可以利用动态规划来进行求解了。

令f[length][pair]表示长度为length，其中有pair组相邻偶数对，且最后这个元素为偶数的数组数目，而g[length][pair]则表示长度为length，其中有pair组相邻偶数对，且最后这个元素为奇数的数组数目。

那么对于f[length][pair]：

1、可以在f[length - 1][pair - 1]的最后填充一个偶数，形成新的偶数对

2、可以在g[length - 1][pair]的最后填充一个偶数，不形成新的偶数对

由于1到m中偶数的数量even \= m // 2，因此就有

f[length][pair] \= (f[length - 1][pair - 1] + g[length - 1][pair]) \* even

而对于g[length][pair]，由于最后填充的是奇数，不可能形成新的偶数对，因此这里的pair只能来自于上一轮。而1到m中奇数的数量odd \= m - even，因此就有

g[length][pair] \= (f[length - 1][pair] + g[length - 1][pair]) \* odd

特别的，对于pair \= 0的情况，由于不存在f[length][-1]，因此f[length][0]只能从g[length - 1][0]，而g[length][0]则不受影响。

另一方面，初始情况下f[1][0] \= even，而g[1][0] \= odd。

另外注意到f和g每一轮都只和上一轮的状态有关，因此可以互相滚动优化掉length这一维。

最后附上python代码：

```python
class Solution(object):
    def countOfArrays(self, n, m, k):
        """
        :type n: int
        :type m: int
        :type k: int
        :rtype: int
        """
        
        f = [0] * (k + 1)
        g = [0] * (k + 1)

        even = m // 2
        odd = m - even

        f[0] = even
        g[0] = odd

        mod = 10 ** 9 + 7
        for index in range(1, n):
            for pair in range(k, 0, -1):
                f[pair], g[pair] = (f[pair - 1] + g[pair]) * even % mod, (f[pair] + g[pair]) * odd % mod
            f[0], g[0] = g[0] * even % mod, (f[0] + g[0]) * odd % mod
        
        return (f[k] + g[k]) % mod
```
