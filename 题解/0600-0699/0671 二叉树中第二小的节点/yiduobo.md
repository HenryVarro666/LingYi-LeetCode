---
title: "671. 二叉树中第二小的节点"
aliases: ["yiduobo的每日leetcode 671.二叉树中第二小的节点"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/295102805"
zhihu_id: "295102805"
zhihu_title: "yiduobo的每日leetcode 671.二叉树中第二小的节点"
question_id: "671"
question: "二叉树中第二小的节点"
problem_url: "https://leetcode.cn/problems/second-minimum-node-in-a-binary-tree/"
created: "2020-11-15T15:49:58+08:00"
updated: "2020-11-15T15:49:58+08:00"
upvotes: 0
comments: 0
---

# 671. 二叉树中第二小的节点

> **[yiduobo的每日leetcode 671.二叉树中第二小的节点](https://zhuanlan.zhihu.com/p/295102805) · 知乎 · 2020-11-15 · 赞同 0**
> 力扣：[671. 二叉树中第二小的节点](https://leetcode.cn/problems/second-minimum-node-in-a-binary-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

671.二叉树中的第二小的节点

[力扣](https://leetcode-cn.com/problems/second-minimum-node-in-a-binary-tree/)

题目中的二叉树有两个性质，一个是任意节点的孩子个数只会是0或者2，另一个则是任意子树最小的节点必然是根节点。

对于某个子树，设其根节点为now，那么有下面几种情况：

1、若now没有左右孩子，那么这颗子树不存在第二小的节点，返回-1。

2、若now的值等于now.left的值，且now的值等于now.right的值：

此时now、now.left以及now.right的值都是树中最小的值，那么需要分别递归求解左右子树中的第二小的节点，然后取其中较小的那个。

3、若now的值等于now.left的值，但now的值不等于now.right的值：

此时now、now.left的值是树中最小的值，now.right的值是右子树中的最小值，且now.right.val > now.val。那么我们还需要递归求解左子树中的第二小的值，然后跟now.right.val进行比较，其中较小的就是树中第二小的值。

4、若now的值等于now.right的值，但now的值不等于now.left的值：

此时是情况3的镜像，只需要递归求解右子树中的第二小的值，然后跟now.left.val比较。

我们从根节点开始执行上面的求解过程，就可以得到整棵树的第二小值了。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def findSecondMinimumValue(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """

        return self.find(root)

    def find(self, now):
        if not now.left:
            return -1

        if now.left.val == now.val:
            if now.right.val == now.val:
                second_l = self.find(now.left)
                second_r = self.find(now.right)
            else:
                second_l = self.find(now.left)
                second_r = now.right.val
        else:
            second_l = now.left.val
            second_r = self.find(now.right)
        
        if second_l == -1:
            return second_r
        elif second_r == -1:
            return second_l
        else:
            return min(second_l, second_r)
```
