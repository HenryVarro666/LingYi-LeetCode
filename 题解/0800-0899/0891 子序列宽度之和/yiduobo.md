---
title: "891. 子序列宽度之和"
aliases: ["yiduobo的每日leetcode 891.子序列宽度之和"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/math", "leetcode/combinatorics", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/352203478"
zhihu_id: "352203478"
zhihu_title: "yiduobo的每日leetcode 891.子序列宽度之和"
question_id: "891"
question: "子序列宽度之和"
problem_url: "https://leetcode.cn/problems/sum-of-subsequence-widths/"
difficulty: "Hard"
rating: 2183
created: "2021-02-22T23:25:11+08:00"
updated: "2021-02-22T23:25:11+08:00"
upvotes: 0
comments: 0
---

# 891. 子序列宽度之和

> **[yiduobo的每日leetcode 891.子序列宽度之和](https://zhuanlan.zhihu.com/p/352203478) · 知乎 · 2021-02-22 · 赞同 0**
> 力扣：[891. 子序列宽度之和](https://leetcode.cn/problems/sum-of-subsequence-widths/) · Hard · 灵茶山艾府：[计算每个元素对答案的贡献，多解法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

891.子序列宽度之和

[力扣](https://leetcode-cn.com/problems/sum-of-subsequence-widths/)

注意到题目描述虽然是子序列，但是在计算宽度时只关心序列中数值的大小，而不关心序列下标相关的东西。换言之，我们即使随意打乱A，最后得到的答案依然不变。

对于一个序列而言，其宽度为序列中的最大值减去最小值，那么我们如果不从序列的角度出发，而是从每个具体的数出发的话，那么对于一个数x而言，其只有在成为某个序列的最大值或者最小值时才会发挥作用。

当x与比x小的数任意组合成序列时，都会被当做序列的最大值做加法；同理，当x与比x大的数任意组合成序列时，都会被当做序列的最小值做减法。不妨设x为A中第K大的数，那么一共就有k - 1个小于等于x的数，一共有2^(k - 1)中组合方式，这意味着x将被累加2^(k - 1)次；同理，大于等于x的数就有n - k个，这意味着x将被减去2^(n - k)次。于是就可以得出一个结论：A中第k大的数x将为答案提供x \* (2^(k - 1) - 2^(n - k))。

到了这里，就有了一种比较简洁的做法。对A从小到大进行排序然后从头到尾遍历，对于当前的A[index]，由于下标从0开始，因此这里的A[index]应该是A中第index + 1大的数，于是应该让答案加上A[index] \* (2^index - 2^(n - index - 1))。我们可以预处理出2的幂次，剩下的就是简单的减法和乘法操作了。

最后附上python代码：

```python
class Solution(object):
    def sumSubseqWidths(self, A):
        """
        :type A: List[int]
        :rtype: int
        """
        
        n = len(A)
        pow2 = [1]
        mod = 10 ** 9 + 7
        for index in range(n):
            pow2.append((pow2[-1] + pow2[-1]) % mod)
        
        res = 0
        for index, num in enumerate(sorted(A)):
            res += num * (pow2[index] - pow2[n - index - 1])
            res %= mod
        
        return res
```
