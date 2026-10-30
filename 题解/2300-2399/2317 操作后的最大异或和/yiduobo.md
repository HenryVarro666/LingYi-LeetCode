---
title: "2317. 操作后的最大异或和"
aliases: ["yiduobo的每日leetcode 2317.操作后的最大异或和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "题单/位运算", "题单/位运算/二-异或-XOR-的性质"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/556694377"
zhihu_id: "556694377"
zhihu_title: "yiduobo的每日leetcode 2317.操作后的最大异或和"
question_id: "2317"
question: "操作后的最大异或和"
problem_url: "https://leetcode.cn/problems/maximum-xor-after-operations/"
difficulty: "Medium"
rating: 1679
created: "2022-08-22T23:46:44+08:00"
updated: "2022-08-22T23:46:44+08:00"
upvotes: 0
comments: 0
---

# 2317. 操作后的最大异或和

> **[yiduobo的每日leetcode 2317.操作后的最大异或和](https://zhuanlan.zhihu.com/p/556694377) · 知乎 · 2022-08-22 · 赞同 0**
> 力扣：[2317. 操作后的最大异或和](https://leetcode.cn/problems/maximum-xor-after-operations/) · Medium · 灵茶山艾府：[一步步提示如何做出此题（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2317.操作后的最大异或和

[力扣](https://leetcode.cn/problems/maximum-xor-after-operations/)

首先观察题目中给出的操作

nums[i] \= nums[i] & (nums[i] ^ x)

这是一个&操作，也就是说只对nums[i]中值为1的位生效，值为0的位在操作后依然为0。同时这里的x可以任取，那么对于某一位，如果nums[i]和x在这一位上都为1，那么二者的异或结果在这一位上就为0，在操作后nums[i]在这一位上也将会变成0。

也就是说，这个操作可以选择让num[i]中任意位上的1变为0，次数不限。

由于题目最终要求的是nums中所有的数异或值最大，那么最理想的情况就是对于每个二进制位，如果nums中所有数在这一位上都为0，那么最终答案的这一位只能是0，否则就可以通过上面的操作将这一位上的1的数量减小到只剩下一个，从而保证最终答案的这一位为1，总结起来就是，对于某一位，如果该位上有1，那么最终答案的这一位就是1，否则就是0，实际上就相当于将nums中的所有数或起来。

最后附上python代码：

```python
class Solution(object):
    def maximumXOR(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        res = 0
        for num in nums:
            res |= num
        
        return res
```
