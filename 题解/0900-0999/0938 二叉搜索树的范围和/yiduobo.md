---
title: "938. 二叉搜索树的范围和"
aliases: ["yiduobo的每日leetcode 938.二叉搜索树的范围和"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/depth-first-search", "leetcode/recursion", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/358187410"
zhihu_id: "358187410"
zhihu_title: "yiduobo的每日leetcode 938.二叉搜索树的范围和"
question_id: "938"
question: "二叉搜索树的范围和"
problem_url: "https://leetcode.cn/problems/range-sum-of-bst/"
difficulty: "Easy"
rating: 1335
created: "2021-03-18T22:02:41+08:00"
updated: "2021-03-18T22:02:41+08:00"
upvotes: 0
comments: 0
---

# 938. 二叉搜索树的范围和

> **[yiduobo的每日leetcode 938.二叉搜索树的范围和](https://zhuanlan.zhihu.com/p/358187410) · 知乎 · 2021-03-18 · 赞同 0**
> 力扣：[938. 二叉搜索树的范围和](https://leetcode.cn/problems/range-sum-of-bst/) · Easy · 灵茶山艾府：[简洁写法（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

938.二叉搜索树的范围和

[力扣](https://leetcode-cn.com/problems/range-sum-of-bst/)

由于二叉搜索树中的节点值满足左子树中任意节点的值小于根节点的值小于右子树中任意节点的值，那么对于求解的范围[low, high]，我们可以从根节点开始递归求解。设当前处理的节点为now，那么：

1、若now.val \< low：此时说明now以及now的左子树中所有节点的值都小于low，因此无需考虑这些节点，那么此时只需递归求解now.right

2、若now.val > high：与情况1类似，此时now以及now的右子树中的所有节点的值都大于high，因此只需递归求解now.left

3、若low \<\= now.val \<\= high，那么此时可以以now为界划分[low, high]，对于左子树我们递归求解大小处于[low, now.val]之间的节点值之和，而对于右子树则递归求解[now.val, high]之间的节点值之和，最终返回二者之和再加上now.val即可

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def rangeSumBST(self, root, low, high):
        """
        :type root: TreeNode
        :type low: int
        :type high: int
        :rtype: int
        """

        return self.sum(root, low, high)

    def sum(self, now, low, high):
        ret = 0
        if now.val < low:
            if now.right:
                ret = self.sum(now.right, low, high)
        elif now.val > high:
            if now.left:
                ret = self.sum(now.left, low, high)
        else:
            ret = now.val
            if now.left:
                ret += self.sum(now.left, low, now.val)
            if now.right:
                ret += self.sum(now.right, now.val, high)
        
        return ret
```
