---
title: "1874. 两个数组的最小乘积和"
aliases: ["yiduobo的每日leetcode 1874.两个数组的最小乘积和"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/622709317"
zhihu_id: "622709317"
zhihu_title: "yiduobo的每日leetcode 1874.两个数组的最小乘积和"
question_id: "1874"
question: "两个数组的最小乘积和"
problem_url: "https://leetcode.cn/problems/minimize-product-sum-of-two-arrays/"
created: "2023-04-18T01:12:05+08:00"
updated: "2023-04-18T01:12:05+08:00"
upvotes: 0
comments: 0
---

# 1874. 两个数组的最小乘积和

> **[yiduobo的每日leetcode 1874.两个数组的最小乘积和](https://zhuanlan.zhihu.com/p/622709317) · 知乎 · 2023-04-18 · 赞同 0**
> 力扣：[1874. 两个数组的最小乘积和](https://leetcode.cn/problems/minimize-product-sum-of-two-arrays/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1874.两个数组的最小乘积和

[力扣](https://leetcode.cn/problems/minimize-product-sum-of-two-arrays/)

对于nums1中的任意两个数a、b以及nums2中的任意两个数c、d，不妨设a \<\= b，c\<\= d，在这里讨论两种乘法组合a \* c + b \* d以及a \* d + b \* c：

令b \= a + m，d \= c + n，于是有

a \* c + b \* d \= a \* c + (a + m) \* (c + n) \= 2ac + an + cm + mn

a \* d + b \* c \= a \* (c + n) + (a + m) \* c \= 2ac + an + cm

很明显，a \* c + b \* d >\= a \* d + b \* c

为了使得最终结果最小，那么就应该让两个数组中的数按大小反向匹配，于是只需将nums1正序排序，nums2逆序排序，然后一趟遍历计算乘积后累加即可。

最后附上python代码：

```python
class Solution(object):
    def minProductSum(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: int
        """

        nums1.sort()
        nums2.sort(reverse=True)

        return sum([nums1[index] * nums2[index] for index in range(len(nums1))])
```
