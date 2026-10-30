---
title: "230. 二叉搜索树中第K小的元素"
aliases: ["yiduobo的每日leetcode 230.二叉搜索树中第K小的元素"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/recursion", "题单/链表-二叉树与回溯", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/链表-二叉树与回溯/二-二叉树", "题单/LeetCode-热题-100/二叉树", "题单/面试经典-150-题/二叉搜索树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/149737432"
zhihu_id: "149737432"
zhihu_title: "yiduobo的每日leetcode 230.二叉搜索树中第K小的元素"
question_id: "230"
question: "二叉搜索树中第 K 小的元素"
problem_url: "https://leetcode.cn/problems/kth-smallest-element-in-a-bst/"
difficulty: "Medium"
created: "2020-06-20T23:53:31+08:00"
updated: "2020-06-20T23:53:31+08:00"
upvotes: 0
comments: 0
---

# 230. 二叉搜索树中第K小的元素

> **[yiduobo的每日leetcode 230.二叉搜索树中第K小的元素](https://zhuanlan.zhihu.com/p/149737432) · 知乎 · 2020-06-20 · 赞同 0**
> 力扣：[230. 二叉搜索树中第 K 小的元素](https://leetcode.cn/problems/kth-smallest-element-in-a-bst/) · Medium · 灵茶山艾府：[中序遍历（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

230.二叉搜索树中第K小的元素<https://leetcode-cn.com/problems/kth-smallest-element-in-a-bst/>

题目要求bst中第k小的元素，可以看成求bst中序遍历结果的第k个元素，于是可以参照之前94题的做法（传送门在这里[yiduobo：yiduobo的每日leetcode 94.二叉树的中序遍历](https://zhuanlan.zhihu.com/p/137080593)），修改树的结构然后一趟遍历就行了。

最后时间复杂度为O(n)。

不过，上面这种做法是一次性的。对于题目最后提到的经常插入、删除节点以及查询第k大的情况，一般做法是对于每个节点维护一下以这个节点为根节点的子树的节点总数，然后每次查询就可以从根节点出发，对比k与左子树中的节点数量来确定第k大节点在树中的位置。

计算子树节点数量的复杂度也是O(n)，但是之后每次插入、删除已经查询的复杂度都是O(h)，其中h表示树的高度，是更加优美的做法。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def kthSmallest(self, root, k):
        """
        :type root: TreeNode
        :type k: int
        :rtype: int
        """

        now = root
        while now:
            if now.left:
                rightest = now.left
                while rightest.right:
                    rightest = rightest.right
                rightest.right = now
                tmp = now.left
                now.left = None
                now = tmp

            else:
                k -= 1
                if k == 0:
                    return now.val
                now = now.right
```
