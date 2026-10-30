---
title: "3687. 图书馆逾期罚款计算器"
aliases: ["yiduobo的每日leetcode 3687.图书馆逾期罚款计算器"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1955328623356654017"
zhihu_id: "1955328623356654017"
zhihu_title: "yiduobo的每日leetcode 3687.图书馆逾期罚款计算器"
question_id: "3687"
question: "图书馆逾期罚款计算器"
problem_url: "https://leetcode.cn/problems/library-late-fee-calculator/"
created: "2025-09-27T17:54:02+08:00"
updated: "2025-09-27T17:54:02+08:00"
upvotes: 2
comments: 0
---

# 3687. 图书馆逾期罚款计算器

> **[yiduobo的每日leetcode 3687.图书馆逾期罚款计算器](https://zhuanlan.zhihu.com/p/1955328623356654017) · 知乎 · 2025-09-27 · 赞同 2**
> 力扣：[3687. 图书馆逾期罚款计算器](https://leetcode.cn/problems/library-late-fee-calculator/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3687.图书馆逾期罚款计算器

[3687. 图书馆逾期罚款计算器 - 力扣（LeetCode）](https://leetcode.cn/problems/library-late-fee-calculator/description/)

题目给出一个整数数组daysLate，其中daysLate[index]表示第index本书的归还日期完了几天。

对于daysLate[index]：

1、若daysLate[index]为1，罚款金额为1

2、若daysLate[index]在2到5之间，罚款金额为2 \* daysLate[index]

3、若daysLate[index]大于5，罚款金额为3 \* daysLate[index]

问所有数的总罚款为多少。

一趟遍历，按照题目的规则计算每本书的罚款金额，然后累加起来即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def lateFee(self, daysLate):
        """
        :type daysLate: List[int]
        :rtype: int
        """
        
        res = 0
        for d in daysLate:
            if d == 1:
                res += 1
            elif 2 <= d <= 5:
                res += d * 2
            else:
                res += d * 3
        
        return res
```
