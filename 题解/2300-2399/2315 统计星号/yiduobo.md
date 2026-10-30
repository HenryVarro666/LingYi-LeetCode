---
title: "2315. 统计星号"
aliases: ["yiduobo的每日leetcode 2315.统计星号"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/string"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/556202715"
zhihu_id: "556202715"
zhihu_title: "yiduobo的每日leetcode 2315.统计星号"
question_id: "2315"
question: "统计星号"
problem_url: "https://leetcode.cn/problems/count-asterisks/"
difficulty: "Easy"
created: "2022-08-21T17:00:49+08:00"
updated: "2022-08-21T17:00:49+08:00"
upvotes: 1
comments: 0
---

# 2315. 统计星号

> **[yiduobo的每日leetcode 2315.统计星号](https://zhuanlan.zhihu.com/p/556202715) · 知乎 · 2022-08-21 · 赞同 1**
> 力扣：[2315. 统计星号](https://leetcode.cn/problems/count-asterisks/) · Easy · 灵茶山艾府：[库函数模拟（Python 一行）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2315.统计星号

[力扣](https://leetcode.cn/problems/count-asterisks/)

题目要求统计不在竖线对中的星号数量，同时题目又保证了竖线是成对出现的，那么就可以使用一个状态标记flag来表示当前是否处于竖线对中，并根据竖线出现的情况来更新flag的值。flag的初始值为false，表示一开始不在竖线对中。

一趟遍历，对于当前字符：

1、如果是竖线，那么更新flag为not flag

2、如果是星号，那么当flag为false时则将答案加1，否则不做任何处理

3、如果是其他字符，直接跳过

最后附上python代码：

```python
class Solution(object):
    def countAsterisks(self, s):
        """
        :type s: str
        :rtype: int
        """

        res = 0
        flag = False
        for char in s:
            if char == '|':
                flag = not flag
            elif char == '*' and not flag:
                res += 1
        
        return res
```
