---
title: "958. 二叉树的完全性检验"
aliases: ["yiduobo的每日leetcode 958.二叉树的完全性检验"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/360523724"
zhihu_id: "360523724"
zhihu_title: "yiduobo的每日leetcode 958.二叉树的完全性检验"
question_id: "958"
question: "二叉树的完全性检验"
problem_url: "https://leetcode.cn/problems/check-completeness-of-a-binary-tree/"
created: "2021-03-28T16:32:27+08:00"
updated: "2021-03-28T16:32:27+08:00"
upvotes: 1
comments: 0
---

# 958. 二叉树的完全性检验

> **[yiduobo的每日leetcode 958.二叉树的完全性检验](https://zhuanlan.zhihu.com/p/360523724) · 知乎 · 2021-03-28 · 赞同 1**
> 力扣：[958. 二叉树的完全性检验](https://leetcode.cn/problems/check-completeness-of-a-binary-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

958.二叉树的完全性检验

[力扣](https://leetcode-cn.com/problems/check-completeness-of-a-binary-tree/)

完全二叉树要求除最后一层之外的所有层都是满的，且最后一层节点全部靠左。既然涉及到层相关，那么自然想到使用层序遍历来检测。

由于前面层都是满的，那么对于第k层而言，其必然具有2^k个节点。每一层的节点个数则可以通过层序遍历队列的长度来计算，那么对比这个节点个数以及2^k就可以得知当前层是否是最下层。最下层节点自然是不能再具有孩子节点的。

另外，对于倒数第二层节点，若某个节点没有左孩子，那么其也不能拥有右孩子，同一层右侧的所有节点都不能有孩子节点。同理，若某个节点没有右孩子，那么同一层的右侧的所有节点也不能有孩子节点。

根据上面两个判断条件，可以设置两个标记leaf_flag以及stop_flag，分别表示当前层是否为最后一层，以及当前层后续的节点是否能继续有孩子节点。

在层序遍历的过程中，每次遍历新的一层时，先根据队列长度判断leaf_flag是否应该为true，同时置stop_flag为false。接下里，对于当前节点依次检测是否具有左孩子和右孩子。若存在某个孩子，且此时的leaf_flag或stop_flag为true，说明这个树不是完全二叉树。若缺失了某个孩子，则说明同一层后续都不应该再具有孩子节点，那么置stop_flag为true。

若可以遍历完整棵树，那么说明这棵树是完全二叉树。

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def isCompleteTree(self, root):
        """
        :type root: TreeNode
        :rtype: bool
        """

        q = [root]
        l = 0
        r = 1
        full_len = 1
        while l < r:
            leaf_flag = (r - l) != full_len
            full_len += full_len
            stop_flag = False
            for now in q[l : r]:
                if now.left:
                    if stop_flag or leaf_flag:
                        return False
                    q.append(now.left)
                else:
                    stop_flag = True

                if now.right:
                    if stop_flag or leaf_flag:
                        return False
                    q.append(now.right)
                else:
                    stop_flag = True
            
            l, r = r, len(q)
        
        return True
```
