---
title: "951. 翻转等价二叉树"
aliases: ["yiduobo的每日leetcode 951.翻转等价二叉树"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/359681561"
zhihu_id: "359681561"
zhihu_title: "yiduobo的每日leetcode 951.翻转等价二叉树"
question_id: "951"
question: "翻转等价二叉树"
problem_url: "https://leetcode.cn/problems/flip-equivalent-binary-trees/"
created: "2021-03-24T23:30:09+08:00"
updated: "2021-03-24T23:30:09+08:00"
upvotes: 0
comments: 0
---

# 951. 翻转等价二叉树

> **[yiduobo的每日leetcode 951.翻转等价二叉树](https://zhuanlan.zhihu.com/p/359681561) · 知乎 · 2021-03-24 · 赞同 0**
> 力扣：[951. 翻转等价二叉树](https://leetcode.cn/problems/flip-equivalent-binary-trees/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

951.翻转等价二叉树

[力扣](https://leetcode-cn.com/problems/flip-equivalent-binary-trees/)

按常规编码做法来做的话是比较复杂的问题，不过如果能好好利用递归的思想，就是很直观的问题了。

我们初始求解的是以root1为根节点的树和以root2为根节点的树能否通过翻转某些节点的左右子树变成完全一致，设这个结论为f[root1, root2]。

首先，若root1的val不等于root2的val，那么无论怎么操作都不可能一致，因此可以直接返回false。

接下来，不妨设root1的两个孩子为left1和right1，root2的两个孩子为left2和right2，那么可以认为，若以left1和left2满足f[left1, left2] \= true，同时right1和right2满足f[right1, right2] \= true，那么就有f[root1, root2]为true。另外，我们也可以对root1和root2进行翻转操作，由于两树同时翻转等于没有翻转，因此只需要考察对root1进行翻转之后的情况，此时root1的左孩子为right1，右孩子为left1，那么此时应该考察的是f[right1, left2]以及f[left1, right2]是否都为true。

这样一来，f[root1, root2]就转化为了若干个子问题，可以进行递归求解了。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def flipEquiv(self, root1, root2):
        """
        :type root1: TreeNode
        :type root2: TreeNode
        :rtype: bool
        """

        return self.check(root1, root2)
    
    def check(self, root1, root2):
        if not root1:
            if not root2:
                return True
            return False
        elif not root2:
            return False
        
        if root1.val != root2.val:
            return False

        if self.check(root1.left, root2.left) and self.check(root1.right, root2.right):
            return True
        
        if self.check(root1.left, root2.right) and self.check(root1.right, root2.left):
            return True
    
        return False
```
