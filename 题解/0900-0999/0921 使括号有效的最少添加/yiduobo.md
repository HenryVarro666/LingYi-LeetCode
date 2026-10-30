---
title: "921. 使括号有效的最少添加"
aliases: ["yiduobo的每日leetcode 921.使括号有效的最少添加"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/355879488"
zhihu_id: "355879488"
zhihu_title: "yiduobo的每日leetcode 921.使括号有效的最少添加"
question_id: "921"
question: "使括号有效的最少添加"
problem_url: "https://leetcode.cn/problems/minimum-add-to-make-parentheses-valid/"
created: "2021-03-09T22:46:36+08:00"
updated: "2021-03-09T22:46:36+08:00"
upvotes: 0
comments: 0
---

# 921. 使括号有效的最少添加

> **[yiduobo的每日leetcode 921.使括号有效的最少添加](https://zhuanlan.zhihu.com/p/355879488) · 知乎 · 2021-03-09 · 赞同 0**
> 力扣：[921. 使括号有效的最少添加](https://leetcode.cn/problems/minimum-add-to-make-parentheses-valid/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

921.使括号有效的最少添加

[力扣](https://leetcode-cn.com/problems/minimum-add-to-make-parentheses-valid/)

如果我们从左向右扫描，那么某一时刻，若左括号的数量大于右括号的数量，我们可以指望后续的序列中提供足够的右括号来适配这些多出的左括号，但是反过来，若右括号的数量大于左括号的数量，我们就必须立刻补上左括号来进行适配。

于是现在有了一种做法，从头到尾一趟扫描，统计当前左右括号数量之差。若某一时刻右括号数量多于左括号，那么添加一个左括号配平，同时答案加一。遍历完成后，若此时左括号数量大于右括号数量，那么一次性添加足够的右括号配平。

最后附上python代码：

```python
class Solution(object):
    def minAddToMakeValid(self, S):
        """
        :type S: str
        :rtype: int
        """

        l = 0
        res = 0
        for char in S:
            if char == '(':
                l += 1
            else:
                l -= 1
                if l < 0:
                    l = 0
                    res += 1
        
        return res + l
```
