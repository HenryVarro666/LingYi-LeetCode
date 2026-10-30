---
title: "3437. 全排列III"
aliases: ["yiduobo的每日leetcode 3437.全排列III"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1889099027175429958"
zhihu_id: "1889099027175429958"
zhihu_title: "yiduobo的每日leetcode 3437.全排列III"
question_id: "3437"
question: "全排列III"
problem_url: "https://leetcode.cn/problems/permutations-iii/"
created: "2025-03-28T23:43:04+08:00"
updated: "2025-03-28T23:43:04+08:00"
upvotes: 0
comments: 0
---

# 3437. 全排列III

> **[yiduobo的每日leetcode 3437.全排列III](https://zhuanlan.zhihu.com/p/1889099027175429958) · 知乎 · 2025-03-28 · 赞同 0**
> 力扣：[3437. 全排列III](https://leetcode.cn/problems/permutations-iii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3437.全排列III

[3437. 全排列 III - 力扣（LeetCode）](https://leetcode.cn/problems/permutations-iii/description/)

题目给定一个整数n，另外定义一个交替排列是没有两个相邻元素同时为奇数或偶数的前n个正整数的排列。现在要求按字典序返回所有的交替排列。

经典搜索回溯问题的变形，依然可以使用回溯法解决。本题中要求相邻元素不能同奇偶，因此在搜索的每一步都需要保证当前填充的元素与上一个填充的元素不同奇偶，其他的就按之前的处理方法来做就行了。

最后附上python代码：

```python
class Solution(object):
    def permute(self, n):
        """
        :type n: int
        :rtype: List[List[int]]
        """
        
        def dfs(now, vis, res):
            if len(now) == n:
                res.append(now[:])
                return
            
            for v in range(1, n + 1):
                if vis[v] or (now and (v + now[-1]) % 2 == 0):
                    continue
                vis[v] = True
                now.append(v)
                dfs(now, vis, res)
                now.pop()
                vis[v] = False
        
        res = []
        dfs([], [False] * (n + 1), res)
        return res
```
