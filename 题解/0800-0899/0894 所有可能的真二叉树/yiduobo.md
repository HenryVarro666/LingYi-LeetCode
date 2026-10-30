---
title: "894. 所有可能的满二叉树"
aliases: ["yiduobo的每日leetcode 894.所有可能的满二叉树"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/dynamic-programming"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/352715484"
zhihu_id: "352715484"
zhihu_title: "yiduobo的每日leetcode 894.所有可能的满二叉树"
question_id: "894"
question: "所有可能的真二叉树"
problem_url: "https://leetcode.cn/problems/all-possible-full-binary-trees/"
difficulty: "Medium"
created: "2021-02-24T22:25:44+08:00"
updated: "2021-02-24T22:25:44+08:00"
upvotes: 0
comments: 0
---

# 894. 所有可能的满二叉树

> **[yiduobo的每日leetcode 894.所有可能的满二叉树](https://zhuanlan.zhihu.com/p/352715484) · 知乎 · 2021-02-24 · 赞同 0**
> 力扣：[894. 所有可能的真二叉树](https://leetcode.cn/problems/all-possible-full-binary-trees/) · Medium · 灵茶山艾府：[动态规划（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

894.所有可能的满二叉树

[力扣](https://leetcode-cn.com/problems/all-possible-full-binary-trees/)

首先，一颗满二叉树的节点个数必然是奇数，那么对于n为偶数的情况，直接返回空list即可。

接下来，对于一颗有n个节点的满二叉树而言，设其根节点为root，那么root的左子树和右子树要么为空，要么也是满二叉树，因此我们可以从1开始到n - 2枚举左子树的节点数量k，那么右子树的节点数量就是n - k - 1，然后通过记忆化搜索递归求解k个节点的满二叉树以及n - k - 1个节点的满二叉树，最后两两进行组合。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def allPossibleFBT(self, N):
        """
        :type N: int
        :rtype: List[TreeNode]
        """

        if N % 2 == 0:
            return []

        f = {}
        return self.dfs(N, f)
    
    def dfs(self, N, f):
        if N not in f:
            if N == 1:
                f[N] = [TreeNode(0)]
            else:
                f[N] = []
                for cnt in range(1, N, 2):
                    left_list = self.dfs(cnt, f)
                    right_list = self.dfs(N - 1 - cnt, f)
                    for left in left_list:
                        for right in right_list:
                            f[N].append(TreeNode(0))
                            f[N][-1].left = left
                            f[N][-1].right = right
        
        return f[N]
```
