---
title: "501. 二叉搜索树中的众数"
aliases: ["yiduobo的每日leetcode 501.二叉搜索树中的众数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/258606906"
zhihu_id: "258606906"
zhihu_title: "yiduobo的每日leetcode 501.二叉搜索树中的众数"
question_id: "501"
question: "二叉搜索树中的众数"
problem_url: "https://leetcode.cn/problems/find-mode-in-binary-search-tree/"
created: "2020-09-23T22:22:14+08:00"
updated: "2020-09-23T22:22:14+08:00"
upvotes: 0
comments: 0
---

# 501. 二叉搜索树中的众数

> **[yiduobo的每日leetcode 501.二叉搜索树中的众数](https://zhuanlan.zhihu.com/p/258606906) · 知乎 · 2020-09-23 · 赞同 0**
> 力扣：[501. 二叉搜索树中的众数](https://leetcode.cn/problems/find-mode-in-binary-search-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

501.二叉搜索树的众数<https://leetcode-cn.com/problems/find-mode-in-binary-search-tree/>

对于常规的list求众数的问题，一般的做法是先进性排序，然后一趟扫描统计每个数出现的次数。在这个题目当中，由于二叉搜索树的中序遍历是天然有序的，那么直接对二叉搜索树的中序遍历进行一趟扫描，统计每个数出现的次数即可。

对于中序遍历，可以使用之前非递归求中序遍历（传送门在这里[yiduobo：yiduobo的每日leetcode 94.二叉树的中序遍历](https://zhuanlan.zhihu.com/p/137080593)）的做法，就相当于直接扫描了一趟中序遍历。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def findMode(self, root):
        """
        :type root: TreeNode
        :rtype: List[int]
        """

        if not root:
            return []

        now = root
        val = None
        cnt = 0
        max_cnt = 0
        res = []
        while now:
            if now.left:
                rightest = now.left
                while rightest.right:
                    rightest = rightest.right
                rightest.right = now
                tmp = now.left
                now.left = None
                now = tmp
            else:
                if val == now.val:
                    cnt += 1
                else:
                    val = now.val
                    cnt = 1
                if cnt == max_cnt:
                    res.append(val)
                elif cnt > max_cnt:
                    res = [val]
                    max_cnt = cnt
                now = now.right

        return res
```
