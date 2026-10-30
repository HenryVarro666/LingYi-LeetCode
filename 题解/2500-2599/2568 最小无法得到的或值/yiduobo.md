---
title: "2568. 最小无法得到的或值"
aliases: ["yiduobo的每日leetcode 2568.最小无法得到的或值"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/位运算", "题单/贪心算法", "题单/位运算/八-思维题", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/641028903"
zhihu_id: "641028903"
zhihu_title: "yiduobo的每日leetcode 2568.最小无法得到的或值"
question_id: "2568"
question: "最小无法得到的或值"
problem_url: "https://leetcode.cn/problems/minimum-impossible-or/"
difficulty: "Medium"
rating: 1754
created: "2023-07-02T22:14:40+08:00"
updated: "2023-07-02T22:14:40+08:00"
upvotes: 0
comments: 0
---

# 2568. 最小无法得到的或值

> **[yiduobo的每日leetcode 2568.最小无法得到的或值](https://zhuanlan.zhihu.com/p/641028903) · 知乎 · 2023-07-02 · 赞同 0**
> 力扣：[2568. 最小无法得到的或值](https://leetcode.cn/problems/minimum-impossible-or/) · Medium · 灵茶山艾府：[脑筋急转弯+lowbit优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2568.最小无法得到的或值

[力扣](https://leetcode.cn/problems/minimum-impossible-or/)

由于涉及到或运算，那么在这里就应该从位的角度出发考虑问题。又由于或运算是无法产生进位的，因此可以从2的幂次出发来考虑问题。

不妨设当前已经可以得到的或值为1到k，那么对于k + 1：

1、若k + 1是2的幂次，那么就要求数组中必须恰好存在k + 1，否则无法得到。

2、若k + 1不是2的幂次，那么不妨设p为最大的满足2^p \< k + 1的数。由情况1可知，数组中必然存在某个数恰好等于2^p，同时k + 1 - 2^p小于k同时小于2^p，因此也必然可以通过数组中除2^p之外的数构造得到。这样一来，这两个数做或运算，就得到了k + 1。

综合上面两种情况可以发现，最小无法得到的或值必然是最小的不存在与数组中的2的幂次，于是可以将数组中的数加入到集合中，然后从1开始逐个检测2的幂次是否出现在集合中，首个没有出现的2的幂次即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def minImpossibleOR(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        num_set = set(nums)
        res = 1
        while res in num_set:
            res <<= 1
        
        return res
```
