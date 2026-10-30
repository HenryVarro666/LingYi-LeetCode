---
title: "2216. 美化数组的最少删除数"
aliases: ["yiduobo的每日leetcode 2216.美化数组的最少删除数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/stack", "leetcode/array", "题单/常用数据结构", "题单/常用数据结构/三-栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/541229628"
zhihu_id: "541229628"
zhihu_title: "yiduobo的每日leetcode 2216.美化数组的最少删除数"
question_id: "2216"
question: "美化数组的最少删除数"
problem_url: "https://leetcode.cn/problems/minimum-deletions-to-make-array-beautiful/"
difficulty: "Medium"
rating: 1510
created: "2022-07-13T19:10:54+08:00"
updated: "2022-07-13T19:10:54+08:00"
upvotes: 0
comments: 0
---

# 2216. 美化数组的最少删除数

> **[yiduobo的每日leetcode 2216.美化数组的最少删除数](https://zhuanlan.zhihu.com/p/541229628) · 知乎 · 2022-07-13 · 赞同 0**
> 力扣：[2216. 美化数组的最少删除数](https://leetcode.cn/problems/minimum-deletions-to-make-array-beautiful/) · Medium · 灵茶山艾府：[栈思想模拟 + O(1) 额外空间](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2216.美化数组的最少删除数

[力扣](https://leetcode.cn/problems/minimum-deletions-to-make-array-beautiful/)

贪心法的题目，最直观的想法就是一趟遍历，如果遇到了相同的数那么就删去其中一个。一个不严谨的证明是遇到相同的数如果保留一个，那么会影响到后面所有数下标的奇偶性，而对于后面的数而言，可以随时删去一个数让奇偶性反转过来，也就是相比直接删去两个数，保留其中一个的可选择性更多。

最后附上python代码：

```python
class Solution(object):
    def minDeletion(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        first = None
        res = len(nums)
        for num in nums:
            if first is None:
                first = num
            elif first == num:
                continue
            else:
                res -= 2
                first = None
        
        return res
```
