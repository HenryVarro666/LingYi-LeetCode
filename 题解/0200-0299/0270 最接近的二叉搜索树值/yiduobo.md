---
title: "270. 最接近的二叉搜索树值"
aliases: ["yiduobo的每日leetcode 270.最接近的二叉搜索树值"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/593968398"
zhihu_id: "593968398"
zhihu_title: "yiduobo的每日leetcode 270.最接近的二叉搜索树值"
question_id: "270"
question: "最接近的二叉搜索树值"
problem_url: "https://leetcode.cn/problems/closest-binary-search-tree-value/"
created: "2022-12-24T02:38:38+08:00"
updated: "2022-12-24T02:38:38+08:00"
upvotes: 0
comments: 0
---

# 270. 最接近的二叉搜索树值

> **[yiduobo的每日leetcode 270.最接近的二叉搜索树值](https://zhuanlan.zhihu.com/p/593968398) · 知乎 · 2022-12-24 · 赞同 0**
> 力扣：[270. 最接近的二叉搜索树值](https://leetcode.cn/problems/closest-binary-search-tree-value/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

270.最接近的二叉搜索树值

[力扣](https://leetcode.cn/problems/closest-binary-search-tree-value/)

在二叉搜索树中查找某个值的常规做法是根据当前节点与要查找的值的大小关系来判断这个值处于当前节点的左子树还是右子树，然后转入对应的子树中继续查找，直到走到叶子节点或者找到这个值。

对于本题，则可以直接套用这种查找方法，从根节点开始向下走到某个叶子节点，在向下行走的过程中使用经过的每一个节点值来更新最终答案。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def closestValue(self, root, target):
        """
        :type root: TreeNode
        :type target: float
        :rtype: int
        """

        now = root
        res = None

        while now:
            if res is None or abs(res - target) > abs(now.val - target):
                res = now.val
            
            if now.val > target:
                now = now.left
            else:
                now = now.right
        
        return res
```
