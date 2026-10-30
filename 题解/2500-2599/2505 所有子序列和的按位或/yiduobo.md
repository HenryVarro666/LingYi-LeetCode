---
title: "2505. 所有子序列和的按位或"
aliases: ["yiduobo的每日leetcode 2505.所有子序列和的按位或"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/632748431"
zhihu_id: "632748431"
zhihu_title: "yiduobo的每日leetcode 2505.所有子序列和的按位或"
question_id: "2505"
question: "所有子序列和的按位或"
problem_url: "https://leetcode.cn/problems/bitwise-or-of-all-subsequence-sums/"
created: "2023-05-28T02:16:43+08:00"
updated: "2023-05-28T02:16:43+08:00"
upvotes: 0
comments: 0
---

# 2505. 所有子序列和的按位或

> **[yiduobo的每日leetcode 2505.所有子序列和的按位或](https://zhuanlan.zhihu.com/p/632748431) · 知乎 · 2023-05-28 · 赞同 0**
> 力扣：[2505. 所有子序列和的按位或](https://leetcode.cn/problems/bitwise-or-of-all-subsequence-sums/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2505.所有子序列和的按位或

[力扣](https://leetcode.cn/problems/bitwise-or-of-all-subsequence-sums/)

题目的数据规模比较大，显然是不能暴力计算的，只能从二进制位的角度来考虑这个问题。

对于所有子序列和按位或的结果的二进制中的某一位p，若其为1，那么下面两种情况需要至少满足一种：

1、数组中的某个数二进制表示的p这一位为1

2、数组中某些数的和二进制表示的p这一位为1

那么对于p这一位，不妨遍历整个数组，若其中存在某个数满足条件1，那么p这一位就为1，反之就需要考虑子序列和。

注意到这里有一个隐藏条件，就是如果需要通过累加和来为最终答案的第p位提供这个1，就说明数组中所有数的p这一位都不为1。如果当前的某个子序列的和第p位同样不为1，那么数组中还不属于该子序列的任意数加入到子序列中，其产生的进位也不可能越过p这一位而直接进位到p左侧这一位。

更形象的描述，不妨记当前遍历到的数的二进制表示为XX...X0XX...X，而当前子序列累加和的二进制表示为YY...Y0YY...Y，这里的0都是第p位上的0。在最极端的情况下，两个数0右侧的X和Y全都是1，最终累加结果在p和p后面这些位上产生的进位也不过是11...1110，不可能越过p这一位直接进位到p左侧的这一位。

有了这个结论，就无须考虑累加的顺序，因为并不会出现因为顺序的原因使得子序列的累加和跳过p这一位的进位，因此只需将所有数逐个累加起来，检查累加过程中出现某次累加和在第p位上为1即可。

更进一步的，对于每一位都可以这样考虑，因此在具体实现上只需一趟遍历，每次先将当前遍历到的数与最终答案做按位或，然后将其加入到累加和当中，再将累加和与最终答案做按位或即可。

最后附上python代码：

```python
class Solution(object):
    def subsequenceSumOr(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        res = 0
        s = 0
        for num in nums:
            res |= num
            s += num
            res |= s
        
        return res
```
