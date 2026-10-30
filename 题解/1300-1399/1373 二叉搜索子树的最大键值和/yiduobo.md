---
title: "1373. 二叉搜索子树的最大键值和"
aliases: ["yiduobo的每日leetcode 1373.二叉搜索子树的最大键值和"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/401217910"
zhihu_id: "401217910"
zhihu_title: "yiduobo的每日leetcode 1373.二叉搜索子树的最大键值和"
question_id: "1373"
question: "二叉搜索子树的最大键值和"
problem_url: "https://leetcode.cn/problems/maximum-sum-bst-in-binary-tree/"
difficulty: "Hard"
rating: 1914
created: "2021-08-18T22:13:37+08:00"
updated: "2021-08-18T22:13:37+08:00"
upvotes: 2
comments: 0
---

# 1373. 二叉搜索子树的最大键值和

> **[yiduobo的每日leetcode 1373.二叉搜索子树的最大键值和](https://zhuanlan.zhihu.com/p/401217910) · 知乎 · 2021-08-18 · 赞同 2**
> 力扣：[1373. 二叉搜索子树的最大键值和](https://leetcode.cn/problems/maximum-sum-bst-in-binary-tree/) · Hard · 灵茶山艾府：[后序遍历（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1373.二叉搜索子树的最大键值和

[力扣](https://leetcode-cn.com/problems/maximum-sum-bst-in-binary-tree/)

题目非常贴心地给出了二叉搜索树的定义，转化一下就是对于某个节点now，其左子树必须是二叉搜索树，且其中最大的节点值必须小于now.val；其右子树必须也是二叉搜索树，且其中最小的节点值必须大于now.val。

除此之外，我们需要求树中所有节点值的和，那么对于每个节点，我们需要求解四个数值：

1、当前子树是否为二叉搜索树

2、子树中的最大节点值

3、子树中的最小节点值

4、子树中所有节点值之和

另外，方便起见，我们也可以顺便求出当前子树中的二叉搜索子树的最大键值和。

具体实现上依然是从根节点开始进行dfs，对于当前节点now：

1、递归求解左子树，此时可以得到

l_flag：表示左子树是否为二叉搜索树

l_max：表示左子树中最大节点值

l_min：表示左子树中最小节点值

l_sum：表示左子树中所有节点值之和

l_res：表示左子树中二叉搜索子树的最大键值和

2、递归求解右子树，同样是得到上述值

r_flag：表示右子树是否为二叉搜索树

r_max：表示右子树中最大节点值

r_min：表示右子树中最小节点值

r_sum：表示右子树中所有节点值之和

r_res：表示右子树中二叉搜索子树的最大键值和

3、回到当前节点now：

ma：当前子树中的最大值，是l_max、r_max以及now.val三者中的最大值

mi：当前子树中的最小值，是l_min、r_min以及now.val三者中的最大值

s：当前子树中所有节点值之和，等于左子树中节点之和加上右子树中节点之和，再加上now.val，也就是l_sum + r_sum + now.val

flag：当前子树是否为二叉搜索树。根据定义，若l_flag以及r_flag都为真，且l_max \< now.val \< r_min，那么flag就为真，否则为假

res：当前子树中二叉搜索子树的最大键值和。首先可以初始化为max(l_res, r_res)，若flag为真，那么也应当考虑当前子树中所有节点之和s，即res \= max(res, s)

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def maxSumBST(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """

        return self.dfs(root)[2]
    
    def dfs(self, now):
        mi = ma = now.val

        if now.left is None:
            l_flag = True
            l_sum = 0
            l_res = 0
            l_min = None
            l_max = None
        else:
            l_flag, l_sum, l_res, l_min, l_max = self.dfs(now.left)
            if l_max >= now.val:
                l_flag = False
            mi = min(mi, l_min)
            ma = max(ma, l_max)

        if now.right is None:
            r_flag = True
            r_sum = 0
            r_res = 0
            r_min = None
            r_max = None
        else:
            r_flag, r_sum, r_res, r_min, r_max = self.dfs(now.right)
            if r_min <= now.val:
                r_flag = False
            mi = min(mi, r_min)
            ma = max(ma, r_max)

        if l_flag and r_flag:
            flag = True
        else:
            flag = False
        
        s = now.val + l_sum + r_sum

        res = max(l_res, r_res)
        if flag:
            res = max(res, now.val + l_sum + r_sum)
        
        return flag, s, res, mi, ma
```
