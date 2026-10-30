---
title: "LCP 26. 导航装置"
aliases: ["yiduobo的每日leetcode LCP26.导航装置"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/573410468"
zhihu_id: "573410468"
zhihu_title: "yiduobo的每日leetcode LCP26.导航装置"
question_id: "LCP 26"
question: "导航装置"
problem_url: "https://leetcode.cn/problems/h/"
created: "2022-10-14T01:29:29+08:00"
updated: "2022-10-14T01:29:29+08:00"
upvotes: 0
comments: 0
---

# LCP 26. 导航装置

> **[yiduobo的每日leetcode LCP26.导航装置](https://zhuanlan.zhihu.com/p/573410468) · 知乎 · 2022-10-14 · 赞同 0**
> 力扣：[LCP 26. 导航装置](https://leetcode.cn/problems/h/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP26.导航装置

[力扣](https://leetcode.cn/problems/hSRGyL/)

由于题目的数据规模非常大，那么只能采用一边遍历一边构造的方法来做。

题目给出的是一颗二叉树，坏就坏在这个二叉上。对于某个节点的导航装置而言，如果在某一时刻因为二叉树的二叉分裂出了两颗子树，那么这两颗子树到这个导航装置的距离是一样的，此时就无法精确定位了。

以样例1来说明，分别考虑在1、2、3、4这四个位置，仅有一个导航装置时会出现的问题。

1、只在1有导航装置：

往下走，在2这里出现了分叉，后续的3和4无法定位

2、只在2有导航装置：

2自身的孩子3和4已经无法定位了，除此之外，2的父亲1同样无法精确定位

3、只在3有导航装置：

这种情况下，不妨将3视为树根，2为3的孩子，1和4为2的孩子。从3走到2，接下来在2这里出现了分叉，1和4无法定位

4、只有4有导航装置：

与情况3对称

可以发现，似乎出现了分叉就会导致定位出现问题，其实不然。观察样例2可以发现，虽然在1处出现了分叉，但是两侧都是单链。如果将某个叶子节点视为根节点，实际上分叉就消失了。

那么可以推断，只有当出现了度为3的节点时，需要额外的导航装置，因为如果导航装置位于该节点的某一相邻节点这一侧时，另外两个相邻节点与导航装置的距离必然相同，导致了问题。此时一个可行的解决方案就是在这两个相邻节点的一侧添加一个额外的导航装置，这样一来就不会有问题了。

接下来的问题就是导航装置应该放在什么地方。

对于当前子树，如果只需要一个导航装置，那么要么就放置在叶子节点处，要么就往上走到某个必须放置的位置。这里必须放置的位置包括遇到了度为3的节点，或者单侧的根节点。

如果需要两个或以上的导航装置，那么一定是出现了度为3的节点。此时将一个导航装置放置在该节点的某个孩子那一侧，另一个就尽量往上放，直到出现另一个度为3的节点，或者单侧的根节点。

具体实现上，可以通过dfs的返回值来确定子树的情况。返回值为0时表示当前子树中一个导航装置都没有，值为1时表示有一个导航装置，值为2时表示有两个。

那么在进行dfs的过程中：

1、若当前节点是个叶子节点，那么直接返回0

2、若当前节点仅有一侧孩子，那么直接递归求解这个孩子节点，然后原样返回这个孩子节点的返回值即可

3、若某个节点既有左孩子又有右孩子，那么说明该节点是一个度为3的节点，此时就需要判断左右子树的返回值的组成情况：

3-1)、当左右孩子都返回0时，说明此时两个孩子这边都没有导航装置，根据上面的结论需要安排一个，并返回1

3-2)、当左右孩子中有一侧为0时，说明暂时不需要新安排导航装置，但是在更上面的位置仍需要安排一个，否则必然存在部分上面的节点与返回值等于0的那一侧节点，到返回值非0的这一侧的导航装置的距离相同，因此这里也需要返回1

3-3)、当左右孩子返回值都不为0时，说明这颗子树已经不需要额外安排导航装置了，此时返回2

需要特别注意的是，由于题目是从根节点开始向下进行dfs的，那么就没有继续往上，将导航装置安排在更上面的节点这种说法了。此时可以先分别递归求解左右子树，根据返回情况决定是否需要安装一个额外的导航装置。

对于上面的这种构造方法没有想出什么严格的证明，但是二叉树的节点构成情况就那么几种，应该都是没有问题的。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None
class Solution(object):
    def navigation(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """

        self.res = 0

        def dfs(now):
            if not now.left:
                if not now.right:
                    return 0
                else:
                    return dfs(now.right)
            elif not now.right:
                return dfs(now.left)
            else:
                left_state = dfs(now.left)
                right_state = dfs(now.right)
                if left_state == 0:
                    if right_state == 0:
                        self.res += 1
                        return 1
                    else:
                        return 1
                elif right_state == 0:
                    return 1
                else:
                    return 2

        if root.left is None or root.right is None:
            if dfs(root) < 2:
                self.res += 1
        elif dfs(root.left) + dfs(root.right) < 2:
            self.res += 1
        
        return self.res
```
