---
title: "1430. 判定给定的序列是否是二叉树从根到叶的路径"
aliases: ["yiduobo的每日leetcode 1430.判定给定的序列是否是二叉树从根到叶的路径"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/616545829"
zhihu_id: "616545829"
zhihu_title: "yiduobo的每日leetcode 1430.判定给定的序列是否是二叉树从根到叶的路径"
question_id: "1430"
question: "判断给定的序列是否是二叉树从根到叶的路径"
problem_url: "https://leetcode.cn/problems/check-if-a-string-is-a-valid-sequence-from-root-to-leaves-path-in-a-binary-tree/"
difficulty: "Medium"
created: "2023-03-24T00:56:23+08:00"
updated: "2023-03-24T00:56:23+08:00"
upvotes: 0
comments: 0
---

# 1430. 判定给定的序列是否是二叉树从根到叶的路径

> **[yiduobo的每日leetcode 1430.判定给定的序列是否是二叉树从根到叶的路径](https://zhuanlan.zhihu.com/p/616545829) · 知乎 · 2023-03-24 · 赞同 0**
> 力扣：[1430. 判断给定的序列是否是二叉树从根到叶的路径](https://leetcode.cn/problems/check-if-a-string-is-a-valid-sequence-from-root-to-leaves-path-in-a-binary-tree/) · Medium · 灵茶山艾府：[简洁写法](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1430.判定给定的序列是否是二叉树从根到叶的路径

[力扣](https://leetcode.cn/problems/check-if-a-string-is-a-valid-sequence-from-root-to-leaves-path-in-a-binary-tree/)

搜索回溯的题目。从根节点开始向下进行搜索回溯，每一轮都根据当前arr中对应的值以及当前节点左右孩子的值决定往哪个节点继续向下搜索回溯。需要注意的是，题目中左右节点的值可能相同。

值得一提的是，题目的数据规模不小，在这个数据规模下很容易构造出完全无法处理的case，不过在这里也没有什么更好的处理方法了。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def isValidSequence(self, root, arr):
        """
        :type root: TreeNode
        :type arr: List[int]
        :rtype: bool
        """

        def dfs(level, now):
            if level == len(arr):
                if not now.left and not now.right:
                    return True
                else:
                    return False
            
            if now.left and now.left.val == arr[level]:
                if dfs(level + 1, now.left):
                    return True
            
            if now.right and now.right.val == arr[level]:
                if dfs(level + 1, now.right):
                    return True
            
            return False
        
        if arr[0] != root.val:
            return False

        return dfs(1, root)
```
