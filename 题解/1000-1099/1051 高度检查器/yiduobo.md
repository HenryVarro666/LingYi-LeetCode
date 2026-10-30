---
title: "1051. 高度检查器"
aliases: ["yiduobo的每日leetcode 1051.高度检查器"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/371826832"
zhihu_id: "371826832"
zhihu_title: "yiduobo的每日leetcode 1051.高度检查器"
question_id: "1051"
question: "高度检查器"
problem_url: "https://leetcode.cn/problems/height-checker/"
created: "2021-05-12T22:00:55+08:00"
updated: "2021-05-12T22:00:55+08:00"
upvotes: 0
comments: 0
---

# 1051. 高度检查器

> **[yiduobo的每日leetcode 1051.高度检查器](https://zhuanlan.zhihu.com/p/371826832) · 知乎 · 2021-05-12 · 赞同 0**
> 力扣：[1051. 高度检查器](https://leetcode.cn/problems/height-checker/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1051.高度检查器

[力扣](https://leetcode-cn.com/problems/height-checker/)

题目要求最后需要移动多少人，实际上就是要求当前顺序heights与最后有序的sorted_heights之间有多少位置上不同，那么只需要将heights排序得到sorted_heights，然后逐位对比即可。

最后附上python代码：

```python
class Solution(object):
    def heightChecker(self, heights):
        """
        :type heights: List[int]
        :rtype: int
        """

        return sum([1 if x != heights[index] else 0 for index, x in enumerate(sorted(heights))])
```
