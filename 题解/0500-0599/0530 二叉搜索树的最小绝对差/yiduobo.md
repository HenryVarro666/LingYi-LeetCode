---
title: "530. 二叉搜索树的最小绝对差"
aliases: ["yiduobo的每日leetcode 530.二叉搜索树的最小绝对差"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/depth-first-search", "leetcode/recursion", "题单/链表-二叉树与回溯", "题单/面试经典-150-题", "题单/链表-二叉树与回溯/二-二叉树", "题单/面试经典-150-题/二叉搜索树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/261167895"
zhihu_id: "261167895"
zhihu_title: "yiduobo的每日leetcode 530.二叉搜索树的最小绝对差"
question_id: "530"
question: "二叉搜索树的最小绝对差"
problem_url: "https://leetcode.cn/problems/minimum-absolute-difference-in-bst/"
difficulty: "Easy"
rating: 1303
created: "2020-10-04T23:17:43+08:00"
updated: "2020-10-04T23:17:43+08:00"
upvotes: 0
comments: 0
---

# 530. 二叉搜索树的最小绝对差

> **[yiduobo的每日leetcode 530.二叉搜索树的最小绝对差](https://zhuanlan.zhihu.com/p/261167895) · 知乎 · 2020-10-04 · 赞同 0**
> 力扣：[530. 二叉搜索树的最小绝对差](https://leetcode.cn/problems/minimum-absolute-difference-in-bst/) · Easy · 灵茶山艾府：[中序遍历，简洁写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

530.二叉搜索树的最小绝对差<https://leetcode-cn.com/problems/minimum-absolute-difference-in-bst/>

对于一个数组来说，如果要求其中任意两个数差的绝对值的最小值，常见的做法就是将其排序，然后从头到尾一趟扫描，每次比较相邻的两个数。

在这里，bst的中序遍历是天然有序的，因此我们只需要求出其中序遍历，比较中序遍历中所有相邻的数来求解答案即可。

我在这里使用的是之前94题修改树结构的做法（传送门在这里[yiduobo：yiduobo的每日leetcode 94.二叉树的中序遍历](https://zhuanlan.zhihu.com/p/137080593)），这样做可以省下储存中序遍历的空间，使得最终空间复杂度为O(1)。

最后附上python代码：

```
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def getMinimumDifference(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """

        last = None
        res = None

        now = root
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
                if last is not None:
                    if res is None or abs(now.val - last) < res:
                        res = abs(now.val - last)
                last = now.val
                now = now.right

        return res
```
