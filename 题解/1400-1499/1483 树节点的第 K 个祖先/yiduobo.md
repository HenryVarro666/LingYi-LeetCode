---
title: "1483. 树节点的第K个祖先"
aliases: ["yiduobo的每日leetcode 1483.树节点的第K个祖先"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/tree", "leetcode/design", "leetcode/dynamic-programming", "leetcode/di-tui", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/三-一般树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/416049592"
zhihu_id: "416049592"
zhihu_title: "yiduobo的每日leetcode 1483.树节点的第K个祖先"
question_id: "1483"
question: "树节点的第 K 个祖先"
problem_url: "https://leetcode.cn/problems/kth-ancestor-of-a-tree-node/"
difficulty: "Hard"
rating: 2115
created: "2021-10-01T14:44:46+08:00"
updated: "2021-10-01T14:44:46+08:00"
upvotes: 0
comments: 0
---

# 1483. 树节点的第K个祖先

> **[yiduobo的每日leetcode 1483.树节点的第K个祖先](https://zhuanlan.zhihu.com/p/416049592) · 知乎 · 2021-10-01 · 赞同 0**
> 力扣：[1483. 树节点的第 K 个祖先](https://leetcode.cn/problems/kth-ancestor-of-a-tree-node/) · Hard · 灵茶山艾府：[【模板讲解】树上倍增算法（以及最近公共祖先）Python/Java/C++/Go](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1483.树节点的第K个祖先

[力扣](https://leetcode-cn.com/problems/kth-ancestor-of-a-tree-node/)

经典的动态规划问题，令f[i][j]表示从节点i开始，朝根节点走2^j步之后走到的节点，那么对于f[i][j]：

1、先考虑边界情况。当j为0时，f[i][j]显然就是i的父亲节点

2、接下来考察j > 0的情况，此时f[i][j]表示的是i往上走2^j步的节点。不妨将这里的2^j拆开变成两个2^(j - 1)之和，那么就相当于从i往上走2^(j - 1)走到i'，然后从i'再往上走2^(j - 1)走到目标节点。这里的i'就是f[i][j - 1]，而目标节点则是f[i'][j - 1]，于是有

f\[i\]\[j\] \= f\[i'\]\[j - 1\] \= f\[f\[i\]\[j - 1\]\]\[j - 1\]

先通过动态规划求解出f，然后对于每一轮询问(node, k)，先将k进行拆分，得到

k \= 2^p1 + 2^p2 + ... + 2^pn

接下来从node开始，先向上走2^p1步，也就是f\[node\]\[p1\]，接下来再从f\[node\]\[p1\]向上走2^p2步，也就是f\[f\[node\]\[p1\]\]\[p2\]。重复此过程，直到走完k步为止。

在这里需要注意步数不够的情况，避免数组越界。

最后附上python代码：

```python
class TreeAncestor(object):

    def __init__(self, n, parent):
        """
        :type n: int
        :type parent: List[int]
        """

        self.p = 0
        self.pow2 = [1]
        while self.pow2[-1] < n - 1:
            self.p += 1
            self.pow2.append(self.pow2[-1] + self.pow2[-1])
        
        self.f = [[None] * (self.p + 1) for _ in range(n)]
        for level in range(self.p + 1):
            for index in range(n):
                if level == 0:
                    self.f[index][level] = parent[index]
                elif self.f[index][level - 1] != -1:
                    self.f[index][level] = self.f[self.f[index][level - 1]][level - 1]
                else:
                    self.f[index][level] = -1

    def getKthAncestor(self, node, k):
        """
        :type node: int
        :type k: int
        :rtype: int
        """

        now = node
        level = self.p
        while now != -1 and k > 0:
            while k < self.pow2[level]:
                level -= 1
            
            now = self.f[now][level]
            k -= self.pow2[level]
        
        return now

# Your TreeAncestor object will be instantiated and called as such:
# obj = TreeAncestor(n, parent)
# param_1 = obj.getKthAncestor(node,k)
```
