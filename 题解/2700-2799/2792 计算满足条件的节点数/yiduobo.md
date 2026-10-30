---
title: "2792. 计算满足条件的节点数"
aliases: ["yiduobo的每日leetcode 2792.计算满足条件的节点数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/657051559"
zhihu_id: "657051559"
zhihu_title: "yiduobo的每日leetcode 2792.计算满足条件的节点数"
question_id: "2792"
question: "计算满足条件的节点数"
problem_url: "https://leetcode.cn/problems/count-nodes-that-are-great-enough/"
created: "2023-09-19T04:01:22+08:00"
updated: "2023-09-19T04:01:22+08:00"
upvotes: 0
comments: 0
---

# 2792. 计算满足条件的节点数

> **[yiduobo的每日leetcode 2792.计算满足条件的节点数](https://zhuanlan.zhihu.com/p/657051559) · 知乎 · 2023-09-19 · 赞同 0**
> 力扣：[2792. 计算满足条件的节点数](https://leetcode.cn/problems/count-nodes-that-are-great-enough/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2792.计算满足条件的节点数

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/count-nodes-that-are-great-enough/)

题目给出的n比较大，但是k很小，于是可以对于每颗子树都维护树中最小的k个节点值，接下来就只需检测子树的根节点的值是否大于这k个最小的节点值中最大的那一个就行了。为了高效维护这k个最小值并得到其中的最大值，就可以使用大顶堆来维护子树中最小的k个节点，此时就得到了一种基于递归的算法。

从根节点向下开始求解。对于当前处理到的节点now：

首先将now.val加入到子树对应的堆heap中，接下来，若now存在左孩子，那么递归求解now.left，得到以now.left为根节点的子树中最小的k个节点形成的堆，不妨记为left_heap。此时只需遍历left_heap，将其中的节点值加入到heap中。同样的，若now存在右孩子，那么对now.right以及right_heap也执行相同的操作。

在更新heap的过程中，若某一时刻heap的大小超过了k，那么就将堆顶元素弹出，因为该元素必然不属于最小的k个元素。

更新完成后，若now.val大于堆顶元素，那么就将答案加上1，最后不要忘了将heap返回给now的父节点使用。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def countGreatEnoughNodes(self, root, k):
        """
        :type root: Optional[TreeNode]
        :type k: int
        :rtype: int
        """

        global res
        res = 0

        def dfs(now):
            global res

            mi_list = [-now.val]
            if now.left:
                left_mi = dfs(now.left)
                for v in left_mi:
                    heapq.heappush(mi_list, v)
                    if len(mi_list) > k:
                        heapq.heappop(mi_list)
            
            if now.right:
                right_mi = dfs(now.right)
                for v in right_mi:
                    heapq.heappush(mi_list, v)
                    if len(mi_list) > k:
                        heapq.heappop(mi_list)
            
            if now.val > -mi_list[0]:
                res += 1

            return mi_list
        

        dfs(root)
        return res
```
