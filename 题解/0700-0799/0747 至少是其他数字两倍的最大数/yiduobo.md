---
title: "747. 至少是其他数字两倍的最大数"
aliases: ["yiduobo的每日leetcode 747.至少是其他数字两倍的最大数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/337736563"
zhihu_id: "337736563"
zhihu_title: "yiduobo的每日leetcode 747.至少是其他数字两倍的最大数"
question_id: "747"
question: "至少是其他数字两倍的最大数"
problem_url: "https://leetcode.cn/problems/largest-number-at-least-twice-of-others/"
created: "2020-12-17T22:59:21+08:00"
updated: "2020-12-17T22:59:21+08:00"
upvotes: 0
comments: 0
---

# 747. 至少是其他数字两倍的最大数

> **[yiduobo的每日leetcode 747.至少是其他数字两倍的最大数](https://zhuanlan.zhihu.com/p/337736563) · 知乎 · 2020-12-17 · 赞同 0**
> 力扣：[747. 至少是其他数字两倍的最大数](https://leetcode.cn/problems/largest-number-at-least-twice-of-others/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

747.至少是其他数字两倍的最大数

[力扣](https://leetcode-cn.com/problems/largest-number-at-least-twice-of-others/)

题目要求找出数组中的最大数，并判断其是否至少是其他数的两倍，那么我们可以一趟扫描，在找出最大数的同时顺便也找出第二大的数，然后就只需要判断最大数是否至少是第二大数的两倍即可。

最后附上python代码：

```python
class Solution(object):
    def dominantIndex(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        first = second = None
        for index, num in enumerate(nums):
            if first is None:
                first = index
            elif second is None:
                if num > nums[first]:
                    second = first
                    first = index
                else:
                    second = index
            elif num > nums[first]:
                second = first
                first = index
            elif num > nums[second]:
                second = index
        
        if second is None or nums[first] >= nums[second] + nums[second]:
            return first
        
        return -1
```
