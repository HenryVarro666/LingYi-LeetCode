---
title: "1145. 二叉树着色游戏"
aliases: ["yiduobo的每日leetcode 1145.二叉树着色游戏"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/链表-二叉树与回溯", "题单/贪心算法", "题单/链表-二叉树与回溯/二-二叉树", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/377752778"
zhihu_id: "377752778"
zhihu_title: "yiduobo的每日leetcode 1145.二叉树着色游戏"
question_id: "1145"
question: "二叉树着色游戏"
problem_url: "https://leetcode.cn/problems/binary-tree-coloring-game/"
difficulty: "Medium"
rating: 1741
created: "2021-06-03T23:38:55+08:00"
updated: "2021-06-03T23:38:55+08:00"
upvotes: 0
comments: 0
---

# 1145. 二叉树着色游戏

> **[yiduobo的每日leetcode 1145.二叉树着色游戏](https://zhuanlan.zhihu.com/p/377752778) · 知乎 · 2021-06-03 · 赞同 0**
> 力扣：[1145. 二叉树着色游戏](https://leetcode.cn/problems/binary-tree-coloring-game/) · Medium · 灵茶山艾府：[没有思路？一张图秒懂！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1145.二叉树着色游戏

[力扣](https://leetcode-cn.com/problems/binary-tree-coloring-game/)

首先可以明确的一点是，选择的y必然是跟x直接相连的，因为这样一来就不会有x和y之间的部分可以让一号玩家占便宜了。那么对于给定的x，与之相连的y就可能有三种情况：

1、y是x的父亲节点，这种情况的前提是x不能是根节点。

对于这种情况而言，一号玩家可以占据以x为根的子树中的所有节点，而其他剩下的节点都归二号玩家所有。

2、y是x的左孩子，这种情况的前提是x必须有左孩子。

对于这种情况而言，二号玩家可以占据以y为根的子树中的所有节点，而其他剩下的节点都归一号玩家所有。

3、y是x的右孩子，这种情况的前提是x必须有右孩子。

与情况2类似，此时二号玩家可以占据以y为根的子树中的所有节点，而其他剩下的节点都归一号玩家所有。

注意到这里的三种情况都涉及到树中所有节点数量，因此可以递归求解以每个节点为根节点的子树中一共有多少个节点，设f[x]表示以x为根的子树中节点的个数。那么对于上面的三种情况，就有：

1、一号玩家占据了f[x]，二号玩家占据了f[root] - f[x]

2、一号玩家占据了f[root] - f[x.left]，二号玩家占据了f[x.left]

3、一号玩家占据了f[root] - f[x.right]，二号玩家占据了f[x.right]

对于给定的x，若

f[root] - f[x] > f[x]

f[x.left] > f[root] - f[x.left]

f[x.right] > f[root] - f[x.right]

这三种情况中有一种成立，那么最终答案就是true，否则就是false

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def btreeGameWinningMove(self, root, n, x):
        """
        :type root: TreeNode
        :type n: int
        :type x: int
        :rtype: bool
        """

        self.res = False
        self.dfs(root, n, x)
        return self.res
    
    def dfs(self, now, n, x):
        l_cnt = r_cnt = 0
        
        if now.left:
            l_cnt = self.dfs(now.left, n, x)
            if now.val == x and l_cnt > n / 2:
                self.res = True
        
        if now.right:
            r_cnt = self.dfs(now.right, n, x)
            if now.val == x and r_cnt > n / 2:
                self.res = True
        
        tot = l_cnt + r_cnt + 1
        if now.val == x and tot * 2 < n:
            self.res = True
        
        return tot
```
