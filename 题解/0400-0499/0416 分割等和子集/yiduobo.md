---
title: "416. 分割等和子集"
aliases: ["yiduobo的每日leetcode 416.分割等和子集"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/memoization", "题单/动态规划", "题单/LeetCode-热题-100", "题单/动态规划/三-背包", "题单/LeetCode-热题-100/动态规划"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/190262943"
zhihu_id: "190262943"
zhihu_title: "yiduobo的每日leetcode 416.分割等和子集"
question_id: "416"
question: "分割等和子集"
problem_url: "https://leetcode.cn/problems/partition-equal-subset-sum/"
difficulty: "Medium"
created: "2020-08-19T23:58:23+08:00"
updated: "2020-08-19T23:58:23+08:00"
upvotes: 2
comments: 0
---

# 416. 分割等和子集

> **[yiduobo的每日leetcode 416.分割等和子集](https://zhuanlan.zhihu.com/p/190262943) · 知乎 · 2020-08-19 · 赞同 2**
> 力扣：[416. 分割等和子集](https://leetcode.cn/problems/partition-equal-subset-sum/) · Medium · 灵茶山艾府：[三种写法：记忆化搜索 / 递推 / bitset 优化（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

416.分割等和子集<https://leetcode-cn.com/problems/partition-equal-subset-sum/>

题目要求将所有数分成两个部分，且这两个部分的和相同。那么首先可以计算出所有数的和sum，若sum为奇数，那么显然无法达成目标。若sum为偶数，则表示我们需要从nums中选出一部分数，使得这部分数的和为sum/2。到了这里，题目就转化为了经典的背包问题，使用动态规划求解。

令f\[i\]\[j\]表示对nums中前i个数中能否选取出和刚好为j的子集，于是就有当f\[i - 1\]\[j - nums\[i\]\]为真时，就有f\[i\]\[j\]为真。其具体含义为当前i - 1个数中能选取出和刚好为j - nums\[i\]的子集时，选取第i个数之后，这个子集的和就正好是j。

注意到f[i][j]符合可以滚动的形式，于是可以省去i这一维，直接用f[j]来表示状态。需要注意的是，滚动之后j需要从大到小进行迭代。

最终的时间复杂度为O(sum(nums) \* n)。由于题目中保证每个数都不超过100，那么最坏情况下时间复杂度也就是O(50 \* n^2)。

最后附上python代码：

```python
class Solution(object):
    def canPartition(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """

        n = sum(nums)
        if n & 1:
            return False

        n /= 2
        f = [False] * (n + 1)
        f[0] = True

        for num in nums:
            for index in range(n, num - 1, -1):
                if f[index - num]:
                    f[index] = True

        return f[n]
```
