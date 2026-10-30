---
title: "2096. 从二叉树一个节点到另一个节点每一步的方向"
aliases: ["yiduobo的每日leetcode 2096.从二叉树一个节点到另一个节点每一步的方向"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/recursion", "leetcode/backtracking", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/521002975"
zhihu_id: "521002975"
zhihu_title: "yiduobo的每日leetcode 2096.从二叉树一个节点到另一个节点每一步的方向"
question_id: "2096"
question: "从二叉树一个节点到另一个节点每一步的方向"
problem_url: "https://leetcode.cn/problems/step-by-step-directions-from-a-binary-tree-node-to-another/"
difficulty: "Medium"
rating: 1805
created: "2022-05-27T22:13:15+08:00"
updated: "2022-05-27T22:13:15+08:00"
upvotes: 0
comments: 0
---

# 2096. 从二叉树一个节点到另一个节点每一步的方向

> **[yiduobo的每日leetcode 2096.从二叉树一个节点到另一个节点每一步的方向](https://zhuanlan.zhihu.com/p/521002975) · 知乎 · 2022-05-27 · 赞同 0**
> 力扣：[2096. 从二叉树一个节点到另一个节点每一步的方向](https://leetcode.cn/problems/step-by-step-directions-from-a-binary-tree-node-to-another/) · Medium · 灵茶山艾府：[DFS 求路径（Python/Java/C++/C/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2096.从二叉树一个节点到另一个节点每一步的方向

[力扣](https://leetcode.cn/problems/step-by-step-directions-from-a-binary-tree-node-to-another/)

题目给出一棵树和其中的两个节点s和t，要求找出从s到t的最短路径，并标记路径上每一步的方向。

为了得到最短的路径，一个自然的想法就是从s开始进行bfs，每一轮都向上或者向下走一步，直到走到t为止。这个做法有一个缺陷是题目给出的数据结构不包含当前节点的父亲节点，因此需要先额外进行一次bfs或者dfs，记录每个节点的父亲节点。

除此之外，也有一种不需要多次遍历的做法。本题的解答涉及到了一个定义，最近公共祖先。树中两个节点的最近公共祖先指的是这两个节点公共祖先当中，离根节点最远的那一个，而对于本题，最短路径就是从s向上走到s和t的最近公共祖先，再从这个最近公共祖先向下走到t。当然，这里的最近公共祖先也可能就是s或者t自身。

求解最近公共祖先一般有两种经典的做法，不过在这里只需要求解一次，那么一种可行的思路就是从根节点向下进行dfs，记录下根节点走到s的dfs序以及根节点走到t的dfs序。对于这两个dfs序，其前缀必然有相同的部分，这些相同部分表示的节点都是s和t的公共祖先，那么根据最近公共祖先的定义，二者的最近公共祖先就是这两个dfs序相同部分中的最后一个节点，不妨记为l。

接下来，从s到l的路径上全部都是向上行走，行走的步数则可以通过根节点到s的dfs中，从l开始到s这一段的长度减一得到。另一方面，从l到t的路径则可以通过从根节点到t的dfs，从l开始到t考虑两两相邻的节点对，再通过判断节点对中后面这个节点是前面节点左孩子还是右孩子确定从l走到t的行走方向。

以样例1来说明：

1、节点3和节点6的dfs分别为513和526，二者最后一个重叠的节点是5，因此3和6的最近公共祖先就是5

2、接下来，从3走到5，在dfs序中长度为3，因此需要从3向上走两步来到5，因此初始化答案为两个U

3、最后从5走到6，首先考察52，发现2是5的右孩子，因此在答案中加入R，然后再考察26，发现6是2的左孩子，因此在答案中加入L

此时就得到了最终答案UURL

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def getDirections(self, root, startValue, destValue):
        """
        :type root: Optional[TreeNode]
        :type startValue: int
        :type destValue: int
        :rtype: str
        """

        self.start_path = []
        self.dest_path = []

        def dfs(now, path):
            if now.val == startValue:
                self.start_path = path[:]
            if now.val == destValue:
                self.dest_path = path[:]

            if now.left:
                path.append(now.left)
                dfs(now.left, path)
                path.pop()
            
            if now.right:
                path.append(now.right)
                dfs(now.right, path)
                path.pop()
        
        dfs(root, [root])
        p = min(len(self.start_path), len(self.dest_path)) - 1
        while self.start_path[p] != self.dest_path[p]:
            p -= 1

        res = ['U'] * (len(self.start_path) - 1 - p)
        for index in range(p, len(self.dest_path) - 1):
            if self.dest_path[index].left == self.dest_path[index + 1]:
                res.append('L')
            else:
                res.append('R')
        
        return ''.join(res)
```
