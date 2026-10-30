---
title: "655. 输出二叉树"
aliases: ["yiduobo的每日leetcode 655.输出二叉树"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/281953870"
zhihu_id: "281953870"
zhihu_title: "yiduobo的每日leetcode 655.输出二叉树"
question_id: "655"
question: "输出二叉树"
problem_url: "https://leetcode.cn/problems/print-binary-tree/"
created: "2020-11-09T23:01:31+08:00"
updated: "2020-11-09T23:01:31+08:00"
upvotes: 0
comments: 0
---

# 655. 输出二叉树

> **[yiduobo的每日leetcode 655.输出二叉树](https://zhuanlan.zhihu.com/p/281953870) · 知乎 · 2020-11-09 · 赞同 0**
> 力扣：[655. 输出二叉树](https://leetcode.cn/problems/print-binary-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

655.输出二叉树

[力扣](https://leetcode-cn.com/problems/print-binary-tree/)

我在这里采用的是先一趟dfs求出树的高度h，然后在一趟层序遍历填充最终的结果。当然也可以一趟直接完工，但是过程中需要计算和修正位置会比较麻烦。

先一趟dfs求出高度h之后，可以通过h得到每一层的宽度n \= 2^h - 1，那么最终答案就是一个h \* n的矩阵。我们用\*来对这个矩阵初始化，然后开始填充这个矩阵。

对于树中的每个节点，其都管辖着某个区间[l, r]。节点本身位于mid \= (l + r) / 2这个位置上，其左右子树则分别管辖着[l, mid - 1]以及[mid + 1, r]。于是我们可以从根节点开始向下进行层序遍历，其中根节点管辖范围是[0, n - 1]。

在层序遍历的过程中，对于当前处理的节点now，获取其管辖范围[l, r]，那么其位于当前层的 mid \= (l + r) / 2这个位置上。更新答案矩阵中的对应位置，然后若now.left不为空，那么将now.left以及[l, mid - 1]加入队列中；若now.right不为空，那么将now.right以及[mid + 1, r]加入队列中。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def printTree(self, root):
        """
        :type root: TreeNode
        :rtype: List[List[str]]
        """

        h = self.dfs(root)
        n = 2 ** h - 1

        q = [[root, 0, n - 1]]
        head = 0
        tail = 1
        res = []
        while head < tail:
            res.append([''] * (n))
            for index in range(head, tail):
                node, l, r = q[index]
                pos = (l + r) >> 1
                res[-1][pos] = str(node.val)
                if node.left:
                    q.append([node.left, l, pos - 1])
                if node.right:
                    q.append([node.right, pos + 1, r])
            
            head = tail
            tail = len(q)

        return res

    def dfs(self, now):
        if not now:
            return 0

        return max(self.dfs(now.left), self.dfs(now.right)) + 1
```
