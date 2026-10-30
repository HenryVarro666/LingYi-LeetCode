---
title: "2643. 一最多的行"
aliases: ["yiduobo的每日leetcode 2643.一最多的行"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/646798389"
zhihu_id: "646798389"
zhihu_title: "yiduobo的每日leetcode 2643.一最多的行"
question_id: "2643"
question: "一最多的行"
problem_url: "https://leetcode.cn/problems/row-with-maximum-ones/"
difficulty: "Easy"
created: "2023-07-30T01:15:52+08:00"
updated: "2023-07-30T01:15:52+08:00"
upvotes: 0
comments: 0
---

# 2643. 一最多的行

> **[yiduobo的每日leetcode 2643.一最多的行](https://zhuanlan.zhihu.com/p/646798389) · 知乎 · 2023-07-30 · 赞同 0**
> 力扣：[2643. 一最多的行](https://leetcode.cn/problems/row-with-maximum-ones/) · Easy · 灵茶山艾府：[遍历（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2643.一最多的行

[力扣](https://leetcode.cn/problems/row-with-maximum-ones/)

直接遍历每一行，统计行中一的数目并取最大值作为答案就行了。具体实现上，使用python这类的语言可以利用sum求行的和，因为每一行的和就是其中1的数目。

最后附上python代码：

```python
class Solution(object):
    def rowAndMaximumOnes(self, mat):
        """
        :type mat: List[List[int]]
        :rtype: List[int]
        """

        res = [0, 0]
        for i in range(len(mat)):
            cnt = sum(mat[i])
            if cnt > res[1]:
                res = [i, cnt]
        
        return res
```
