---
title: "3897. 连接二进制片段得到的最大值"
aliases: ["yiduobo的每日leetcode 3897.连接二进制片段得到的最大值"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2027892003245958258"
zhihu_id: "2027892003245958258"
zhihu_title: "yiduobo的每日leetcode 3897.连接二进制片段得到的最大值"
question_id: "3897"
question: "连接二进制片段得到的最大值"
problem_url: "https://leetcode.cn/problems/maximum-value-of-concatenated-binary-segments/"
difficulty: "Hard"
rating: 1998
created: "2026-04-15T23:51:11+08:00"
updated: "2026-04-15T23:51:16+08:00"
upvotes: 1
comments: 0
---

# 3897. 连接二进制片段得到的最大值

> **[yiduobo的每日leetcode 3897.连接二进制片段得到的最大值](https://zhuanlan.zhihu.com/p/2027892003245958258) · 知乎 · 2026-04-15 · 赞同 1**
> 力扣：[3897. 连接二进制片段得到的最大值](https://leetcode.cn/problems/maximum-value-of-concatenated-binary-segments/) · Hard · 灵茶山艾府：[做法同 179 题（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3897.连接二进制片段得到的最大值

<https://leetcode.cn/problems/maximum-value-of-concatenated-binary-segments/>

题目给出两个大小为n的整数数组num1和nums0，其中nums1[index]表示index这个片段中1的数量，而nums0[index]则表示index这个片段中0的数量。这里的n不超过10^5。

对于第index个片段，其由nums1[index]个1，后面跟着nums0[index]个0组成。

现在可以将这n个片段重新排序，然后将排序后的片段连接起来，形成一个二进制数。问可能得到的最大二进制数是多少。答案需要对10^9 + 7取模。

题目保证所有的nums1和nums0中所有元素之和不超过2 \* 10^5。

题目保证了num1和num0中所有元素之和不超过2 \* 10^5，那么就意味着最终构造出来的二进制数的位数不超过2 \* 10^5，因此可以想办法先把这个数构造出来，然后再计算其十进制的值并取模。

在构造层面，需要解决的问题就是如何重新排布这些片段，才能使得最终结果最大。

首先可以明确的是，全1构成的片段显然是应该尽量排到高位上的，于是可以先进行一趟遍历，将所有nums0[index]为0的片段取出来，将对应的nums1[index]数量的1先添加到最终的二进制数中。

接下来对于剩下的片段，则可以通过排序来确定先后顺序。具体来说，对于两个片段p和q，若二者相同，那么就没有排序的必要，否则的话二者的对应的nums1[p]、nums1[q]以及nums0[p]、nums0[q]可能呈现以下几种关系：

- nums1[p] > nums1[q]
- nums1[p] \< nums1[q]
- nums1[p] \= nums1[q]，同时nums0[p] > nums0[q]
- nums1[p] \= nums1[q]，同时nums0[p] \< nums0[q]

由于题目中的片段都是1在前0在后，因此对于p和q这两个片段，无论是p-q还是q-p，拼接出来的二进制数长度是相同的，因此在这里就应该让高位上有尽量多的1。基于这一点，对于前两种情况，就应该让1更多的那个片段排到前面。另一方面，对于后两种情况，第一段1的数量是相同的，此时就应该让中间这一段0的数量尽量的少，这样一来，才能让第二段1尽量靠前，例如110和1100，应该构造1101100而不是1100110，因为前者中间的0较少，可以让后面第二段1更靠前。

综合上面的结论，可以发现对于非全1的片段，应该按照1的数量倒序为第一关键字，0的数量正序为第二关键字进行排序。

排序后，按照顺序将对应数量的0和1填充到最终的二进制数组中，接下来只需初始化答案为0，然后从前往后一趟遍历，不停得将答案乘以2然后加上当前位上的值即可。过程中如果答案大于等于10^9 + 7，就将其减去10^9 + 7。这样做的理由是对于一个k位二进制数，其转化为十进制的结果为

2^(k - 1) \* a[0] + 2^(k - 2) \* a[1] + ... + 2^0 \* a[k - 1]

合并前两项，就是

2^(k - 2) \* (2 \* a[0] + a[1])

然后再把第三项合并进来，就是

2^(k - 3) \* (2 \* (2 \* a[0] + a[1]) + a[2])

以此类推，最终得到的就是

2 \* (2 \* (... 2 \* (2 \* (2 \* a[0]) + a[1]) + a[2]) ... ) + a[k - 2]) + a[k - 1]

也就是从最高位开始，不断乘以2，再加上当前位上的值

最后附上python代码：

```python
class Solution(object):
    def maxValue(self, nums1, nums0):
        """
        :type nums1: List[int]
        :type nums0: List[int]
        :rtype: int
        """
        
        other = []
        final = []
        for v1, v0 in zip(nums1, nums0):
            if v0 == 0:
                final.extend([1] * v1)
            else:
                other.append((v1, v0))
        
        other.sort(key=lambda d:(-d[0], d[1]))
        for v1, v0 in other:
            final.extend([1] * v1)
            final.extend([0] * v0)
        
        res = 0
        mod = 10 ** 9 + 7
        for v in final:
            res = res + res + v
            if res >= mod:
                res -= mod
        
        return res
```
