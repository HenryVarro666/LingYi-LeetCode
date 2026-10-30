---
title: "337. 打家劫舍III"
aliases: ["yiduobo的每日leetcode 337.打家劫舍III"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/dynamic-programming", "题单/链表-二叉树与回溯", "题单/动态规划", "题单/链表-二叉树与回溯/二-二叉树", "题单/动态规划/十二-树形-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/162684037"
zhihu_id: "162684037"
zhihu_title: "yiduobo的每日leetcode 337.打家劫舍III"
question_id: "337"
question: "打家劫舍 III"
problem_url: "https://leetcode.cn/problems/house-robber-iii/"
difficulty: "Medium"
created: "2020-07-21T20:25:45+08:00"
updated: "2020-07-21T20:25:45+08:00"
upvotes: 0
comments: 0
---

# 337. 打家劫舍III

> **[yiduobo的每日leetcode 337.打家劫舍III](https://zhuanlan.zhihu.com/p/162684037) · 知乎 · 2020-07-21 · 赞同 0**
> 力扣：[337. 打家劫舍 III](https://leetcode.cn/problems/house-robber-iii/) · Medium · 灵茶山艾府：[【视频】如何思考树形 DP？附 DP 题单（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

337.打家劫舍III <https://leetcode-cn.com/problems/house-robber-iii/>

打家劫舍系列的第三弹，也是强行为了题目背景让一伙人住成树的形状，可以算是某种经典的树形动态规划。

对于某个节点，我们可以选择抢也可以选择不抢，那么我们需要分别算出抢这个点和不抢这个点时，以当前点为根节点的子树的最大收益。我们使用一个list来记录，list[0]表示抢，而list[1]表示不抢。

首先，我们递归求解左右子树抢或不抢的最大收益，分别的得到left和right。

接下来，如果我们抢该节点，那么左右孩子只能选择不抢，于是抢该节点的最大收益为now.val + left[1] + right[1]。

如果我们不抢该节点，那么左右孩子既可以抢也可以不抢，于是不抢该节点的最大收益为max(left[0], left[1]) + max(right[0], right[1])。

于是从根节点下来，一趟dfs就搞定了，最终的时间复杂度为O(n)。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def rob(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """

        return max(self.dfs(root))

    def dfs(self, now):
        if not now:
            return [0, 0]
        left = self.dfs(now.left)
        right = self.dfs(now.right)
        return [now.val + left[1] + right[1], max(left) + max(right)]
```
