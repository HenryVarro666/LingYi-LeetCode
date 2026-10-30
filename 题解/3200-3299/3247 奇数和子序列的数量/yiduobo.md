---
title: "3247. 奇数和子序列的数量"
aliases: ["yiduobo的每日leetcode 3247.奇数和子序列的数量"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/721374510"
zhihu_id: "721374510"
zhihu_title: "yiduobo的每日leetcode 3247.奇数和子序列的数量"
question_id: "3247"
question: "奇数和子序列的数量"
problem_url: "https://leetcode.cn/problems/number-of-subsequences-with-odd-sum/"
created: "2024-09-22T02:46:53+08:00"
updated: "2024-09-22T02:46:53+08:00"
upvotes: 1
comments: 0
---

# 3247. 奇数和子序列的数量

> **[yiduobo的每日leetcode 3247.奇数和子序列的数量](https://zhuanlan.zhihu.com/p/721374510) · 知乎 · 2024-09-22 · 赞同 1**
> 力扣：[3247. 奇数和子序列的数量](https://leetcode.cn/problems/number-of-subsequences-with-odd-sum/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3247.奇数和子序列的数量

[. - 力扣（LeetCode）](https://leetcode.cn/problems/number-of-subsequences-with-odd-sum/description/)

题目给出一个数组nums，要求计算其中和为奇数的子序列的数目。

经典的动态规划问题。令f[index]和g[index]分别表示从下标0到i中和为奇数以及偶数的子序列的数目，那么在初始状况下，若nums[0]为奇数，有f[0] \= 1，g[0] \= 0，否则又f[0] \= 0，g[0] \= 1。

接下来对于index > 0的情况：

1、若nums[index]为偶数，那么将其加入到任意和为奇数的子序列，得到的依然是和为奇数的子序列，将其加入到任意和为偶数的子序列，得到的依然是和为偶数的子序列，那么就有

f[index] \= f[index - 1] + f[index - 1]，其中第一个f[index - 1]表示丢弃nums[index]，第二个f[index - 1]则表示在之前和为奇数的子序列的基础上加入nums[index]。

g[index] \= g[index - 1] + g[index - 1] + 1，其中第一个g[index - 1]表示丢弃nums[index]，第二个g[index - 1]则表示在之前和为偶数的子序列的基础上加入nums[index]，而最后的1则表示仅保留nums[index]形成新的和为偶数的子序列。

2、若nums[index]为奇数，此时与上面对称，有

f[index] \= f[index - 1] + g[index - 1] + 1，其中f[index - 1]表示放弃nums[index]，g[index - 1]表示在和为偶数的子序列的基础上加入nums[index]，最后的1则表示仅保留nums[index]形成新的和为奇数的子序列。

g[index] \= g[index - 1] + f[index - 1]，其中g[index - 1]表示放弃nums[index]，f[index - 1]表示在和为奇数的子序列的基础上加入nums[index]。

注意到这里f和g的每一轮都只和上一轮有关，因此可以使用变量迭代来节省掉数组的空间。

最后附上python代码：

```python
class Solution(object):
    def subsequenceCount(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        if nums[0] % 2 == 0:
            f, g = 0, 1
        else:
            f, g = 1, 0
        
        mod = 10 ** 9 + 7
        for v in nums[1:]:
            if v % 2 == 0:
                f, g = f + f, g + g + 1
            else:
                f, g = f + g + 1, f + g
        
            f %= mod
            g %= mod

        return f
```
