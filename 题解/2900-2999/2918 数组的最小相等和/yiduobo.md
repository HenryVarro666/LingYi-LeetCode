---
title: "2918. 数组的最小相等和"
aliases: ["yiduobo的每日leetcode 2918.数组的最小相等和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/664999347"
zhihu_id: "664999347"
zhihu_title: "yiduobo的每日leetcode 2918.数组的最小相等和"
question_id: "2918"
question: "数组的最小相等和"
problem_url: "https://leetcode.cn/problems/minimum-equal-sum-of-two-arrays-after-replacing-zeros/"
difficulty: "Medium"
rating: 1526
created: "2023-11-04T04:22:39+08:00"
updated: "2023-11-04T04:22:39+08:00"
upvotes: 0
comments: 0
---

# 2918. 数组的最小相等和

> **[yiduobo的每日leetcode 2918.数组的最小相等和](https://zhuanlan.zhihu.com/p/664999347) · 知乎 · 2023-11-04 · 赞同 0**
> 力扣：[2918. 数组的最小相等和](https://leetcode.cn/problems/minimum-equal-sum-of-two-arrays-after-replacing-zeros/) · Medium · 灵茶山艾府：[分类讨论（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2918.数组的最小相等和

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/minimum-equal-sum-of-two-arrays-after-replacing-zeros/)

题目要求将两个数组中所有的0都替换为正整数，使得两个数组之和相等且最小。由于必须要进行替换，因此可以先分别遍历两个数组，统计其中0的个数x、y以及数组之和s1、s2，那么可能的数组最小和就是s1 + x以及s2 + y，理由是由于必须将0替换成正整数，那么最好情况下也是将0替换成1，因此替换后的数组和就是s1 + x以及s2 + y。

方便起见，将x累加进s1，将y累加进s2。接下来：

1、若s1 \= s2，此时无需进行任何操作，答案就是s1

2、若s1 \< s2，此时应该将s1补足到s2，这里就要求nums1中至少存在一个0。若存在，那么答案就是s2，否则无法使得两个数组和相等，直接返回-1

3、若s1 > s2，与情况2对称，这里要求nums2中至少存在一个0。若存在，那么答案就是s1，否则返回-1

最后附上python代码：

```python
class Solution(object):
    def minSum(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: int
        """

        s1 = s2 = 0
        x = y = 0
        for v in nums1:
            s1 += v
            if v == 0:
                x += 1
        
        for v in nums2:
            s2 += v
            if v == 0:
                y += 1
        
        s1 += x
        s2 += y

        if s1 == s2:
            return s1
        elif s1 > s2:
            if y > 0:
                return s1
            else:
                return -1
        elif x > 0:
            return s2
        else:
            return -1
```
