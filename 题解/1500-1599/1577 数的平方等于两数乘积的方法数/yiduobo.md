---
title: "1577. 数的平方等于两数乘积的方法数"
aliases: ["yiduobo的每日leetcode 1577.数的平方等于两数乘积的方法数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/430010084"
zhihu_id: "430010084"
zhihu_title: "yiduobo的每日leetcode 1577.数的平方等于两数乘积的方法数"
question_id: "1577"
question: "数的平方等于两数乘积的方法数"
problem_url: "https://leetcode.cn/problems/number-of-ways-where-square-of-number-is-equal-to-product-of-two-numbers/"
created: "2021-11-05T22:49:30+08:00"
updated: "2021-11-05T22:49:30+08:00"
upvotes: 0
comments: 0
---

# 1577. 数的平方等于两数乘积的方法数

> **[yiduobo的每日leetcode 1577.数的平方等于两数乘积的方法数](https://zhuanlan.zhihu.com/p/430010084) · 知乎 · 2021-11-05 · 赞同 0**
> 力扣：[1577. 数的平方等于两数乘积的方法数](https://leetcode.cn/problems/number-of-ways-where-square-of-number-is-equal-to-product-of-two-numbers/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1577.数的平方等于两数乘积的方法数

[力扣](https://leetcode-cn.com/problems/number-of-ways-where-square-of-number-is-equal-to-product-of-two-numbers/)

注意到题目中nums1和nums2的规模都很小，因此可以直接暴力枚举。

对于类型1，可以直接枚举nums2[j]以及nums2[k]，计算二者的乘积并统计起来，然后枚举nums1[i]，并使用nums2[i]的平方的出现次数来更新答案。

对于类型2也是同样的做法，直接枚举nums1[j]以及nums1[k]，计算二者的乘积并统计起来，然后枚举nums2[i]，并使用nums2[i]的平方的出现次数来更新答案。

最后附上python代码：

```python
class Solution(object):
    def numTriplets(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: int
        """

        m = len(nums1)
        n = len(nums2)
        res = 0

        count_dict = {}
        for i in range(m - 1):
            for j in range(i + 1, m):
                tmp = nums1[i] * nums1[j]
                count_dict[tmp] = count_dict.get(tmp, 0) + 1
        for num in nums2:
            res += count_dict.get(num * num, 0)
        
        count_dict = {}
        for i in range(n - 1):
            for j in range(i + 1, n):
                tmp = nums2[i] * nums2[j]
                count_dict[tmp] = count_dict.get(tmp, 0) + 1
        for num in nums1:
            res += count_dict.get(num * num, 0)
        
        return res
```
