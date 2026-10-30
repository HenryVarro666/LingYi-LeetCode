---
title: "3131. 找出与数组相加的整数"
aliases: ["yiduobo的每日leetcode 3131.找出与数组相加的整数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/702303069"
zhihu_id: "702303069"
zhihu_title: "yiduobo的每日leetcode 3131.找出与数组相加的整数"
question_id: "3131"
question: "找出与数组相加的整数 I"
problem_url: "https://leetcode.cn/problems/find-the-integer-added-to-array-i/"
difficulty: "Easy"
created: "2024-06-08T00:21:05+08:00"
updated: "2024-06-08T00:21:05+08:00"
upvotes: 0
comments: 0
---

# 3131. 找出与数组相加的整数

> **[yiduobo的每日leetcode 3131.找出与数组相加的整数](https://zhuanlan.zhihu.com/p/702303069) · 知乎 · 2024-06-08 · 赞同 0**
> 力扣：[3131. 找出与数组相加的整数 I](https://leetcode.cn/problems/find-the-integer-added-to-array-i/) · Easy · 灵茶山艾府：[最小值之差（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3131.找出与数组相加的整数

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-integer-added-to-array-i/description/)

题目给出两个数组nums1和nums2，要求找出一个整数x，使得nums1中的所有元素加上x后，每种元素出现的次数都与nums2相同。

很明显，在这里nums1中的最小值加上x后就应该变成nums2中的最小值，nums1中的次小值加上x后就应该变成nums2中的次小值，以此类推，因此答案就是nums2中的最小值减去nums1中的最小值。

证明也很简单，不妨设nums1[a] \< nums1[b]，nums2[c] \< nums2[d]，那么就有

nums2[c] - nums1[b] \< nums2[d] - nums1[b] \< nums2[d] - nums1[a]

即将nums1[b]变为nums2[c]所需的x小于将nums1[a]变为nums2[d]所需的x，这也就意味着变换时不能打乱顺序

最后附上python代码：

```python
class Solution(object):
    def addedInteger(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: int
        """

        return min(nums2) - min(nums1)
```
