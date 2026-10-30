---
title: "979. 在二叉树中分配硬币"
aliases: ["yiduobo的每日leetcode 979.在二叉树中分配硬币"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/recursion", "题单/链表-二叉树与回溯", "题单/贪心算法", "题单/链表-二叉树与回溯/二-二叉树", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/363056011"
zhihu_id: "363056011"
zhihu_title: "yiduobo的每日leetcode 979.在二叉树中分配硬币"
question_id: "979"
question: "在二叉树中分配硬币"
problem_url: "https://leetcode.cn/problems/distribute-coins-in-binary-tree/"
difficulty: "Medium"
rating: 1709
created: "2021-04-07T22:17:10+08:00"
updated: "2021-04-07T22:17:10+08:00"
upvotes: 0
comments: 0
---

# 979. 在二叉树中分配硬币

> **[yiduobo的每日leetcode 979.在二叉树中分配硬币](https://zhuanlan.zhihu.com/p/363056011) · 知乎 · 2021-04-07 · 赞同 0**
> 力扣：[979. 在二叉树中分配硬币](https://leetcode.cn/problems/distribute-coins-in-binary-tree/) · Medium · 灵茶山艾府：[【图解】贡献法（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

979.在二叉树中分配硬币

[力扣](https://leetcode-cn.com/problems/distribute-coins-in-binary-tree/)

题目中的每个节点都可能与其父亲节点或者孩子节点产生移动硬币的操作，如果全部计数的话就会产生重复，于是我们可以只统计一侧。我在这里统计的是每个节点需要与其孩子节点进行多少次移动操作，那么对于以now为根节点的子树而言，该子树内所有节点与其对应的孩子节点进行交换操作的总次数就是左子树交换的次数加上右子树交换的次数，再加上now与now.left以及now.right交换的次数。

对于子树中的交换次数，可以使用递归进行求解。

除此之外，还需要计算now与now.left以及now.right交换的次数。这个数量取决于两颗子树中节点的数量以及现有金币的数量。若某棵子树中节点的数量不等于金币的数量，那么就需要从now移进或者移出一些金币，这个移动的量就是子树中节点数量与金币数量的差值。

对于子树中节点数量以及金币数量，也可以通过递归进行求解。

于是现在就有了一种做法。从根节点开始向下递归，对于当前处理的节点now：

1、若now为空，那么节点数、金币数以及操作数都为0，于是返回三个0

2、若now不为空：

2-1）递归求解now.left，得到s_l、cnt_l、res_l分别表示左子树中金币数、左子树中节点数、左子树中总共需要的操作数

2-2）递归求解now.right，得到s_r、cnt_r、res_r，意义与左子树类似。

2-3）交换总次数res \= res_l + res_r，另外还需要计算now与now.left以及now.right交换的次数，于是有res +\= abs(s_l - cnt_l) + abs(s_r - cnt_r)

2-4）最后，对于以now为根节点的子树，其金币总数为s_l + s_r + now.val，节点总数为cnt_l + cnt_r + 1，操作总数为res，返回这三个值即可

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def distributeCoins(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """

        s, cnt, res = self.dfs(root)
        return res
    
    def dfs(self, now):
        if not now:
            return 0, 0, 0
        
        s_l, cnt_l, res_l = self.dfs(now.left)
        s_r, cnt_r, res_r = self.dfs(now.right)
        res = res_l + res_r
        res += abs(s_l - cnt_l) + abs(s_r - cnt_r)
        
        return s_l + s_r + now.val, cnt_l + cnt_r + 1, res
```
