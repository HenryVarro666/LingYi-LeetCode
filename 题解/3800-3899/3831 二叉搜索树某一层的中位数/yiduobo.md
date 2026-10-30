---
title: "3831. 二叉搜索树某一层的中位数"
aliases: ["yiduobo的每日leetcode 3831.二叉搜索树某一层的中位数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2002225883365283791"
zhihu_id: "2002225883365283791"
zhihu_title: "yiduobo的每日leetcode 3831.二叉搜索树某一层的中位数"
question_id: "3831"
question: "二叉搜索树某一层的中位数"
problem_url: "https://leetcode.cn/problems/median-of-a-binary-search-tree-level/"
created: "2026-02-06T03:54:46+08:00"
updated: "2026-02-06T03:54:52+08:00"
upvotes: 1
comments: 0
---

# 3831. 二叉搜索树某一层的中位数

> **[yiduobo的每日leetcode 3831.二叉搜索树某一层的中位数](https://zhuanlan.zhihu.com/p/2002225883365283791) · 知乎 · 2026-02-06 · 赞同 1**
> 力扣：[3831. 二叉搜索树某一层的中位数](https://leetcode.cn/problems/median-of-a-binary-search-tree-level/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3831.二叉搜索树中某一层的中位数

<https://leetcode.cn/problems/median-of-a-binary-search-tree-level/description/>

题目给出一颗二叉搜索树的根节点root，以及一个整数level。

根节点位于第0层，所有孩子节点的层数都等于其父亲节点的层数加上1。

要求返回第level层中所有节点值的中位数。若该层不存在，或者没有节点，则返回-1。若该层节点数量为偶数，则返回中间靠右的那一个值。

由于题目需要计算的是某一层的中位数，于是可以从root开始向下进行层序遍历，找出第level层的所有节点然后计算中位数。

另一方面，由于题目给出的二叉搜索树，那么如果在层序遍历的bfs时，严格按照先左后右的顺序将孩子节点加入到bfs队列，那么队列中每一层对应的节点就必然是按照树中从左到右的顺序排好的，也就是说这些节点是天然有序的，因此答案就是将level这一层节点正中间的值。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def levelMedian(self, root, level):
        """
        :type root: Optional[TreeNode]
        :type level: int
        :rtype: int
        """
        
        q = [root]
        curr = 0
        head, tail = 0, 1

        while head < tail and curr < level:
            for x in q[head : tail]:
                if x.left:
                    q.append(x.left)
                if x.right:
                    q.append(x.right)
            
            head, tail = tail, len(q)
            curr += 1
        
        if curr < level or head == tail:
            return -1
        return q[head + (tail - head) // 2].val
```
