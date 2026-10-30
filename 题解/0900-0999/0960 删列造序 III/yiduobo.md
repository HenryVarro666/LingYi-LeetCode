---
title: "960. 删列造序III"
aliases: ["yiduobo的每日leetcode 960.删列造序III"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/四-经典线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/360865629"
zhihu_id: "360865629"
zhihu_title: "yiduobo的每日leetcode 960.删列造序III"
question_id: "960"
question: "删列造序 III"
problem_url: "https://leetcode.cn/problems/delete-columns-to-make-sorted-iii/"
difficulty: "Hard"
rating: 2247
created: "2021-03-29T22:31:24+08:00"
updated: "2021-03-29T22:31:24+08:00"
upvotes: 0
comments: 0
---

# 960. 删列造序III

> **[yiduobo的每日leetcode 960.删列造序III](https://zhuanlan.zhihu.com/p/360865629) · 知乎 · 2021-03-29 · 赞同 0**
> 力扣：[960. 删列造序 III](https://leetcode.cn/problems/delete-columns-to-make-sorted-iii/) · Hard · 灵茶山艾府：[最长递增子序列（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

960.删列造序III

[力扣](https://leetcode-cn.com/problems/delete-columns-to-make-sorted-iii/)

题目要求出最少删去多少列，那么我们可以反过来思考，将问题变成最多保留下来多少列。对于一列而言，其能保留下来的条件就是要么这是最左侧的那一列，要么每一行上的数比当前最右侧的那一列都要大。

到了这里就有一种最长上升子序列的即时感，不过这里的最长上升子序列是多行版的，于是也可以照搬动态规划的做法。令f[i]表示以第i列结尾最多可以保留多少列，那么对于f[i]而言：

1、若i\=0，那么其自然可以保留，于是有f[i] \= 1

2、若i > 0：

2-1）第0到i - 1列都可以不要，那么可以初始化f[i] \= 1

2-2）其也可以可以接在满足条件的列j后面，其中0 \<\= j \< i，同时满足第j列每一行上的数都小于等于第i列上的数。那么这里从0到i - 1进行遍历，找出满足条件的j，那么这里就有

f[i] \= max(f[j]) + 1

最后答案就是l - max(f)，其中l为总列数。

最后附上python代码：

```python
class Solution(object):
    def minDeletionSize(self, strs):
        """
        :type strs: List[str]
        :rtype: int
        """

        n = len(strs)
        l = len(strs[0])
        f = [0] * l
        f[0] = 1
        for i in range(1, l):
            tmp = 0
            for j in range(0, i):
                flag = True
                for k in range(n):
                    if strs[k][i] < strs[k][j]:
                        flag = False
                        break
                if flag:
                    tmp = max(tmp, f[j])
            
            f[i] = tmp + 1
        
        return l - max(f)
```
