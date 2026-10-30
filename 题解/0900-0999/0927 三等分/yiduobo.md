---
title: "927. 三等分"
aliases: ["yiduobo的每日leetcode 927.三等分"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/356684234"
zhihu_id: "356684234"
zhihu_title: "yiduobo的每日leetcode 927.三等分"
question_id: "927"
question: "三等分"
problem_url: "https://leetcode.cn/problems/three-equal-parts/"
created: "2021-03-12T19:07:11+08:00"
updated: "2021-03-12T19:07:11+08:00"
upvotes: 0
comments: 0
---

# 927. 三等分

> **[yiduobo的每日leetcode 927.三等分](https://zhuanlan.zhihu.com/p/356684234) · 知乎 · 2021-03-12 · 赞同 0**
> 力扣：[927. 三等分](https://leetcode.cn/problems/three-equal-parts/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

927.三等分

[力扣](https://leetcode-cn.com/problems/three-equal-parts/)

题目要求分出三个二进制值相等的连续子数组，那么首先可以明确的是，若可以分出来，那么这三个连续子数组中1的数量必然是相等的，且排布也必须是一样的。那么我们可以首先统计出原始数组中1出现的次数s，若s不是3的倍数，那么显然不可分。另外，当s等于0时，说明原数组全都是0，那么[0, 0, 000..000]就是一组可行解。

接下来考察s为3的倍数，且不为0的情况。

首先，可以将s除以3，得到每个连续子数组中1出现的次数n。接下里可以从头到尾进行一趟扫描，根据n将连续子数组中1的部分划分出来，那么划分后的数组就是

[00..000] [l1...r1] [00..000] [l2...r2] [00.. 000] [l3...r3] [00..000]

其中[l1...r1]表示第1个1到第n个1这一段，[l2...r2]表示第n + 1个1到第2n个1这一段，而[l3...r3]表示第2n + 1个1到第3n个1这一段。其他的[00..000]表示可能存在若干个0，这里的若干个也可以是0个。

如果能分出来，那么[l1...r1]、[l2...r2]、[l3...r3]这三段必须要完全一致，否则说明不可分。若这三段完全一致，则还需要考虑多出的0的分配。

显然，[l1...r1]之前的0必须分配给第一段，但由于是前缀0，因此不影响最终的大小。但是相对的，[l3...r3]后面的0必须分配个第三段，这里的0是后缀0，因此对于[l1...r1]以及[l2...r2]来说，也需要同样数量的0才能保持大小一致。

此时就只需要考察[l1...r1]到[l2...r2]之间0的个数以及[l2...r2]到[l3...r3]之间0的个数是否大于等于[l3...r3]后面0的个数。若数量不够，那么就说明不可分，否则就给[l1...r1]以及[l2...r2]分配与[l3...r3]后面同等数量的0，而剩下的0都则归为[l2...r2]以及[l3...r3]的前缀0即可。

简单举个例子，对于000110000011000011000这个数组而言，首先可知其中有6个1，那么每一组应该是2个1，因此首先根据1的个数将数组划分为

[000][11][00000][11][0000][11][000]

接下来对于第三部分，其后面还有3个0，那么对于第1和第2部分之间的5个0，需要分配3个0给第1部分作为后缀，而对于第2和第3部分之间的4个0，同样需要分配3个0给第2部分作为后缀，那么就可以得出最终的划分方案

[00011000] [0011000] [011000]

最后附上python代码：

```python
class Solution(object):
    def threeEqualParts(self, arr):
        """
        :type arr: List[int]
        :rtype: List[int]
        """

        s = sum(arr)
        if s % 3 != 0:
            return [-1, -1]
        s /= 3
        if s == 0:
            return [0, 2]

        l1 = 0
        while arr[l1] != 1:
            l1 += 1
        now = 1
        r1 = l1
        while now < s:
            r1 += 1
            now += arr[r1]
        
        l2 = r1 + 1
        while arr[l2] != 1:
            l2 += 1
        now = 1
        r2 = l2
        while now < s:
            r2 += 1
            now += arr[r2]
        
        l3 = r2 + 1
        while arr[l3] != 1:
            l3 += 1
        r3 = len(arr) - 1
        while arr[r3] == 0:
            r3 -= 1
        
        if r1 - l1 != r2 - l2 or r1 - l1 != r3 - l3:
            return [-1, -1]
        
        suffix_zero = len(arr) - r3 - 1
        if l3 - 1 - (r2 + 1) + 1 < suffix_zero:
            return [-1, -1]
        if l2 - 1 - (r1 + 1) + 1 < suffix_zero:
            return [-1, -1]

        return [r1 + suffix_zero, r2 + suffix_zero + 1]
```
