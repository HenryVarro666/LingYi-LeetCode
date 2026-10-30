---
title: "653. 两数之和IV - 输入bst"
aliases: ["yiduobo的每日leetcode 653.两数之和IV - 输入bst"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/279376130"
zhihu_id: "279376130"
zhihu_title: "yiduobo的每日leetcode 653.两数之和IV - 输入bst"
question_id: "653"
question: "两数之和IV - 输入bst"
problem_url: "https://leetcode.cn/problems/two-sum-iv-input-is-a-bst/"
created: "2020-11-08T16:13:54+08:00"
updated: "2020-11-08T16:13:54+08:00"
upvotes: 0
comments: 0
---

# 653. 两数之和IV - 输入bst

> **[yiduobo的每日leetcode 653.两数之和IV - 输入bst](https://zhuanlan.zhihu.com/p/279376130) · 知乎 · 2020-11-08 · 赞同 0**
> 力扣：[653. 两数之和IV - 输入bst](https://leetcode.cn/problems/two-sum-iv-input-is-a-bst/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

653.两数之和IV

[力扣](https://leetcode-cn.com/problems/two-sum-iv-input-is-a-bst/)

对于输入的bst，其中序遍历是天然有序的，因此我们可以通过求其中序遍历得到有序的序列，然后在有序序列上使用双指针就能很快得到答案。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def findTarget(self, root, k):
        """
        :type root: TreeNode
        :type k: int
        :rtype: bool
        """

        num_list = self.dfs(root)

        l = 0
        r = len(num_list) - 1
        while l < r:
            if num_list[l] + num_list[r] == k:
                return True
            elif num_list[l] + num_list[r] > k:
                r -= 1
            else:
                l += 1
        
        return False

    def dfs(self, now):
        if now is None:
            return []

        return self.dfs(now.left) + [now.val] + self.dfs(now.right)
```
