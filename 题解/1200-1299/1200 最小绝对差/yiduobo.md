---
title: "1200. 最小绝对差"
aliases: ["yiduobo的每日leetcode 1200.最小绝对差"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/sorting"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/381336779"
zhihu_id: "381336779"
zhihu_title: "yiduobo的每日leetcode 1200.最小绝对差"
question_id: "1200"
question: "最小绝对差"
problem_url: "https://leetcode.cn/problems/minimum-absolute-difference/"
difficulty: "Easy"
created: "2021-06-16T23:45:08+08:00"
updated: "2021-06-16T23:45:08+08:00"
upvotes: 0
comments: 0
---

# 1200. 最小绝对差

> **[yiduobo的每日leetcode 1200.最小绝对差](https://zhuanlan.zhihu.com/p/381336779) · 知乎 · 2021-06-16 · 赞同 0**
> 力扣：[1200. 最小绝对差](https://leetcode.cn/problems/minimum-absolute-difference/) · Easy · 灵茶山艾府：[排序后，只需考虑相邻元素之差（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1200.最小绝对差

[力扣](https://leetcode-cn.com/problems/minimum-absolute-difference/)

题目要求具有最小绝对差的元素对，并按照升序输出，那么我们可以想将数组从小到大进行排序。完成排序后，可以明确的是最小绝对差必然出现在相邻的两个元素之间，因此可以一趟扫描求解最小绝对差以及对应的元素对。

最后附上python代码：

```python
class Solution(object):
    def minimumAbsDifference(self, arr):
        """
        :type arr: List[int]
        :rtype: List[List[int]]
        """

        arr = sorted(arr)
        res = [[arr[0], arr[1]]]
        min_diff = arr[1] - arr[0]
        for index in range(2, len(arr)):
            if arr[index] - arr[index - 1] < min_diff:
                min_diff = arr[index] - arr[index - 1]
                res = [[arr[index - 1], arr[index]]]
            elif arr[index] - arr[index - 1] == min_diff:
                res.append([arr[index - 1], arr[index]])
        
        return res
```
