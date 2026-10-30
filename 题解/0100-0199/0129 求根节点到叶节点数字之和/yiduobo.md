---
title: "129. 求根到叶子节点数字之和"
aliases: ["yiduobo的每日leetcode 129.求根到叶子节点数字之和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/recursion", "leetcode/binary-tree", "题单/链表-二叉树与回溯", "题单/面试经典-150-题", "题单/链表-二叉树与回溯/二-二叉树", "题单/面试经典-150-题/二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/140948286"
zhihu_id: "140948286"
zhihu_title: "yiduobo的每日leetcode 129.求根到叶子节点数字之和"
question_id: "129"
question: "求根节点到叶节点数字之和"
problem_url: "https://leetcode.cn/problems/sum-root-to-leaf-numbers/"
difficulty: "Medium"
created: "2020-05-14T22:53:35+08:00"
updated: "2020-05-14T22:53:35+08:00"
upvotes: 0
comments: 0
---

# 129. 求根到叶子节点数字之和

> **[yiduobo的每日leetcode 129.求根到叶子节点数字之和](https://zhuanlan.zhihu.com/p/140948286) · 知乎 · 2020-05-14 · 赞同 0**
> 力扣：[129. 求根节点到叶节点数字之和](https://leetcode.cn/problems/sum-root-to-leaf-numbers/) · Medium · 灵茶山艾府：[两种写法：没有返回值 / 有返回值（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

129.求根到叶子节点数字之和<https://leetcode-cn.com/problems/sum-root-to-leaf-numbers/>

对于以节点p为根的树，p能产生的价值与p所能形成的所有p到叶子节点的路径长度有关。

以样例二来说明，以节点x来代指val为x的节点：

节点4能形成三条路径，分别为4-9-5，4-9-1，4-0。其中，有两条长度为3的路径，一条长度为2的路径，那么节点4能提供的价值为

(10^(3 - 1) \* 2 + 10^(2 - 1) \* 1) \* 4 \= 840

对于两条长度为3的路径，4在这里形成了400；而对于长度为2的路径，4则是形成了40。

节点9则是形成两条路径，分别为9-5，9-1。因此，节点9能提供的价值为

(10^(2 - 1) \* 2) \* 9 \= 180

即两条长度为2的路径都形成了90。

剩下的节点5，1，0都是形成长度为1的路径，因此分别能提供

(10^(1 - 1)) \* 5 \= 5

(10^(1 - 1)) \* 1 \= 1

(10^(1 - 1)) \* 0 \= 0

最后，全部加起来就有840 + 180 + 5 + 1 + 0 \= 1026。

于是，对于所有的节点，我们分别求出其到叶子节点能形成的所有路径长度即可。我们可以从根节点出发往下dfs：

1、若当前节点为叶子节点，那么只能形成1一条长度为1的路径。

2、若不是叶子节点，那么先递归求解左右子树能形成的所有路径长度，然后在这个基础上加上1，表示将当前节点也加入路径中，就能得到当前子树根节点所能形成的所有路径长度了。

当某个节点所能形成的所有路径确定之后，其能带来的价值已经确定了，于是可以在这个过程中同时计算res。

最后附上python代码，其中level_dict的key与val表示长度为key的路径有val条：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def sumNumbers(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """

        if not root:
            return 0

        res, level_dict = self.dfs(root)
        return res

    def dfs(self, now):
        left_res = right_res = 0
        left_level = right_level = {}
        if now.left:
            left_res, left_level = self.dfs(now.left)
        if now.right:
            right_res, right_level = self.dfs(now.right)
        
        level_dict = {}
        for key, val in left_level.items():
            level_dict[key + 1] = level_dict.get(key + 1, 0) + val
        for key, val in right_level.items():
            level_dict[key + 1] = level_dict.get(key + 1, 0) + val
        
        if not level_dict:
            level_dict = {1:1}

        res = left_res + right_res
        for key, val in level_dict.items():
            res += 10 ** (key - 1) * val * now.val

        return res, level_dict
```
