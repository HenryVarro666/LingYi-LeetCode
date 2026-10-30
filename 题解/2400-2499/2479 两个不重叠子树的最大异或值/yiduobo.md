---
title: "2479. 两个不重叠子树的最大异或值"
aliases: ["yiduobo的每日leetcode 2479.两个不重叠子树的最大异或值"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/632563393"
zhihu_id: "632563393"
zhihu_title: "yiduobo的每日leetcode 2479.两个不重叠子树的最大异或值"
question_id: "2479"
question: "两个不重叠子树的最大异或值"
problem_url: "https://leetcode.cn/problems/maximum-xor-of-two-non-overlapping-subtrees/"
created: "2023-05-27T03:18:13+08:00"
updated: "2023-05-27T03:18:13+08:00"
upvotes: 0
comments: 0
---

# 2479. 两个不重叠子树的最大异或值

> **[yiduobo的每日leetcode 2479.两个不重叠子树的最大异或值](https://zhuanlan.zhihu.com/p/632563393) · 知乎 · 2023-05-27 · 赞同 0**
> 力扣：[2479. 两个不重叠子树的最大异或值](https://leetcode.cn/problems/maximum-xor-of-two-non-overlapping-subtrees/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2479.两个不重叠子树的最大异或值

[力扣](https://leetcode.cn/problems/maximum-xor-of-two-non-overlapping-subtrees/)

对于这类最大异或值问题，一种可行的做法是利用trie树来辅助求解。具体来说，就是利用trie树储存每个数字的二进制表示，那么对于一次查询，则只需从根节点向下，每一位都尽量往与当前查询数字对应二进制相反的子树中走即可。

之前的1707题就是使用了这种处理方法，具体可以参考：

[yiduobo：yiduobo的每日leetcode 1707.与数组中元素的最大异或值](https://zhuanlan.zhihu.com/p/449610412)

对于本题，除了最大异或值的问题外，还需要要求子树不重叠。

一种可行的处理方法是先进行一次dfs，求解以每个节点为根节点的子树中的节点值之后，然后再采用类似后续遍历的处理方法，先递归求解子树并完成子树中的查询，然后完成当前节点的查询。查询完成后，再将当前节点值加入到trie树中。这样一来就可以保证不会出现重叠的情况。

最后附上python代码：

```python
class Node(object):

    def __init__(self):
        self.childs = [None, None]

class Solution(object):
    def maxXor(self, n, edges, values):
        """
        :type n: int
        :type edges: List[List[int]]
        :type values: List[int]
        :rtype: int
        """

        def check(v):
            ma = 0
            now = trie
            for index in range(46, -1, -1):
                digit = (v >> index) & 1
                target = 1 - digit
                if now.childs[target] is not None:
                    ma = ma + ma + 1
                    now = now.childs[target]
                elif now.childs[digit] is not None:
                    ma = ma + ma
                    now = now.childs[digit]
                else:
                    return 0

            return ma

        def add(v):
            now = trie
            for index in range(46, -1, -1):
                digit = (v >> index) & 1
                if now.childs[digit] is None:
                    tmp = Node()
                    now.childs[digit] = tmp
                
                now = now.childs[digit]

        def dfs(now, fa):
            s[now] = values[now]
            for next in g[now]:
                if next != fa:
                    s[now] += dfs(next, now)

            return s[now]

        def query(now, fa):
            global res
            res = max(res, check(s[now]))
            for next in g[now]:
                if next != fa:
                    query(next, now)
            
            add(s[now])

        trie = Node()

        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        s = [0] * n
        dfs(0, None)

        global res
        res = 0
        query(0, None)

        return res
```
