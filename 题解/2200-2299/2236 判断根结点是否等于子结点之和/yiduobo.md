---
title: "2236. 判断根结点是否等于子结点之和"
aliases: ["yiduobo的每日leetcode 2236.判断根结点是否等于子结点之和"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/depth-first-search", "leetcode/recursion"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/544667950"
zhihu_id: "544667950"
zhihu_title: "yiduobo的每日leetcode 2236.判断根结点是否等于子结点之和"
question_id: "2236"
question: "判断根结点是否等于子结点之和"
problem_url: "https://leetcode.cn/problems/root-equals-sum-of-children/"
difficulty: "Easy"
created: "2022-07-22T00:08:08+08:00"
updated: "2022-07-22T23:43:59+08:00"
upvotes: 0
comments: 0
---

# 2236. 判断根结点是否等于子结点之和

> **[yiduobo的每日leetcode 2236.判断根结点是否等于子结点之和](https://zhuanlan.zhihu.com/p/544667950) · 知乎 · 2022-07-22 · 赞同 0**
> 力扣：[2236. 判断根结点是否等于子结点之和](https://leetcode.cn/problems/root-equals-sum-of-children/) · Easy · 灵茶山艾府：[扩展：如果有 n 个节点要怎么做？（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2236.判断根结点是否等于子结点之和

[力扣](https://leetcode.cn/problems/root-equals-sum-of-children/)

感觉跟上一题是一起来的。。由于题目保证了树的结构与样例一致，因此可以放心使用root.left和root.right来找到左右孩子，接下来判断root.val是否等于root.left.val加上root.right.val就行了。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def checkTree(self, root):
        """
        :type root: Optional[TreeNode]
        :rtype: bool
        """

        return root.val == root.left.val + root.right.val
```
