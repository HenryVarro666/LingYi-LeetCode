---
title: "136. 只出现一次的数字"
aliases: ["yiduobo的每日leetcode 136.只出现一次的数字"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation", "题单/位运算", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/位运算/九-其他", "题单/LeetCode-热题-100/技巧", "题单/面试经典-150-题/位运算"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/141645616"
zhihu_id: "141645616"
zhihu_title: "yiduobo的每日leetcode 136.只出现一次的数字"
question_id: "136"
question: "只出现一次的数字"
problem_url: "https://leetcode.cn/problems/single-number/"
difficulty: "Easy"
created: "2020-05-17T23:09:35+08:00"
updated: "2020-05-17T23:09:35+08:00"
upvotes: 0
comments: 0
---

# 136. 只出现一次的数字

> **[yiduobo的每日leetcode 136.只出现一次的数字](https://zhuanlan.zhihu.com/p/141645616) · 知乎 · 2020-05-17 · 赞同 0**
> 力扣：[136. 只出现一次的数字](https://leetcode.cn/problems/single-number/) · Easy · 灵茶山艾府：[O(n) 一次遍历，附相似题目（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

136.只出现一次的数字<https://leetcode-cn.com/problems/single-number/>

利用到异或运算的性质，x异或0等于x，且x异或x等于0。

于是可以将所有数全部异或起来，出现两次数因为异或了自身于是变成了0，最后就剩下那个只出现一次的数了。

最后附上python代码：

```
class Solution(object):
    def singleNumber(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        res = 0
        for num in nums:
            res ^= num

        return res
```
