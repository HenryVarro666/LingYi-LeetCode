---
title: "108. 将有序数组转化成二叉搜索树"
aliases: ["yiduobo的每日leetcode 108.将有序数组转化成二叉搜索树"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/recursion", "leetcode/divide-and-conquer", "题单/链表-二叉树与回溯", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/链表-二叉树与回溯/二-二叉树", "题单/LeetCode-热题-100/二叉树", "题单/面试经典-150-题/分治"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/138530184"
zhihu_id: "138530184"
zhihu_title: "yiduobo的每日leetcode 108.将有序数组转化成二叉搜索树"
question_id: "108"
question: "将有序数组转换为二叉搜索树"
problem_url: "https://leetcode.cn/problems/convert-sorted-array-to-binary-search-tree/"
difficulty: "Easy"
created: "2020-05-06T17:31:35+08:00"
updated: "2020-05-06T17:31:35+08:00"
upvotes: 0
comments: 0
---

# 108. 将有序数组转化成二叉搜索树

> **[yiduobo的每日leetcode 108.将有序数组转化成二叉搜索树](https://zhuanlan.zhihu.com/p/138530184) · 知乎 · 2020-05-06 · 赞同 0**
> 力扣：[108. 将有序数组转换为二叉搜索树](https://leetcode.cn/problems/convert-sorted-array-to-binary-search-tree/) · Easy · 灵茶山艾府：[入门递归，从二叉树开始（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

昨日有事外出，今天补上。

108.将有序数组转化成二叉搜索树<https://leetcode-cn.com/problems/convert-sorted-array-to-binary-search-tree/>

比较基础的题目。

对于一个节点的情况，这个节点就是要求的树。

对于两个节点的情况，其中一个作为根，另一个作为左孩子或者右孩子都可以。

对于超过两个节点的情况，取正中间的节点作为根，然后递归求解左右子树即可。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def sortedArrayToBST(self, nums):
        """
        :type nums: List[int]
        :rtype: TreeNode
        """

        if not nums:
            return None
            
        return self.build(0, len(nums) - 1, nums)

    def build(self, left, right, nums):
        if left == right:
            return TreeNode(nums[left])
        
        if left == right - 1:
            root = TreeNode(nums[left])
            root.right = TreeNode(nums[right])
            return root

        mid = (left + right) / 2
        root = TreeNode(nums[mid])
        root.left = self.build(left, mid - 1, nums)
        root.right = self.build(mid + 1, right, nums)
        return root
```
