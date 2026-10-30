---
title: "LCP 11. 期望个数统计"
aliases: ["yiduobo的每日leetcode LCP11.期望个数统计"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/571112886"
zhihu_id: "571112886"
zhihu_title: "yiduobo的每日leetcode LCP11.期望个数统计"
question_id: "LCP 11"
question: "期望个数统计"
problem_url: "https://leetcode.cn/problems/qi-wang-ge-shu-tong-ji/"
created: "2022-10-07T02:53:55+08:00"
updated: "2022-10-07T02:53:55+08:00"
upvotes: 0
comments: 0
---

# LCP 11. 期望个数统计

> **[yiduobo的每日leetcode LCP11.期望个数统计](https://zhuanlan.zhihu.com/p/571112886) · 知乎 · 2022-10-07 · 赞同 0**
> 力扣：[LCP 11. 期望个数统计](https://leetcode.cn/problems/qi-wang-ge-shu-tong-ji/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP11.期望个数统计

[力扣](https://leetcode.cn/problems/qi-wang-ge-shu-tong-ji/)

题目的数据规模非常大，但是理清楚逻辑之后会发现还是很简单的。

由于只有相同的能力值将打乱简历的顺序，那么就可以将简历按相同能力值分开，各算各的，最后再把期望加起来。

对于相同能力值的简历，不妨设当前考虑的简历有n份，那么就相当于随机给出一个1到n的排列，问这个排列中每个数字落在对应下标位置上的期望是多少。在这里可以再次将期望拆开，变成这n个数字落在各自位置上的期望之和。由于每个数字落在对应下标上的概率都是1/n，那么期望也就是1/n，而n个1/n之和恰好为1。换言之，无论目前这一种能力值的简历的数量n是多少，最终得到的期望都是1。

于是只需要一趟遍历，使用集合统计不同能力值的数量即可。

最后附上python代码：

```python
class Solution(object):
    def expectNumber(self, scores):
        """
        :type scores: List[int]
        :rtype: int
        """

        return len(set(scores))
```
