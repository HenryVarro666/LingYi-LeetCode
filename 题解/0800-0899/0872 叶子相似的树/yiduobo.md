---
title: "872. 叶子相似的树"
aliases: ["yiduobo的每日leetcode 872.叶子相似的树"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/depth-first-search", "leetcode/recursion", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/350431776"
zhihu_id: "350431776"
zhihu_title: "yiduobo的每日leetcode 872.叶子相似的树"
question_id: "872"
question: "叶子相似的树"
problem_url: "https://leetcode.cn/problems/leaf-similar-trees/"
difficulty: "Easy"
rating: 1288
created: "2021-02-13T17:08:33+08:00"
updated: "2021-02-13T17:08:33+08:00"
upvotes: 0
comments: 0
---

# 872. 叶子相似的树

> **[yiduobo的每日leetcode 872.叶子相似的树](https://zhuanlan.zhihu.com/p/350431776) · 知乎 · 2021-02-13 · 赞同 0**
> 力扣：[872. 叶子相似的树](https://leetcode.cn/problems/leaf-similar-trees/) · Easy · 灵茶山艾府：[简单题，简单做（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

872.叶子相似的树

[力扣](https://leetcode-cn.com/problems/leaf-similar-trees/)

叶子节点是没有左右孩子的节点，于是只需要对两棵树分别进行dfs，若当前节点没有左右孩子，那么该节点就是一个叶子节点，将其加入对应的数组；若当前节点有左孩子或者右孩子，那么就递归进行求解。dfs完成后，判断两个叶子节点数组是否一致即可。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def leafSimilar(self, root1, root2):
        """
        :type root1: TreeNode
        :type root2: TreeNode
        :rtype: bool
        """

        list1 = []
        list2 = []
        self.dfs(root1, list1)
        self.dfs(root2, list2)
        return list1 == list2
    
    def dfs(self, now, leaf_list):
        if not now.left and not now.right:
            leaf_list.append(now.val)
        else:
            if now.left:
                self.dfs(now.left, leaf_list)
            if now.right:
                self.dfs(now.right, leaf_list)
```
