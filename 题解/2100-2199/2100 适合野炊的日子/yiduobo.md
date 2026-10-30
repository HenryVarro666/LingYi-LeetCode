---
title: "2100. 适合打劫银行的日子"
aliases: ["yiduobo的每日leetcode 2100.适合打劫银行的日子"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/array", "leetcode/dynamic-programming", "leetcode/di-tui", "题单/动态规划", "题单/动态规划/专题-前后缀分解"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/521424851"
zhihu_id: "521424851"
zhihu_title: "yiduobo的每日leetcode 2100.适合打劫银行的日子"
question_id: "2100"
question: "适合野炊的日子"
problem_url: "https://leetcode.cn/problems/find-good-days-to-rob-the-bank/"
difficulty: "Medium"
rating: 1702
created: "2022-05-28T23:31:06+08:00"
updated: "2022-05-28T23:31:06+08:00"
upvotes: 0
comments: 0
---

# 2100. 适合打劫银行的日子

> **[yiduobo的每日leetcode 2100.适合打劫银行的日子](https://zhuanlan.zhihu.com/p/521424851) · 知乎 · 2022-05-28 · 赞同 0**
> 力扣：[2100. 适合野炊的日子](https://leetcode.cn/problems/find-good-days-to-rob-the-bank/) · Medium · 灵茶山艾府：[两次遍历 + 前后缀分解](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2100.适合打劫银行的日子

[力扣](https://leetcode.cn/problems/find-good-days-to-rob-the-bank/)

题目要求找出所有的山谷，要求山谷两侧下降的长度都大于等于time，那么一个自然的想法就是枚举所有山谷的位置，然后判断以该位置结尾的递减子串以及以该位置开头的递增子串的长度是否都大于等于time。

对于这个问题，则可以预处理出以每个位置结尾的递减子串的最大长度以及以每个位置开头的递增子串的最大长度。令left[index]表示以security[index]结尾的最长递减子序列的长度，那么对于left[index]，若security[index - 1]大于等于security[index]，那么就有left[index] \= left[index - 1] + 1，否则left[index] \= 0。类似的，令right[index]表示以security[index]开头的最长递增子序列的长度，反向一趟遍历求解即可。

最后附上python代码：

```python
class Solution(object):
    def goodDaysToRobBank(self, security, time):
        """
        :type security: List[int]
        :type time: int
        :rtype: List[int]
        """

        n = len(security)
        left = [0] * n
        for index in range(1, n):
            if security[index - 1] >= security[index]:
                left[index] = left[index - 1] + 1

        right = [0] * n
        for index in range(n - 2, -1, -1):
            if security[index + 1] >= security[index]:
                right[index] = right[index + 1] + 1

        res = []
        for index in range(n):
            if left[index] >= time and right[index] >= time:
                res.append(index)
        
        return res
```
