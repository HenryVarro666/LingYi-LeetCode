---
title: "1161. 最大层内元素和"
aliases: ["yiduobo的每日leetcode 1161.最大层内元素和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/breadth-first-search", "leetcode/recursion", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/378712508"
zhihu_id: "378712508"
zhihu_title: "yiduobo的每日leetcode 1161.最大层内元素和"
question_id: "1161"
question: "最大层内元素和"
problem_url: "https://leetcode.cn/problems/maximum-level-sum-of-a-binary-tree/"
difficulty: "Medium"
rating: 1250
created: "2021-06-07T21:48:01+08:00"
updated: "2021-06-07T21:48:01+08:00"
upvotes: 0
comments: 0
---

# 1161. 最大层内元素和

> **[yiduobo的每日leetcode 1161.最大层内元素和](https://zhuanlan.zhihu.com/p/378712508) · 知乎 · 2021-06-07 · 赞同 0**
> 力扣：[1161. 最大层内元素和](https://leetcode.cn/problems/maximum-level-sum-of-a-binary-tree/) · Medium · 灵茶山艾府：[两种方法：BFS / DFS（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1161.最大层内元素和

[力扣](https://leetcode-cn.com/problems/maximum-level-sum-of-a-binary-tree/)

直接按照题目要求对树进行层序遍历，对于每一层求出当前层所有元素的和，然后最其中的最大值即可。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def maxLevelSum(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """

        max_s = root.val
        res = 1
        q = [root]
        l = 0
        r = 1
        level = 0
        while l < r:
            s = 0
            level += 1
            for now in q[l : r]:
                s += now.val
                if now.left:
                    q.append(now.left)
                if now.right:
                    q.append(now.right)
            
            if s > max_s:
                max_s = s
                res = level
            
            l, r = r, len(q)
        
        return res
```
