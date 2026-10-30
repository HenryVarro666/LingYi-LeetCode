---
title: "1008. 前序遍历构造二叉搜索树"
aliases: ["yiduobo的每日leetcode 1008.前序遍历构造二叉搜索树"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/367060224"
zhihu_id: "367060224"
zhihu_title: "yiduobo的每日leetcode 1008.前序遍历构造二叉搜索树"
question_id: "1008"
question: "前序遍历构造二叉搜索树"
problem_url: "https://leetcode.cn/problems/construct-binary-search-tree-from-preorder-traversal/"
created: "2021-04-22T22:25:38+08:00"
updated: "2021-04-22T22:25:38+08:00"
upvotes: 0
comments: 0
---

# 1008. 前序遍历构造二叉搜索树

> **[yiduobo的每日leetcode 1008.前序遍历构造二叉搜索树](https://zhuanlan.zhihu.com/p/367060224) · 知乎 · 2021-04-22 · 赞同 0**
> 力扣：[1008. 前序遍历构造二叉搜索树](https://leetcode.cn/problems/construct-binary-search-tree-from-preorder-traversal/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

1008.前序遍历构造二叉搜索树

[力扣](https://leetcode-cn.com/problems/construct-binary-search-tree-from-preorder-traversal/)

注意到这里是要构造出一颗二叉搜索树，那么就有一个隐藏条件，也就是树的中序遍历是单调递增的，那么一个直观的想法就是对前序遍历排序得到中序遍历，然后根据前序遍历和中序遍历构造出这棵树。这个做法的时间复杂度为O(nlogn)，主要是排序的复杂度较高。

回想一下常见的使用前序遍历与中序遍历构造二叉树的做法，无非也是先找出当前子树根节点在中序遍历中的位置，然后中序遍历就被分割成了两个部分，分别对应左子树和右子树，接下来递归进行求解即可。

回到本题，由于是二叉搜索树，那么我们对于某棵子树而言，其左子树中所有节点的值都小于该节点的值，而右子树中所有节点的值都大于该节点的值。设当前子树对应前序遍历的区间为[l, r]，那么根节点为l，根据前序遍历根-左-右的顺序，[l + 1, r]的排布就是前面一部分为左子树中的节点值，而剩下的部分则是右子树中的节点值，也就是说将会被val[l]分割成两个部分。设其中第一个大于val[l]的位置为next[l]，那么[l + 1, next[l] - 1]就属于左子树，而[next[l], r]则属于右子树，此时就可以继续递归求解了。

对于next的求解，是在一个数组中找到下一个大于当前数的位置的问题，可以使用经典的单调栈进行求解。

于是现在就有了一种O(n)的做法：

1、首先利用单调栈求出前序遍历中每个数下一个更大数的位置

2、接下来递归求解[0, n - 1]，设当前处理到[l, r]，那么分割点的位置就是next[l]，接下来递归求解[l, next[l] - 1]以及[next[l], r]即可。这里需要注意左子树或右子树为空的情况，可以通过确定next[l]是否存在，以及next[l]是否等于l + 1来判断。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def bstFromPreorder(self, preorder):
        """
        :type preorder: List[int]
        :rtype: TreeNode
        """

        n = len(preorder)
        stack = [n - 1]
        next = [-1]
        for index in range(n - 2, -1, -1):
            while stack and preorder[stack[-1]] < preorder[index]:
                stack.pop()
            
            if stack:
                next.append(stack[-1])
            else:
                next.append(-1)

            stack.append(index)

        next.reverse()

        return self.build(preorder, 0, n - 1, next)
    
    def build(self, preorder, l, r, next):
        now = TreeNode(preorder[l])
        if l < r:
            if next[l] > 0 and next[l] <= r:
                if next[l] - 1 > l:
                    now.left = self.build(preorder, l + 1, next[l] - 1, next)
                
                now.right = self.build(preorder, next[l], r, next)
            else:
                now.left = self.build(preorder, l + 1, r, next)
        
        return now
```
