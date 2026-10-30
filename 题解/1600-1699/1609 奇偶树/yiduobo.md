---
title: "1609. 奇偶树"
aliases: ["yiduobo的每日leetcode 1609.奇偶树"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/434567866"
zhihu_id: "434567866"
zhihu_title: "yiduobo的每日leetcode 1609.奇偶树"
question_id: "1609"
question: "奇偶树"
problem_url: "https://leetcode.cn/problems/even-odd-tree/"
created: "2021-11-17T23:58:33+08:00"
updated: "2021-11-17T23:58:33+08:00"
upvotes: 0
comments: 0
---

# 1609. 奇偶树

> **[yiduobo的每日leetcode 1609.奇偶树](https://zhuanlan.zhihu.com/p/434567866) · 知乎 · 2021-11-17 · 赞同 0**
> 力扣：[1609. 奇偶树](https://leetcode.cn/problems/even-odd-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1609.奇偶树

[力扣](https://leetcode-cn.com/problems/even-odd-tree/)

题目给出一棵树，要求判断其奇数层和偶数层是否分别满足某些条件。既然是按层来进行判断，那么很自然想到使用层序遍历来解决。直接对树进行层序遍历，然后对于每一层的节点判断奇偶性以及单调性即可。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def isEvenOddTree(self, root):
        """
        :type root: TreeNode
        :rtype: bool
        """

        q = [root]
        rest = 1
        multi = 1

        l = 0
        r = 1
        while l < r:
            new_r = r
            for index in range(l, r):
                if q[index].val % 2 != rest:
                    return False
                if index > l and (q[index].val - q[index - 1].val) * multi <= 0:
                    return False
                
                if q[index].left:
                    q.append(q[index].left)
                    new_r += 1
            
                if q[index].right:
                    q.append(q[index].right)
                    new_r += 1
                
            l, r = r, new_r
            rest = 1 - rest
            multi = -multi
        
        return True
```
