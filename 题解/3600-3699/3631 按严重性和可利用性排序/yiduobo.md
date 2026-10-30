---
title: "3631. 按严重性和可利用性排序"
aliases: ["yiduobo的每日leetcode 3631.按严重性和可利用性排序"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1946341536146133058"
zhihu_id: "1946341536146133058"
zhihu_title: "yiduobo的每日leetcode 3631.按严重性和可利用性排序"
question_id: "3631"
question: "按严重性和可利用性排序"
problem_url: "https://leetcode.cn/problems/sort-threats-by-severity-and-exploitability/"
created: "2025-09-03T01:06:04+08:00"
updated: "2025-09-03T01:06:04+08:00"
upvotes: 0
comments: 0
---

# 3631. 按严重性和可利用性排序

> **[yiduobo的每日leetcode 3631.按严重性和可利用性排序](https://zhuanlan.zhihu.com/p/1946341536146133058) · 知乎 · 2025-09-03 · 赞同 0**
> 力扣：[3631. 按严重性和可利用性排序](https://leetcode.cn/problems/sort-threats-by-severity-and-exploitability/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3631.按严重性和可利用性排序

[3631. 按严重性和可利用性排序威胁 - 力扣（LeetCode）](https://leetcode.cn/problems/sort-threats-by-severity-and-exploitability/description/)

题目给出一个二维数组threats，其中threats\[index\] \= \[id\[index\], sev\[index\], exp\[index\]\]，表示第index个威胁，其严重程度为sev\[index\]，可利用性为exp\[index\]。定义威胁index的分数为score \= 2 \* sev\[index\] + exp\[index\]，要求按照分数降序返回threats。

直接按照题目要求计算每个威胁的分数，然后以分数为第一关键字倒序，下标为第二关键字正序，排序原数组的下标就行了。

最后附上python代码：

```python
class Solution(object):
    def sortThreats(self, threats):
        """
        :type threats: List[List[int]]
        :rtype: List[List[int]]
        """
        
        return sorted(threats, key=lambda d:(-(d[1] * 2 + d[2]), d[0]))
```
