---
title: "437. 路径总和III"
aliases: ["yiduobo的每日leetcode 437.路径总和III"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/backtracking", "leetcode/prefix-sum", "题单/常用数据结构", "题单/链表-二叉树与回溯", "题单/LeetCode-热题-100", "题单/常用数据结构/一-前缀和", "题单/链表-二叉树与回溯/二-二叉树", "题单/LeetCode-热题-100/二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/201636615"
zhihu_id: "201636615"
zhihu_title: "yiduobo的每日leetcode 437.路径总和III"
question_id: "437"
question: "路径总和 III"
problem_url: "https://leetcode.cn/problems/path-sum-iii/"
difficulty: "Medium"
created: "2020-08-28T00:47:34+08:00"
updated: "2020-08-28T00:47:34+08:00"
upvotes: 0
comments: 0
---

# 437. 路径总和III

> **[yiduobo的每日leetcode 437.路径总和III](https://zhuanlan.zhihu.com/p/201636615) · 知乎 · 2020-08-28 · 赞同 0**
> 力扣：[437. 路径总和 III](https://leetcode.cn/problems/path-sum-iii/) · Medium · 灵茶山艾府：[做法和 560 题是一样的，附常见问题及其解答（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

437.路径总和III <https://leetcode-cn.com/problems/path-sum-iii/>

题目要求树中路径和等于sum的路径条数，乍一看还以为是树分治这类难搞的东西，不过注意到题目中的路径要求方向必须是向下的，那么对于任意节点node而言，一条合法的路径就不可能同时包含node.left以及node.right。

有了上面这个性质，就可以对于每个节点都维护一个sum_dict，其中sum_dict[value]表示以node为起点的和为value的路径一共有多少条。然后对于每个节点node，优先递归求解node.left以及node.right的sum_dict，然后通过这两个sum_dict来获取node的sum_dict。有了sum_dict之后，sum_dict[sum]就是以node为起点，路径和为sum的路径条数，而总的这个路径条数同样可以递归求解。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def pathSum(self, root, sum):
        """
        :type root: TreeNode
        :type sum: int
        :rtype: int
        """

        return self.dfs(root, sum)[1]

    def dfs(self, now, sum):
        if not now:
            return {}, 0

        left_sum, left_res = self.dfs(now.left, sum)
        right_sum, right_res = self.dfs(now.right, sum)
        sum_dict = {now.val: 1}
        for key, val in left_sum.items():
            sum_dict[key + now.val] = sum_dict.get(key + now.val, 0) + val
        for key, val in right_sum.items():
            sum_dict[key + now.val] = sum_dict.get(key + now.val, 0) + val

        return sum_dict, sum_dict.get(sum, 0) + left_res + right_res
```
