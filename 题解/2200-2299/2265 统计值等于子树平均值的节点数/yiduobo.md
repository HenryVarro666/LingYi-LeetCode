---
title: "2265. 统计值等于子树平均值的节点数"
aliases: ["yiduobo的每日leetcode 2265.统计值等于子树平均值的节点数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/recursion", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/548785990"
zhihu_id: "548785990"
zhihu_title: "yiduobo的每日leetcode 2265.统计值等于子树平均值的节点数"
question_id: "2265"
question: "统计值等于子树平均值的节点数"
problem_url: "https://leetcode.cn/problems/count-nodes-equal-to-average-of-subtree/"
difficulty: "Medium"
rating: 1473
created: "2022-08-02T00:19:43+08:00"
updated: "2022-08-02T00:19:43+08:00"
upvotes: 0
comments: 0
---

# 2265. 统计值等于子树平均值的节点数

> **[yiduobo的每日leetcode 2265.统计值等于子树平均值的节点数](https://zhuanlan.zhihu.com/p/548785990) · 知乎 · 2022-08-02 · 赞同 0**
> 力扣：[2265. 统计值等于子树平均值的节点数](https://leetcode.cn/problems/count-nodes-equal-to-average-of-subtree/) · Medium · 灵茶山艾府：[统计子树元素和 & 子树大小（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2265.统计值等于子树平均值的节点数

[力扣](https://leetcode.cn/problems/count-nodes-equal-to-average-of-subtree/)

对于树中的任意节点node，设其左右孩子分别为node.left和node.right。为了求出以node为根节点的子树的平均值，就需要知道这颗树中各节点数值之和，以及这棵树中节点的数目。

对于树中相关问题的求解，可以考虑使用递归来进行求解。

以node为根节点的树中所有节点数值之和，就等于以node.left为根节点的子树中所有节点数值之和，加上等于以node.right为根节点的子树中所有节点数值之和，再加上node自身的数值。

以node为根节点的树中的节点数目，则等于以node.left为根节点的子树中的节点数目，加上等于以node.right为根节点的子树中节点的数目，再加上1，也就是node自身。

除了上述两个值，还需要求解当前子树中值等于子树的平均值的节点数目，这个值同样是优先递归求解左右子树，然后根据开始求得的节点数值之和以及节点数目计算出平均值，再判断当前节点自身是否为满足条件的节点。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def averageOfSubtree(self, root):
        """
        :type root: Optional[TreeNode]
        :rtype: int
        """

        def dfs(now):
            res = 0
            cnt = 1
            s = now.val
            if now.left:
                left_res, left_cnt, left_s = dfs(now.left)
                res += left_res
                cnt += left_cnt
                s += left_s
            
            if now.right:
                right_res, right_cnt, right_s = dfs(now.right)
                res += right_res
                cnt += right_cnt
                s += right_s
            
            if s / cnt == now.val:
                res += 1
            
            return res, cnt, s

        return dfs(root)[0]
```
