---
title: "1022. 从根到叶的二进制数之和"
aliases: ["yiduobo的每日leetcode 1022.从根到叶的二进制数之和"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/depth-first-search", "leetcode/recursion", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/368935790"
zhihu_id: "368935790"
zhihu_title: "yiduobo的每日leetcode 1022.从根到叶的二进制数之和"
question_id: "1022"
question: "从根到叶的二进制数之和"
problem_url: "https://leetcode.cn/problems/sum-of-root-to-leaf-binary-numbers/"
difficulty: "Easy"
rating: 1462
created: "2021-04-29T23:10:39+08:00"
updated: "2021-04-29T23:10:39+08:00"
upvotes: 0
comments: 0
---

# 1022. 从根到叶的二进制数之和

> **[yiduobo的每日leetcode 1022.从根到叶的二进制数之和](https://zhuanlan.zhihu.com/p/368935790) · 知乎 · 2021-04-29 · 赞同 0**
> 力扣：[1022. 从根到叶的二进制数之和](https://leetcode.cn/problems/sum-of-root-to-leaf-binary-numbers/) · Easy · 灵茶山艾府：[两种 DFS 写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1022.从根到叶的二进制数之和

[力扣](https://leetcode-cn.com/problems/sum-of-root-to-leaf-binary-numbers/)

从根节点开始进行dfs，带着从根节点开始到当前节点结束的二进制值前缀prefix往下走。对于当前节点now而言，这个前缀prefix的值应当更新为prefix + prefix + now.val。若当前节点为叶子节点，那么此时的prefix就是所求的二进制值，直接返回即可；若当前节点不是叶子节点，那么就递归求解当前节点的左右孩子，然后返回二者求解的和即可。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def sumRootToLeaf(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """

        return self.dfs(root, 0)
    
    def dfs(self, now, prefix):
        prefix = prefix + prefix + now.val
        if not now.left and not now.right:
            return prefix
        
        ret = 0
        if now.left:
            ret += self.dfs(now.left, prefix)
        
        if now.right:
            ret += self.dfs(now.right, prefix)
        
        return ret
```
