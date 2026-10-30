---
title: "549. 二叉树中最长的连续序列"
aliases: ["yiduobo的每日leetcode 549.二叉树中最长的连续序列"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/601136226"
zhihu_id: "601136226"
zhihu_title: "yiduobo的每日leetcode 549.二叉树中最长的连续序列"
question_id: "549"
question: "二叉树中最长的连续序列"
problem_url: "https://leetcode.cn/problems/binary-tree-longest-consecutive-sequence-ii/"
created: "2023-01-27T02:15:15+08:00"
updated: "2023-01-27T02:15:15+08:00"
upvotes: 0
comments: 0
---

# 549. 二叉树中最长的连续序列

> **[yiduobo的每日leetcode 549.二叉树中最长的连续序列](https://zhuanlan.zhihu.com/p/601136226) · 知乎 · 2023-01-27 · 赞同 0**
> 力扣：[549. 二叉树中最长的连续序列](https://leetcode.cn/problems/binary-tree-longest-consecutive-sequence-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

549.二叉树中最长的连续序列

[力扣](https://leetcode.cn/problems/binary-tree-longest-consecutive-sequence-ii/)

题目描述中已经给出了答案的组成形式的提示，大体上可以分为三种，分别为单个父节点，子-父结构以及子-父-子结构。方便起见，在这里可以稍微扩展一下子-父-子结构的定义范围，允许子-父支链上子的部分为空，这样一来，子-父-子结构就将所有的三种可能都涵盖进去了。

接下来考虑子-父-子结构的组成。很明显，在这里应该将其拆分成父-左子以及父-右子的组合，更具体的，又可以分为左升右降和左降右升。由于左右对称，升降对称，那么在这里简单考虑一下如何求解左升链的长度，就可以推广到其他三种链了。

对于左升链，设当前求解的节点为now：

1、若now没有左孩子，那么这条左升链的长度显然为0，而父-左子结构的长度可以认为就是单个节点now的长度，也就是1

2、若now有左孩子，且now.left.val \= now.val + 1，那么就可以在以now.left为起点的升序链条头部再额外添加一个节点now，于是可以先递归求解now.left的最长升降链的长度，然后使用now.left最长升链长度加1来构成父-左子的升链结构

对上面的方法进行左右以及升降的对称调整，就可以求得其他三种的链结构了。接下来，可以将父-左子的升链结构与父-右子的降链结构组合起来，得到的就是一组子-父-子的结构。除此之外，将父-左子的降链结构与父-右子的升链结构组合也能得到一组子-父-子结构。使用这两组中较长的那一组更新答案。

最后，由于是递归求解，因此在更新完答案后还需要返回以now为起点的最长升链长度以及最长降链长度，即两种升链结构以及两种降链结构中，分别选出值较大的那一个作为函数的返回即可。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def longestConsecutive(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """

        global res
        res = 0

        def dfs(now):
            global res

            now_l_dec = now_l_inc = 1
            if now.left:
                son_l_inc, son_l_dec = dfs(now.left)
                if now.val == now.left.val + 1:
                    now_l_dec = son_l_dec + 1
                elif now.val == now.left.val - 1:
                    now_l_inc = son_l_inc + 1
            
            now_r_dec = now_r_inc = 1
            if now.right:
                son_r_inc, son_r_dec = dfs(now.right)
                if now.val == now.right.val + 1:
                    now_r_dec = son_r_dec + 1
                elif now.val == now.right.val - 1:
                    now_r_inc = son_r_inc + 1
            
            res = max(res, now_l_dec + now_r_inc - 1, now_l_inc + now_r_dec - 1)
            return max(now_l_inc, now_r_inc), max(now_l_dec, now_r_dec)
        
        dfs(root)
        return res
```
