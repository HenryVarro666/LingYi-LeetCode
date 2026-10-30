---
title: "112. 路径总和 & 113. 路径总和II"
aliases: ["yiduobo的每日leetcode 112.路径总和 && 113.路径总和II", "112. 路径总和", "113. 路径总和II"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/depth-first-search", "leetcode/recursion", "题单/链表-二叉树与回溯", "题单/面试经典-150-题", "题单/链表-二叉树与回溯/二-二叉树", "题单/面试经典-150-题/二叉树", "leetcode/medium", "leetcode/backtracking", "leetcode/binary-tree"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/138849283"
zhihu_id: "138849283"
zhihu_title: "yiduobo的每日leetcode 112.路径总和 && 113.路径总和II"
question_id: ["112", "113"]
question: ["路径总和", "路径总和 II"]
problem_url: ["https://leetcode.cn/problems/path-sum/", "https://leetcode.cn/problems/path-sum-ii/"]
difficulty: ["Easy", "Medium"]
created: "2020-05-07T21:56:58+08:00"
updated: "2020-05-07T21:56:58+08:00"
upvotes: 1
comments: 0
---

# 112. 路径总和 & 113. 路径总和II

> **[yiduobo的每日leetcode 112.路径总和 && 113.路径总和II](https://zhuanlan.zhihu.com/p/138849283) · 知乎 · 2020-05-07 · 赞同 1**
> 力扣：[112. 路径总和](https://leetcode.cn/problems/path-sum/) · Easy · 灵茶山艾府：[简洁写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)
> 力扣：[113. 路径总和 II](https://leetcode.cn/problems/path-sum-ii/) · Medium · 灵茶山艾府：[回溯，附常见问题及其解答（Python/Java/C++/Go/JS/Rust）](../0113%20路径总和%20II/灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

112.路径总和<https://leetcode-cn.com/problems/path-sum/>

113.路径总和II<https://leetcode-cn.com/problems/path-sum-ii/>

112题要求树中是否存在根到叶子的路径满足路径上节点的和等于sum，113题则是找出所有这种路径。

两个问题都是用搜索回溯来解决，每次尝试往左子树或者右子树走，同时修改此时的sum。如果当前节点是叶子结点，那么判断该节点的值是否等于现在的sum，如果是，说明找到了一组解，将其记录下来即可。

最后附上python代码，这里是113题的代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def pathSum(self, root, sum):
        """
        :type root: TreeNode
        :type sum: int
        :rtype: List[List[int]]
        """

        res = []
        self.dfs(root, sum, [], res)
        return res

    def dfs(self, now_node, s, now_choose, res):
        if not now_node:
            return
        if not now_node.left and not now_node.right:
            if now_node.val == s:
                res.append(now_choose[:] + [now_node.val])
        else:
            now_choose.append(now_node.val)
            s -= now_node.val
            if now_node.left:
                self.dfs(now_node.left, s, now_choose, res)
            if now_node.right:
                self.dfs(now_node.right, s, now_choose, res)
            s += now_node.val
            now_choose.pop()
```
