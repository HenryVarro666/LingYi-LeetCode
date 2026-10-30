---
title: "386. 字典序排数"
aliases: ["yiduobo的每日leetcode 386.字典序排数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/168795214"
zhihu_id: "168795214"
zhihu_title: "yiduobo的每日leetcode 386.字典序排数"
question_id: "386"
question: "字典序排数"
problem_url: "https://leetcode.cn/problems/lexicographical-numbers/"
created: "2020-08-06T00:20:04+08:00"
updated: "2020-08-06T00:20:04+08:00"
upvotes: 0
comments: 0
---

# 386. 字典序排数

> **[yiduobo的每日leetcode 386.字典序排数](https://zhuanlan.zhihu.com/p/168795214) · 知乎 · 2020-08-06 · 赞同 0**
> 力扣：[386. 字典序排数](https://leetcode.cn/problems/lexicographical-numbers/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

386.字典序排数<https://leetcode-cn.com/problems/lexicographical-numbers/>

题目要求按字典序排列1到n，可以发现相邻的项要么具有相同的前缀，要么全然无关从头开始，那么如果将这些数按位放到trie树中，就可以发现题目实际上是要在trie中做一个类似前序遍历的遍历。

当然，在这里我们没必要一开始就将trie数构造出来，而是在搜索回溯的过程中逐个构造其叶子节点即可。

最后附上python代码：

```python
class Solution(object):
    def lexicalOrder(self, n):
        """
        :type n: int
        :rtype: List[int]
        """

        res = []
        for now in range(1, 10):
            if now <= n:
                res.append(now)
                self.dfs(now, n, res)

        return res

    def dfs(self, now, n, res):
        for num in range(10):
            tmp = now * 10 + num
            if tmp <= n:
                res.append(tmp)
                self.dfs(tmp, n, res)
```
