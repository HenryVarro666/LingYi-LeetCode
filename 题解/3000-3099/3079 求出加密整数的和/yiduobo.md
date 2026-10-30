---
title: "3079. 求出加密整数的和"
aliases: ["yiduobo的每日leetcode 3079.求出加密整数的和"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/698215816"
zhihu_id: "698215816"
zhihu_title: "yiduobo的每日leetcode 3079.求出加密整数的和"
question_id: "3079"
question: "求出加密整数的和"
problem_url: "https://leetcode.cn/problems/find-the-sum-of-encrypted-integers/"
difficulty: "Easy"
created: "2024-05-17T00:08:11+08:00"
updated: "2024-05-17T00:08:11+08:00"
upvotes: 0
comments: 0
---

# 3079. 求出加密整数的和

> **[yiduobo的每日leetcode 3079.求出加密整数的和](https://zhuanlan.zhihu.com/p/698215816) · 知乎 · 2024-05-17 · 赞同 0**
> 力扣：[3079. 求出加密整数的和](https://leetcode.cn/problems/find-the-sum-of-encrypted-integers/) · Easy · 灵茶山艾府：[不用字符串的 O(1) 空间写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3079.求出加密整数的和

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-sum-of-encrypted-integers/description/)

一趟遍历，对于当前遍历到的数字v，分离出其各位数字同时记录其中的最大值，同时更新基数111..111，这个基数的位数取决于分离数字的轮次。分离完毕后，使用这个基数乘以分离出来的最大值就得到了加密后的整数，将其累加到答案中即可。

最后附上python代码：

```python
class Solution(object):
    def sumOfEncryptedInt(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        res = 0
        for v in nums:
            mul = 1
            ma = 0
            while True:
                ma = max(ma, v % 10)
                v /= 10
                if v == 0:
                    break
                mul = mul * 10 + 1
            
            res += mul * ma
        
        return res
```
