---
title: "795. 区间子数组个数"
aliases: ["yiduobo的每日leetcode 795.区间子数组个数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bian-li", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/五-三指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/342122854"
zhihu_id: "342122854"
zhihu_title: "yiduobo的每日leetcode 795.区间子数组个数"
question_id: "795"
question: "区间子数组个数"
problem_url: "https://leetcode.cn/problems/number-of-subarrays-with-bounded-maximum/"
difficulty: "Medium"
rating: 1817
created: "2021-01-05T21:18:16+08:00"
updated: "2021-01-05T21:18:16+08:00"
upvotes: 1
comments: 0
---

# 795. 区间子数组个数

> **[yiduobo的每日leetcode 795.区间子数组个数](https://zhuanlan.zhihu.com/p/342122854) · 知乎 · 2021-01-05 · 赞同 1**
> 力扣：[795. 区间子数组个数](https://leetcode.cn/problems/number-of-subarrays-with-bounded-maximum/) · Medium · 灵茶山艾府：[【图解】一次遍历+简洁写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

795.区间子数组个数

[力扣](https://leetcode-cn.com/problems/number-of-subarrays-with-bounded-maximum/)

对于这类区间相关的问题，一般有两种做法。第一种是通过某种数据数据结构动态维护区间的某些信息，然后动态求解一个区间内的某个问题。第二种则是固定住区间的某一端，然后通过某种性质，通常是单调性来移动另一端，求解两个端点之内区间的某个问题。

对于这个问题，我采用的是固定住区间的起点start_pos，然后尝试将区间向右扩展。当然，这里不需要什么单调性之类的东西，只需要简单的判断。

从左往右一趟扫描，对于当前节点now，设其在数组中的下标为index：

1、若now大于R，那么说明该节点无论如何都不可能加入到答案中，且以start_pos为起点的区间也没有可能再往右扩展了，因此此时将start_pos置为空。

2、若now小于等于R：

2-1）若此时start_pos为空，那么将index标记为区间左端点。因为对于某个节点，即使其值小于L，该节点也可能通过后续节点的带动成为合法的答案。

2-2）若now大于等于L，那么该节点为当前区间最右侧的大于等于L的节点，此时需要通过一个变量last_pos记录index。

接下来，若当前的last_pos不为空，那么对于下列区间

[start_pos, start_pos + 1, ..., last_pos, last_pos + 1, ... index]

[start_pos + 1, ..., last_pos, last_pos + 1, ... index]

[start_pos + 2, ..., last_pos, last_pos + 1, ... index]

...

[last_pos - 1, last_pos, last_pos + 1, ... index]

其中last_pos位置上的数是大于等于L的，且区间中的所有数都小于等于R。而对于last_pos + 1到index之间的所有数，通过2-2可知这里所有的数都是小于L的，因此不能独立形成答案。

因此，以index为右端点的合法区间一共就有last_pos - start_pos + 1个。

处理完成index之后，继续向右扫描直到处理完所有节点即可。

最后附上python代码：

```python
class Solution(object):
    def numSubarrayBoundedMax(self, A, L, R):
        """
        :type A: List[int]
        :type L: int
        :type R: int
        :rtype: int
        """

        res = 0
        start_pos = None
        last_pos = None
        for index, now in enumerate(A):
            if now > R:
                start_pos = None
                last_pos = None
            else:
                if start_pos is None:
                    start_pos = index
                if now >= L:
                    last_pos = index
                if last_pos is not None:
                    res += last_pos - start_pos + 1

        return res
```
