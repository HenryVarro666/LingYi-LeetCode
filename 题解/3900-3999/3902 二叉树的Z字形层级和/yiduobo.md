---
title: "3902. 二叉树的Z字形层级和"
aliases: ["yiduobo的每日leetcode 3902.二叉树的Z字形层级和"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2028635660043526968"
zhihu_id: "2028635660043526968"
zhihu_title: "yiduobo的每日leetcode 3902.二叉树的Z字形层级和"
question_id: "3902"
question: "二叉树的Z字形层级和"
problem_url: "https://leetcode.cn/problems/zigzag-level-sum-of-binary-tree/"
created: "2026-04-18T00:59:03+08:00"
updated: "2026-04-18T00:59:03+08:00"
upvotes: 0
comments: 0
---

# 3902. 二叉树的Z字形层级和

> **[yiduobo的每日leetcode 3902.二叉树的Z字形层级和](https://zhuanlan.zhihu.com/p/2028635660043526968) · 知乎 · 2026-04-18 · 赞同 0**
> 力扣：[3902. 二叉树的Z字形层级和](https://leetcode.cn/problems/zigzag-level-sum-of-binary-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3902.二叉树的Z字形层级和

<https://leetcode.cn/problems/zigzag-level-sum-of-binary-tree/>

题目给出一颗二叉树的根节点root。

现在要求按照Z字形逐层遍历二叉树。在奇数层中(从1开始)，需要从左到右遍历，而在偶数层中，则需要从右到左遍历。在遍历过程中，需要计算每一层节点的节点值之和。

另外，在奇数层中，对于首个没有左孩子的节点，该节点以及本层中后续遍历到的节点对应的节点值不能被累加到层和中；而在偶数层中，对于首个没有右孩子的节点，该节点以及本层中后续遍历到的节点对应的节点值不能被累加到层和中。

要求返回层和的数组。

按照题目要求，使用bfs进行层序遍历计算层和即可。

由于是z字形遍历，在具体实现上可以从队列尾到队列头进行遍历，这样做的理由是偶数层需要逆序遍历，所以从后往前，而在偶数层从后往前遍历的过程中，下一层的节点也是从后往前加入到队列中的，所以如果要正常遍历，那么在这个反的队列中应该再反一次，所以每一层都是从后往前遍历。需要注意的是，奇数层是先将左孩子入队再将右孩子入队，形成正常的序，而偶数层因为是反序，所以要先将右孩子入队再将左孩子入队。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def zigzagLevelSum(self, root):
        """
        :type root: Optional[TreeNode]
        :rtype: List[int]
        """
        
        q = [root]
        head, tail = 0, 1
        level = 1
        res = []

        while head < tail:
            flag = True
            res.append(0)

            for index in range(tail - 1, head - 1, -1):
                now = q[index]
                if level % 2 == 1:
                    if now.left:
                        q.append(now.left)
                    else:
                        flag = False
                    if now.right:
                        q.append(now.right)
                else:
                    if now.right:
                        q.append(now.right)
                    else:
                        flag = False
                    if now.left:
                        q.append(now.left)

                if flag:
                    res[-1] += now.val
            
            head, tail = tail, len(q)
            level += 1
    
        return res
```
