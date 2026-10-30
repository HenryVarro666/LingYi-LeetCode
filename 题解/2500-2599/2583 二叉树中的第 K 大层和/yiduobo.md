---
title: "2583. 二叉树中的第K大层和"
aliases: ["yiduobo的每日leetcode 2583.二叉树中的第K大层和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/breadth-first-search", "leetcode/quickselect", "leetcode/sorting", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/642745562"
zhihu_id: "642745562"
zhihu_title: "yiduobo的每日leetcode 2583.二叉树中的第K大层和"
question_id: "2583"
question: "二叉树中的第 K 大层和"
problem_url: "https://leetcode.cn/problems/kth-largest-sum-in-a-binary-tree/"
difficulty: "Medium"
rating: 1374
created: "2023-07-11T03:36:10+08:00"
updated: "2023-07-11T03:36:10+08:00"
upvotes: 0
comments: 0
---

# 2583. 二叉树中的第K大层和

> **[yiduobo的每日leetcode 2583.二叉树中的第K大层和](https://zhuanlan.zhihu.com/p/642745562) · 知乎 · 2023-07-11 · 赞同 0**
> 力扣：[2583. 二叉树中的第 K 大层和](https://leetcode.cn/problems/kth-largest-sum-in-a-binary-tree/) · Medium · 灵茶山艾府：[BFS+排序/快速选择（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2583.二叉树中的第K大层和

[力扣](https://leetcode.cn/problems/kth-largest-sum-in-a-binary-tree/)

对于树中层和的求解，一般的处理方法是从根节点向下进行一次层序遍历，每次将同层的节点值累加起来。而对于第K大层和的求解，则可以维护一个大小为K的小顶堆，每次将层和加入到堆中，若堆中元素个数超过了K个，那么就将堆顶元素弹出。

遍历完成后，若堆的大小不到K，说明树少于K层，此时直接返回-1，反过来若堆的大小等于k，那么堆顶元素即为最终答案。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def kthLargestLevelSum(self, root, k):
        """
        :type root: Optional[TreeNode]
        :type k: int
        :rtype: int
        """

        heap = []
        q = [root]
        head, tail = 0, 1
        while head < tail:
            s = 0
            for now in q[head : tail]:
                s += now.val
                if now.left:
                    q.append(now.left)
                if now.right:
                    q.append(now.right)
            
            heapq.heappush(heap, s)
            if len(heap) > k:
                heapq.heappop(heap)
            
            head, tail = tail, len(q)

        if len(heap) < k:
            return -1
            
        return heap[0]
```
