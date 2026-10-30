---
title: "2471. 逐层排序二叉树所需的最少操作数目"
aliases: ["yiduobo的每日leetcode 2471.逐层排序二叉树所需的最少操作数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/breadth-first-search", "leetcode/sorting", "题单/常用数据结构", "题单/链表-二叉树与回溯", "题单/常用数据结构/七-并查集", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/587881632"
zhihu_id: "587881632"
zhihu_title: "yiduobo的每日leetcode 2471.逐层排序二叉树所需的最少操作数目"
question_id: "2471"
question: "逐层排序二叉树所需的最少操作数目"
problem_url: "https://leetcode.cn/problems/minimum-number-of-operations-to-sort-a-binary-tree-by-level/"
difficulty: "Medium"
rating: 1635
created: "2022-11-29T23:48:04+08:00"
updated: "2022-11-29T23:48:04+08:00"
upvotes: 0
comments: 0
---

# 2471. 逐层排序二叉树所需的最少操作数目

> **[yiduobo的每日leetcode 2471.逐层排序二叉树所需的最少操作数目](https://zhuanlan.zhihu.com/p/587881632) · 知乎 · 2022-11-29 · 赞同 0**
> 力扣：[2471. 逐层排序二叉树所需的最少操作数目](https://leetcode.cn/problems/minimum-number-of-operations-to-sort-a-binary-tree-by-level/) · Medium · 灵茶山艾府：[BFS + 置换环 + 离散化](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2471.逐层排序二叉树所需的最少操作数目

[力扣](https://leetcode.cn/problems/minimum-number-of-operations-to-sort-a-binary-tree-by-level/)

首先需要注意的是，题目中的操作是交换节点的值而不是节点本身，这也就意味着上层节点交换值之后并不会影响下层节点的顺序，因此在这里就可以从上到下进行层序遍历，对于每一层单独计算排序交换所需的操作次数。

对于单独的一层而言，则可以先将这一层的节点值收集起来并排序，然后确定每个值的目标位置target。接下来只需一趟遍历，对于每个位置，若当前位置上的值v\[index\]的目标位置target\[v\[index\]\]不是当前位置，那么就不断将index与target\[v\[index\]\]上的值进行交换，直到当前位置上的值v\[index\]的目标位置target\[v\[index\]\]等于index为止。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def minimumOperations(self, root):
        """
        :type root: Optional[TreeNode]
        :rtype: int
        """

        res = 0
        q = [root]
        head, tail = 0, 1
        while head < tail:
            for now in q[head : tail]:
                if now.left:
                    q.append(now.left)
                if now.right:
                    q.append(now.right)
            
            head, tail = tail, len(q)
            v = [q[index].val for index in range(head, tail)]
            target = {}
            for index, num in enumerate(sorted(v)):
                target[num] = index

            for index in range(len(v)):
                while index != target[v[index]]:
                    target_pos = target[v[index]]
                    v[index], v[target_pos] = v[target_pos], v[index]
                    res += 1

        return res
```
