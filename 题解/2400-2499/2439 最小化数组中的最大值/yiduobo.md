---
title: "2439. 最小化数组中的最大值"
aliases: ["yiduobo的每日leetcode 2439.最小化数组中的最大值"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/binary-search", "题单/二分算法", "题单/二分算法/二-二分答案"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/583795067"
zhihu_id: "583795067"
zhihu_title: "yiduobo的每日leetcode 2439.最小化数组中的最大值"
question_id: "2439"
question: "最小化数组中的最大值"
problem_url: "https://leetcode.cn/problems/minimize-maximum-of-array/"
difficulty: "Medium"
rating: 1965
created: "2022-11-16T02:02:02+08:00"
updated: "2022-11-16T02:02:02+08:00"
upvotes: 1
comments: 0
---

# 2439. 最小化数组中的最大值

> **[yiduobo的每日leetcode 2439.最小化数组中的最大值](https://zhuanlan.zhihu.com/p/583795067) · 知乎 · 2022-11-16 · 赞同 1**
> 力扣：[2439. 最小化数组中的最大值](https://leetcode.cn/problems/minimize-maximum-of-array/) · Medium · 灵茶山艾府：[两种做法：二分答案 / 分类讨论（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2439.最小化数组中的最大值

[力扣](https://leetcode.cn/problems/minimize-maximum-of-array/)

由于题目可以将后面位置上的数值转移到前面的位置上，那么就可以断定，最终结果必然可以通过操作，将最大值转移到nums[0]上。另一方面，如果出现后续数字都比较小的时候，最终结果只会由前缀决定，例如[1, 10, 1]，最终结果可以写成[6, 5, 1]，而此时发挥作用的只有前两个数字。

综合上面两点就可以发现，最终结果必然是某个前缀平均数的向上取整，于是只需一趟遍历，计算所有前缀的平均数向上取整后的结果，然后取其中最大的作为最终答案即可。

最后附上python代码：

```python
class Solution(object):
    def minimizeArrayValue(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        res = 0
        now = 0
        for index, num in enumerate(nums):
            now += num
            avg = now / (index + 1)
            if now % (index + 1) != 0:
                avg += 1
            
            res = max(res, avg)
        
        return res
```
