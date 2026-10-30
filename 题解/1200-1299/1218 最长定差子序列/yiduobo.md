---
title: "1218. 最长定差子序列"
aliases: ["yiduobo的每日leetcode 1218.最长定差子序列"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/382749399"
zhihu_id: "382749399"
zhihu_title: "yiduobo的每日leetcode 1218.最长定差子序列"
question_id: "1218"
question: "最长定差子序列"
problem_url: "https://leetcode.cn/problems/longest-arithmetic-subsequence-of-given-difference/"
created: "2021-06-21T23:51:03+08:00"
updated: "2021-06-21T23:51:03+08:00"
upvotes: 0
comments: 0
---

# 1218. 最长定差子序列

> **[yiduobo的每日leetcode 1218.最长定差子序列](https://zhuanlan.zhihu.com/p/382749399) · 知乎 · 2021-06-21 · 赞同 0**
> 力扣：[1218. 最长定差子序列](https://leetcode.cn/problems/longest-arithmetic-subsequence-of-given-difference/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1218.最长定差子序列

[力扣](https://leetcode-cn.com/problems/longest-arithmetic-subsequence-of-given-difference/)

经典的动态规划问题。令f[i][j]表示前i个数中，以j为结尾时最长定差子序列的长度，那么对于f[i][j]而言，其上一位必然是f[i - 1][j - diff]。由于这里每一轮的结果都是从上一轮得来的，因此可以省去一维。另外对于前i个数而言，最多也就只有i个备选答案，因此可以使用dict来进行动态规划。

最后附上python代码：

```python
class Solution(object):
    def longestSubsequence(self, arr, difference):
        """
        :type arr: List[int]
        :type difference: int
        :rtype: int
        """

        f = {}
        for num in arr:
            pre = num - difference
            now = f.get(pre, 0) + 1
            f[num] = now
        
        return max(f.values())
```
