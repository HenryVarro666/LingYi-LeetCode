---
title: "2917. 找出数组中的K-or值"
aliases: ["yiduobo的每日leetcode 2917.找出数组中的K-or值"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation", "leetcode/bian-li", "题单/位运算", "题单/位运算/一-基础题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/664998924"
zhihu_id: "664998924"
zhihu_title: "yiduobo的每日leetcode 2917.找出数组中的K-or值"
question_id: "2917"
question: "找出数组中的 K-or 值"
problem_url: "https://leetcode.cn/problems/find-the-k-or-of-an-array/"
difficulty: "Easy"
rating: 1389
created: "2023-11-04T04:06:46+08:00"
updated: "2023-11-04T04:06:46+08:00"
upvotes: 0
comments: 0
---

# 2917. 找出数组中的K-or值

> **[yiduobo的每日leetcode 2917.找出数组中的K-or值](https://zhuanlan.zhihu.com/p/664998924) · 知乎 · 2023-11-04 · 赞同 0**
> 力扣：[2917. 找出数组中的 K-or 值](https://leetcode.cn/problems/find-the-k-or-of-an-array/) · Easy · 灵茶山艾府：[统计每个比特位有多少个 1（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2917.找出数组中的K-or值

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/find-the-k-or-of-an-array/)

题目中数值的大小取值范围在2^31之内，因此可以直接枚举所有2的幂次pow2，然后对于当前枚举到的pow2，一趟遍历检测数组中有多少个数在这一位上为1。若存在至少k个数在这一位上为1，就将pow2累加到答案中。重复此过程直到pow2大于数组中的最大值为止。

最后附上python代码：

```python
class Solution(object):
    def findKOr(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        ma = max(nums)
        pow2 = 1
        res = 0
        while pow2 <= ma:
            cnt = 0
            for v in nums:
                if v & pow2 == pow2:
                    cnt += 1
            
            if cnt >= k:
                res += pow2
            
            pow2 += pow2
        
        return res
```
