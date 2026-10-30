---
title: "2196. 根据描述创建二叉树"
aliases: ["yiduobo的每日leetcode 2196.根据描述创建二叉树"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/hash-table", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/538510134"
zhihu_id: "538510134"
zhihu_title: "yiduobo的每日leetcode 2196.根据描述创建二叉树"
question_id: "2196"
question: "根据描述创建二叉树"
problem_url: "https://leetcode.cn/problems/create-binary-tree-from-descriptions/"
difficulty: "Medium"
rating: 1644
created: "2022-07-07T00:07:50+08:00"
updated: "2022-07-07T00:07:50+08:00"
upvotes: 1
comments: 0
---

# 2196. 根据描述创建二叉树

> **[yiduobo的每日leetcode 2196.根据描述创建二叉树](https://zhuanlan.zhihu.com/p/538510134) · 知乎 · 2022-07-07 · 赞同 1**
> 力扣：[2196. 根据描述创建二叉树](https://leetcode.cn/problems/create-binary-tree-from-descriptions/) · Medium · 灵茶山艾府：[哈希表建树 + 位运算优化找根（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2196.根据描述创建二叉树

[力扣](https://leetcode.cn/problems/create-binary-tree-from-descriptions/)

由于题目中各节点的值各不相同，因此可以利用节点的值作为key，节点本身作为对应的value，通过哈希表来完成树的构建。具体来说就是遍历descriptions，通过当前的parent和child从哈希表中找出对应的节点。若不存在，则在哈希表中新加入对应的节点。接下来对于找到的节点，通过isLeft完成关联就好了。

遍历完成后，树实际上已经建好了，只需遍历所有节点，找出从未当过child的节点作为根节点返回即可。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def createBinaryTree(self, descriptions):
        """
        :type descriptions: List[List[int]]
        :rtype: Optional[TreeNode]
        """

        f_set = set()
        node_dict = {}
        for parent, child, isLeft in descriptions:
            if parent not in node_dict:
                node_dict[parent] = TreeNode(parent)
            node_parent = node_dict[parent]

            if child not in node_dict:
                node_dict[child] = TreeNode(child)
            node_child = node_dict[child]

            if isLeft:
                node_parent.left = node_child
            else:
                node_parent.right = node_child
            
            f_set.add(child)
        
        for parent, _, _ in descriptions:
            if parent not in f_set:
                return node_dict[parent]
```
