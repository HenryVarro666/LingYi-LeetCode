---
title: "366. 寻找二叉树的叶子节点"
aliases: ["yiduobo的每日leetcode 366.寻找二叉树的叶子节点"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/598381413"
zhihu_id: "598381413"
zhihu_title: "yiduobo的每日leetcode 366.寻找二叉树的叶子节点"
question_id: "366"
question: "寻找二叉树的叶子节点"
problem_url: "https://leetcode.cn/problems/find-leaves-of-binary-tree/"
created: "2023-01-11T22:25:10+08:00"
updated: "2023-01-11T22:25:10+08:00"
upvotes: 0
comments: 0
---

# 366. 寻找二叉树的叶子节点

> **[yiduobo的每日leetcode 366.寻找二叉树的叶子节点](https://zhuanlan.zhihu.com/p/598381413) · 知乎 · 2023-01-11 · 赞同 0**
> 力扣：[366. 寻找二叉树的叶子节点](https://leetcode.cn/problems/find-leaves-of-binary-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

366.寻找二叉树的叶子节点

[力扣](https://leetcode.cn/problems/find-leaves-of-binary-tree/)

根据题目的描述，每个节点会在其所有孩子节点全部被删除之后的下一轮遭到删除，那么在这里就可以从根节点向下递归求解。对于当前节点now，先递归求解now.left和now.right遭到删除的轮次，那么now被删除的轮次就是二者中较大值加上1。使用一个哈希表将所有节点收集起来，key为每个节点被删除的轮次，递归求解完成后将哈希表按照key从小到大排序后输出即可。

需要注意的是，由于题目要求从左至右删除节点，因此在递归求解时需要先求解左子树再求解右子树。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def findLeaves(self, root):
        """
        :type root: TreeNode
        :rtype: List[List[int]]
        """

        node_dict = {}

        def dfs(now):
            if not now.left:
                if not now.right:
                    level = 0
                else:
                    level = dfs(now.right) + 1
            elif not now.right:
                level = dfs(now.left) + 1
            else:
                level = max(dfs(now.left), dfs(now.right)) + 1
            
            if level not in node_dict:
                node_dict[level] = []
            node_dict[level].append(now.val)
            return level

        dfs(root)

        return [x[1] for x in sorted(node_dict.items(), key=lambda d:d[0])]
```
