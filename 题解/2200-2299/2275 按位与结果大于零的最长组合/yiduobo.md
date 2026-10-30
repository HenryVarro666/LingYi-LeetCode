---
title: "2275. 按位与结果大于零的最长组合"
aliases: ["yiduobo的每日leetcode 2275.按位与结果大于零的最长组合"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/brainteaser", "leetcode/enumeration", "题单/位运算", "题单/位运算/四-拆位-/-贡献法"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/550748088"
zhihu_id: "550748088"
zhihu_title: "yiduobo的每日leetcode 2275.按位与结果大于零的最长组合"
question_id: "2275"
question: "按位与结果大于零的最长组合"
problem_url: "https://leetcode.cn/problems/largest-combination-with-bitwise-and-greater-than-zero/"
difficulty: "Medium"
rating: 1642
created: "2022-08-07T01:28:48+08:00"
updated: "2022-08-07T01:28:48+08:00"
upvotes: 0
comments: 0
---

# 2275. 按位与结果大于零的最长组合

> **[yiduobo的每日leetcode 2275.按位与结果大于零的最长组合](https://zhuanlan.zhihu.com/p/550748088) · 知乎 · 2022-08-07 · 赞同 0**
> 力扣：[2275. 按位与结果大于零的最长组合](https://leetcode.cn/problems/largest-combination-with-bitwise-and-greater-than-zero/) · Medium · 灵茶山艾府：[统计 1 的个数（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2275.按位与结果大于零的最长组合

[力扣](https://leetcode.cn/problems/largest-combination-with-bitwise-and-greater-than-zero/)

如果想要按位与之后的结果大于零，那么必须有至少一个二进制位，满足所有参与与运算的数在这一位上都等于1。题目要找的是最长的组合，实际上就是要找出一个二进制位，使得在这一位上等于1的数最多，于是可以遍历每个数，然后将这些数一位一位拆开，使用哈希表统计每一个二进制位上等于1的数的数目，其中的最大值就是最终答案了。

最后附上python代码：

```python
class Solution(object):
    def largestCombination(self, candidates):
        """
        :type candidates: List[int]
        :rtype: int
        """
        
        pow2 = [1]
        for index in range(1, 24):
            pow2.append(pow2[-1] + pow2[-1])

        cnt = [0] * 24
        for num in candidates:
            for index, p in enumerate(pow2):
                if num & p:
                    num ^= p
                    cnt[index] += 1

        return max(cnt)
```
