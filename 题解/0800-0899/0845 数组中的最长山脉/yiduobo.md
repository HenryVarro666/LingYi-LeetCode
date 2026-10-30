---
title: "845. 数组中的最长山脉"
aliases: ["yiduobo的每日leetcode 845.数组中的最长山脉"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/347748115"
zhihu_id: "347748115"
zhihu_title: "yiduobo的每日leetcode 845.数组中的最长山脉"
question_id: "845"
question: "数组中的最长山脉"
problem_url: "https://leetcode.cn/problems/longest-mountain-in-array/"
created: "2021-01-29T22:56:38+08:00"
updated: "2021-01-29T22:56:38+08:00"
upvotes: 0
comments: 0
---

# 845. 数组中的最长山脉

> **[yiduobo的每日leetcode 845.数组中的最长山脉](https://zhuanlan.zhihu.com/p/347748115) · 知乎 · 2021-01-29 · 赞同 0**
> 力扣：[845. 数组中的最长山脉](https://leetcode.cn/problems/longest-mountain-in-array/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

845.数组中的最长山脉

[力扣](https://leetcode-cn.com/problems/longest-mountain-in-array/)

对于一个山脉，是由B[0]到B[i]这一段单调递增的连续子数组以及B[i]到B[B.length - 1]这一段单调递减的连续子数组构成的，那么我们可以优先预处理出left和right两个数组，其中left[index]表示以arr[index]为终点的单调递增子数组的长度，而right[index]则表示以arr[index]为起点的单调递减子数组的长度，这两个数组可以通过正反两趟扫描求得。

求解出left以及right之后，枚举每个index，若当前left[index]以及right[index]大于1，那么才会存在以arr[index]为中心的山脉，此时使用left[index] + right[index] - 1更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def longestMountain(self, arr):
        """
        :type arr: List[int]
        :rtype: int
        """

        if len(arr) < 3:
            return 0
        
        left = [1]
        for index in range(1, len(arr)):
            if arr[index] > arr[index - 1]:
                left.append(left[-1] + 1)
            else:
                left.append(1)
        
        right = [1]
        for index in range(len(arr) - 2, -1, -1):
            if arr[index] > arr[index + 1]:
                right.append(right[-1] + 1)
            else:
                right.append(1)
        right.reverse()

        res = 0
        for index in range(len(arr)):
            if left[index] > 1 and right[index] > 1:
                res = max(res, left[index] + right[index] - 1)
        
        return res
```
