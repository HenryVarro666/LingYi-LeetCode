---
title: "687. 最长同值路径"
aliases: ["yiduobo的每日leetcode 687.最长同值路径"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/tree", "leetcode/depth-first-search", "leetcode/recursion", "leetcode/dynamic-programming", "leetcode/binary-tree", "题单/链表-二叉树与回溯", "题单/动态规划", "题单/链表-二叉树与回溯/二-二叉树", "题单/动态规划/十二-树形-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/305865264"
zhihu_id: "305865264"
zhihu_title: "yiduobo的每日leetcode 687.最长同值路径"
question_id: "687"
question: "最长同值路径"
problem_url: "https://leetcode.cn/problems/longest-univalue-path/"
difficulty: "Medium"
created: "2020-11-22T14:34:39+08:00"
updated: "2020-11-22T14:34:39+08:00"
upvotes: 0
comments: 0
---

# 687. 最长同值路径

> **[yiduobo的每日leetcode 687.最长同值路径](https://zhuanlan.zhihu.com/p/305865264) · 知乎 · 2020-11-22 · 赞同 0**
> 力扣：[687. 最长同值路径](https://leetcode.cn/problems/longest-univalue-path/) · Medium · 灵茶山艾府：[【视频】彻底掌握直径 DP！从二叉树到一般树！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

687.最长同值路径

[力扣](https://leetcode-cn.com/problems/longest-univalue-path/)

题目要求树中节点值相同的最长路径，这条路径必然是由某棵子树的根节点，加上其左子树中的一条树链以及右子树中的一条树链构成，这里树链的长度可以为0，那么我们可以递归求解每棵子树包含其根节点在内的最长树链长度，对于某个节点now：

1、若now存在左孩子，那么递归求解now.left，得到包含now.left在内的左子树的最长树链长度，设为left。若now.val不等于now.left.val，那么now无法往左边延伸，于是将left置零。

2、若now存在右孩子，同样是递归求解now.right，得到right。若now.val不等于now.right.val，那么now无法往右边延伸，于是将right置零。

3、此时经过now的最长同值路径就是left + right + 1，用这个值更新答案。

4、包含now在内的树链的最长长度则为max(left, right) + 1，返回这个值供now的父亲节点使用。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def longestUnivaluePath(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """

        if not root:
            return 0
        
        self.res = 0
        self.dfs(root)
        return self.res - 1

    def dfs(self, now):
        left = right = 0

        if now.left:
            tmp = self.dfs(now.left)
            if now.left.val == now.val:
                left = tmp

        if now.right:
            tmp = self.dfs(now.right)
            if now.right.val == now.val:
                right = tmp
        
        self.res = max(self.res, left + right + 1)
        return max(left, right) + 1
```
