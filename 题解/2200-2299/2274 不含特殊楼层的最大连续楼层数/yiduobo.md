---
title: "2274. 不含特殊楼层的最大连续楼层数"
aliases: ["yiduobo的每日leetcode 2274.不含特殊楼层的最大连续楼层数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/sorting"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/550448947"
zhihu_id: "550448947"
zhihu_title: "yiduobo的每日leetcode 2274.不含特殊楼层的最大连续楼层数"
question_id: "2274"
question: "不含特殊楼层的最大连续楼层数"
problem_url: "https://leetcode.cn/problems/maximum-consecutive-floors-without-special-floors/"
difficulty: "Medium"
created: "2022-08-06T00:58:07+08:00"
updated: "2022-08-06T00:58:07+08:00"
upvotes: 0
comments: 0
---

# 2274. 不含特殊楼层的最大连续楼层数

> **[yiduobo的每日leetcode 2274.不含特殊楼层的最大连续楼层数](https://zhuanlan.zhihu.com/p/550448947) · 知乎 · 2022-08-06 · 赞同 0**
> 力扣：[2274. 不含特殊楼层的最大连续楼层数](https://leetcode.cn/problems/maximum-consecutive-floors-without-special-floors/) · Medium · 灵茶山艾府：[排序，计算相邻元素差的最大值（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2274.不含特殊楼层的最大连续楼层数

[力扣](https://leetcode.cn/problems/maximum-consecutive-floors-without-special-floors/)

首先可以明确的是，最终答案必然属于一下三种情况之一：

1、bottom与最低的特殊楼层之间的连续楼层

2、top与最高的特殊楼层之间的连续楼层

3、两个相邻的特殊楼层之间的连续楼层

于是可以先将所有特殊楼层从小到大进行排序，此时就可以通过排序后的首尾楼层与bottom以及top计算出情况1和情况2中的连续楼层数。接下来一趟遍历，计算两个相邻特殊楼层直接的连续楼层数，并更新最终答案即可。

需要特别注意的是，在计算情况1和情况2时，如果bottom和top自身不是特殊楼层的话，那么就可以将其加入到连续楼层中，而在计算情况3时，两个相邻的特殊楼层都不能加入到连续楼层中，因此在计算情况3时相比计算情况1和情况2时有1层楼的差别。

最后附上python代码：

```python
class Solution(object):
    def maxConsecutive(self, bottom, top, special):
        """
        :type bottom: int
        :type top: int
        :type special: List[int]
        :rtype: int
        """

        sorted_specail = sorted(special)
        res = max(sorted_specail[0] - bottom, top - sorted_specail[-1])
        for index in range(1, len(sorted_specail)):
            res = max(res, sorted_specail[index] - sorted_specail[index - 1] - 1)

        return res
```
