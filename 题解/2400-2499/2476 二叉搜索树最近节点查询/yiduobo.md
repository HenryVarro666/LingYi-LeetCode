---
title: "2476. 二叉搜索树最近节点查询"
aliases: ["yiduobo的每日leetcode 2476.二叉搜索树最近节点查询"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/recursion", "leetcode/binary-tree", "题单/二分算法", "题单/链表-二叉树与回溯", "题单/二分算法/一-二分查找", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/588758637"
zhihu_id: "588758637"
zhihu_title: "yiduobo的每日leetcode 2476.二叉搜索树最近节点查询"
question_id: "2476"
question: "二叉搜索树最近节点查询"
problem_url: "https://leetcode.cn/problems/closest-nodes-queries-in-a-binary-search-tree/"
difficulty: "Medium"
rating: 1597
created: "2022-12-02T22:36:31+08:00"
updated: "2022-12-02T22:36:31+08:00"
upvotes: 0
comments: 0
---

# 2476. 二叉搜索树最近节点查询

> **[yiduobo的每日leetcode 2476.二叉搜索树最近节点查询](https://zhuanlan.zhihu.com/p/588758637) · 知乎 · 2022-12-02 · 赞同 0**
> 力扣：[2476. 二叉搜索树最近节点查询](https://leetcode.cn/problems/closest-nodes-queries-in-a-binary-search-tree/) · Medium · 灵茶山艾府：[中序遍历+二分查找（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2476.二叉搜索树最近节点查询

[力扣](https://leetcode.cn/problems/closest-nodes-queries-in-a-binary-search-tree/)

注意到题目给出的是一颗二叉搜索树，那么对这棵树进行一趟中序遍历就可以得到一个按照节点值排好序的数组。接下来只需要在这个数组中二分每个查询，或者将查询排序后利用单调性求出每个询问对应的结果就行了。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def closestNodes(self, root, queries):
        """
        :type root: Optional[TreeNode]
        :type queries: List[int]
        :rtype: List[List[int]]
        """

        n = len(queries)
        res = [[-1, -1] for _ in range(n)]
        sorted_queries = sorted([q, index] for index, q in enumerate(queries))
        num_list = []

        def dfs(now):
            if now.left:
                dfs(now.left)
            num_list.append(now.val)
            if now.right:
                dfs(now.right)

        dfs(root)

        pre = -1
        p = 0

        for num in num_list:
            while p < n and sorted_queries[p][0] < num:
                res[sorted_queries[p][1]] = [pre, num]
                p += 1
            while p < n and sorted_queries[p][0] == num:
                res[sorted_queries[p][1]] = [num, num]
                p += 1
            pre = num
        
        while p < n:
            res[sorted_queries[p][1]] = [pre, -1]
            p += 1
        
        return res
```
