---
title: "742. 二叉树最近的叶节点"
aliases: ["yiduobo的每日leetcode 742.二叉树最近的叶节点"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/605540038"
zhihu_id: "605540038"
zhihu_title: "yiduobo的每日leetcode 742.二叉树最近的叶节点"
question_id: "742"
question: "二叉树最近的叶节点"
problem_url: "https://leetcode.cn/problems/closest-leaf-in-a-binary-tree/"
created: "2023-02-11T23:43:02+08:00"
updated: "2023-02-11T23:43:02+08:00"
upvotes: 0
comments: 0
---

# 742. 二叉树最近的叶节点

> **[yiduobo的每日leetcode 742.二叉树最近的叶节点](https://zhuanlan.zhihu.com/p/605540038) · 知乎 · 2023-02-11 · 赞同 0**
> 力扣：[742. 二叉树最近的叶节点](https://leetcode.cn/problems/closest-leaf-in-a-binary-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

742.二叉树最近的叶节点

[力扣](https://leetcode.cn/problems/closest-leaf-in-a-binary-tree/)

不妨设树中值为k的节点为p，那么目标叶子节点的位置有两种可能情况：

1、目标叶子节点在以p为根节点的子树中：

这种情况下，目标叶子节点到p的距离可以通过dfs直接得到

2、目标叶子节点为以p的某个祖先节点为根节点的子树中，但不在以p为根节点的子树中：

这种情况下，设这个祖先节点为a，那么目标叶子节点到p的距离需要通过其到a的距离再加上a到p的距离得到。其中目标叶子节点到a的距离可以通过一次dfs得到，而a到p的距离同样可以在dfs的过程中得到

更进一步的，可以将情况1合并到情况2中，即目标叶子节点位于p到root的路径上的某个点a为根节点的子树中，此时的最短距离就是p到a的距离加上以目标节点到a的距离。

到了这里，就可以从根节点开始向下进行dfs，对于当前dfs到的节点now：

1、递归求解孩子节点：

若now有左孩子，那么递归求解now.left，得到l_leaf、l_dis以及l_step。

其中l_leaf和l_dis表示的是以now.left为根节点的子树中，到达now.left距离最近的叶子节点对应的val以及具体的距离，而l_step则表示值为k的节点p到达now.left的距离，若p不在now.left这颗子树中，那么l_step为空。

若now没有左孩子，那么l_leaf、l_dis、l_step都应该置为空。

同样的，若now有右孩子，那么递归求解now.right，得到r_leaf、r_dis以及r_step，否则将这三个值置为空。

2、更新now自身对应的now_leaf、now_dis以及now_step：

通过l_dis和r_dis来更新以now为根节点的子树中到达now最近的叶子节点的值now_leaf以及具体的距离now_dis。需要注意的是，若l_leaf和r_leaf都为空，说明now自身是一个叶子节点，此时的now_leaf就是now自身的值，而now_dis为0

通过l_step和r_step更新p到now的距离now_step。同样的，若now的值就为k，那么now自身就是p，此时的now_step应该为0。另外，若l_step和r_step都为空，说明p不在以now为根节点的子树中，此时的now_step也应该置为空。

3、若得到的now_step不为空，说明now是p到root的路径上的某个节点，此时就可以使用p到now的距离now_step，加上目标叶子节点到now的距离now_dis来更新最终答案了

4、最后，返回now_leaf、now_dis以及now_step给上面的节点使用

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def findClosestLeaf(self, root, k):
        """
        :type root: TreeNode
        :type k: int
        :rtype: int
        """

        global min_dis, res
        min_dis = None
        res = None
        
        def dfs(now):
            if now.left is not None:
                l_leaf, l_dis, l_step = dfs(now.left)
            else:
                l_leaf, l_dis, l_step = None, None, None

            if now.right is not None:
                r_leaf, r_dis, r_step = dfs(now.right)
            else:
                r_leaf, r_dis, r_step = None, None, None

            if l_leaf is None and r_leaf is None:
                now_leaf = now.val
                now_dis = 0
            elif l_leaf is None or (r_leaf is not None and r_dis < l_dis):
                now_leaf = r_leaf
                now_dis = r_dis + 1
            else:
                now_leaf = l_leaf
                now_dis = l_dis + 1
            
            if now.val == k:
                now_step = 0
            elif l_step is None:
                if r_step is None:
                    now_step = None
                else:
                    now_step = r_step + 1
            else:
                now_step = l_step + 1
            
            global min_dis, res
            if now_step is not None and (min_dis is None or min_dis > now_dis + now_step):
                min_dis = now_dis + now_step
                res = now_leaf
        
            return now_leaf, now_dis, now_step

        dfs(root)
        return res
```
