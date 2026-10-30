---
title: "558. 四叉树交集"
aliases: ["yiduobo的每日leetcode 558.四叉树交集"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/265531402"
zhihu_id: "265531402"
zhihu_title: "yiduobo的每日leetcode 558.四叉树交集"
question_id: "558"
question: "四叉树交集"
problem_url: "https://leetcode.cn/problems/logical-or-of-two-binary-grids-represented-as-quad-trees/"
created: "2020-10-13T22:53:19+08:00"
updated: "2020-10-13T22:53:19+08:00"
upvotes: 0
comments: 0
---

# 558. 四叉树交集

> **[yiduobo的每日leetcode 558.四叉树交集](https://zhuanlan.zhihu.com/p/265531402) · 知乎 · 2020-10-13 · 赞同 0**
> 力扣：[558. 四叉树交集](https://leetcode.cn/problems/logical-or-of-two-binary-grids-represented-as-quad-trees/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

558.四叉树交集<https://leetcode-cn.com/problems/logical-or-of-two-binary-grids-represented-as-quad-trees/>

题目要求对两颗四叉树求交集，那么对于tree1中的节点A以及tree2中的节点B，若这两个节点是对应的节点，那么：

1、若A是叶子节点，且值为1：

由于1 || X \= 1，所以此时不论B怎么样，与A进行或运算之后的结果必然也全都是1

2、若A是叶子节点，且值为0：

由于0 || X \= X，所以此时不论B怎么样，与A进行或运算之后的结果必然还是B

3、若A不是叶子节点，但B是叶子节点，且值为1：

与情况1相同

4、若A不是叶子节点，但B是叶子节点，且值为0：

与情况2类似，此时的结果就是节点A

5、若A和B都不是叶子节点，那么此时需要对A和B的四个部分先递归求解，在递归计算完成后需要判断四个部分是否都是叶子节点。由于是或运算，因此最终的运算结果可能全为1，但不可能全为0，所以当四个部分都是叶子节点时，只需要判断是否都为1即可。若都为1，说明A交B的结果也是叶子节点，且值为1，否则就不是叶子节点。

最后附上python代码：

```python
"""
# Definition for a QuadTree node.
class Node(object):
    def __init__(self, val, isLeaf, topLeft, topRight, bottomLeft, bottomRight):
        self.val = val
        self.isLeaf = isLeaf
        self.topLeft = topLeft
        self.topRight = topRight
        self.bottomLeft = bottomLeft
        self.bottomRight = bottomRight
"""

class Solution(object):
    def intersect(self, quadTree1, quadTree2):
        """
        :type quadTree1: Node
        :type quadTree2: Node
        :rtype: Node
        """

        return self.dfs(quadTree1, quadTree2)

    def dfs(self, quadTree1, quadTree2):
        if quadTree1.isLeaf:
            if quadTree1.val:
                return quadTree1
            else:
                return quadTree2
        elif quadTree2.isLeaf:
            if quadTree2.val:
                return quadTree2
            else:
                return quadTree1
        else:
            ret = Node(False, False)
            ret.topLeft = self.dfs(quadTree1.topLeft, quadTree2.topLeft)
            ret.topRight = self.dfs(quadTree1.topRight, quadTree2.topRight)
            ret.bottomLeft = self.dfs(quadTree1.bottomLeft, quadTree2.bottomLeft)
            ret.bottomRight = self.dfs(quadTree1.bottomRight, quadTree2.bottomRight)
            if ret.topLeft.isLeaf and ret.topLeft.val and ret.topRight.isLeaf and ret.topRight.val and ret.bottomLeft.isLeaf and ret.bottomLeft.val and ret.bottomRight.isLeaf and ret.bottomRight.val:
                ret.topLeft = ret.topRight = ret.bottomLeft = ret.bottomRight = None
                ret.isLeaf = ret.val = True

        return ret
```
