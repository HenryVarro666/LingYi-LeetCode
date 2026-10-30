---
title: "1740. 找到二叉树中的距离"
aliases: ["yiduobo的每日leetcode 1740.找到二叉树中的距离"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/620572146"
zhihu_id: "620572146"
zhihu_title: "yiduobo的每日leetcode 1740.找到二叉树中的距离"
question_id: "1740"
question: "找到二叉树中的距离"
problem_url: "https://leetcode.cn/problems/find-distance-in-a-binary-tree/"
created: "2023-04-09T18:53:29+08:00"
updated: "2023-04-09T18:53:29+08:00"
upvotes: 0
comments: 0
---

# 1740. 找到二叉树中的距离

> **[yiduobo的每日leetcode 1740.找到二叉树中的距离](https://zhuanlan.zhihu.com/p/620572146) · 知乎 · 2023-04-09 · 赞同 0**
> 力扣：[1740. 找到二叉树中的距离](https://leetcode.cn/problems/find-distance-in-a-binary-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1740.找到二叉树中的距离

[力扣](https://leetcode.cn/problems/find-distance-in-a-binary-tree/)

又是LCA的问题，不过本题计算的是两个目标节点到LCA的距离之和。

由于节点的数据结构中并不存在父亲节点的信息，那么在这里就可以参考之前的1644题，通过自顶向下的一次dfs来寻找这个LCA。

[yiduobo：yiduobo的每日leetcode 1644.二叉树的最近公共祖先II](https://zhuanlan.zhihu.com/p/619223621)

与之前不同的是，在这里需要计算距离之和，那么在这里维护的不再是子树中目标节点的数量，而是到目标节点的距离。在dfs过程中，若某个节点的左右子树返回的到目标节点的距离都不为空，或者其中一方不为空同时当前节点是p或q之一，那么该节点就是LCA，使用返回的距离计算最终答案即可。

另外根据样例3可以发现本题中存在p和q相同的情况，对于这种特殊情况直接返回0即可。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def findDistance(self, root, p, q):
        """
        :type root: TreeNode
        :type p: int
        :type q: int
        :rtype: int
        """

        if p == q:
            return 0
        
        global res
        res = 0

        def dfs(now):
            global res

            if res == 0 and now.left:
                l_dis = dfs(now.left)
            else:
                l_dis = None
            
            if res == 0 and now.right:
                r_dis = dfs(now.right)
            else:
                r_dis = None

            if l_dis is not None:
                l_dis += 1
            if r_dis is not None:
                r_dis += 1

            if l_dis or r_dis:
                if l_dis and r_dis:
                    if res == 0:
                        res = l_dis + r_dis
                    return None

                elif now.val == p or now.val == q:
                    if res == 0:
                        if l_dis:
                            res = l_dis
                        else:
                            res = r_dis
                    
                    return None
                
                else:
                    if l_dis:
                        return l_dis
                    else:
                        return r_dis
            
            elif now.val == p or now.val == q:
                return 0

            return None

        dfs(root)
        return res
```
