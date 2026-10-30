---
title: "2385. 感染二叉树需要的总时间"
aliases: ["yiduobo的每日leetcode 2385.感染二叉树需要的总时间"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/recursion", "leetcode/hash-table", "leetcode/binary-tree", "题单/链表-二叉树与回溯", "题单/动态规划", "题单/链表-二叉树与回溯/二-二叉树", "题单/动态规划/十二-树形-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/565533284"
zhihu_id: "565533284"
zhihu_title: "yiduobo的每日leetcode 2385.感染二叉树需要的总时间"
question_id: "2385"
question: "感染二叉树需要的总时间"
problem_url: "https://leetcode.cn/problems/amount-of-time-for-binary-tree-to-be-infected/"
difficulty: "Medium"
rating: 1711
created: "2022-09-18T01:54:01+08:00"
updated: "2022-09-18T01:54:01+08:00"
upvotes: 0
comments: 0
---

# 2385. 感染二叉树需要的总时间

> **[yiduobo的每日leetcode 2385.感染二叉树需要的总时间](https://zhuanlan.zhihu.com/p/565533284) · 知乎 · 2022-09-18 · 赞同 0**
> 力扣：[2385. 感染二叉树需要的总时间](https://leetcode.cn/problems/amount-of-time-for-binary-tree-to-be-infected/) · Medium · 灵茶山艾府：[从两次遍历到一次遍历（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2385.感染二叉树需要的总时间

[力扣](https://leetcode.cn/problems/amount-of-time-for-binary-tree-to-be-infected/)

题目要求感染整颗二叉树需要的时间，实际上就是给出树中的一个节点start，问与start最远的距离是多少。对于这个问题，最直观的思路就是从start开始进行bfs直到遍历完整颗树，bfs的轮次就是最终答案。不过在这里并没有给出节点的父亲是什么，因此需要先从root开始向下遍历一次，将每个节点的父亲是什么记录下来，再从start开始进行bfs。

当然，只遍历一次的做法也是有的。可以明确的是，最终答案有两种可能：

1、从start到以start为根的子树中某个节点的距离

2、从start向上走若干步到达某个祖先节点p，然后从p出发向不是start所在的子树一侧一直走到底，这两段距离之和

第一种情况是比较好计算的，就是以start为根节点的子树的最大深度。对于第二种情况，则可以使用一个变量path_flag记录start是否位于当前子树当中。那么对于某个节点now，先递归求解左右子树now.left和now.right，分别得到now.left和now.right这两颗子树中的最大深度，以及对应的path_flag。

当now.left对应的path_flag为真时，说明start位于now.left中，那么答案就可能是从start到now，然后从now往now.right一直走到底。这里两端的距离分别是start的深度减去now的深度，再加上now.right这颗子树中的最大深度。反之，若now.right对应的path_flag为真时，那么答案就是start的深度减去now的深度，再加上now.left这颗子树中的最大深度。更新完答案后，根据now.left和now.right的最大深度以及对应的path_flag来更新now中的最大深度以及对应的path_flag并返回即可。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def amountOfTime(self, root, start):
        """
        :type root: Optional[TreeNode]
        :type start: int
        :rtype: int
        """

        self.res = 0
        self.start_depth = None

        def dfs(now, depth):
            if now.left:
                left_max_depth, left_path_flag = dfs(now.left, depth + 1)
            else:
                left_max_depth = 0
                left_path_flag = False

            if now.right:
                right_max_depth, right_path_flag = dfs(now.right, depth + 1)
            else:
                right_max_depth = 0
                right_path_flag = False
            
            max_depth = max(left_max_depth, right_max_depth)
            path_flag = False

            if now.val == start:
                self.start_depth = depth
                self.res = max_depth
                path_flag = True
            elif left_path_flag:
                self.res = max(self.res, self.start_depth - depth + right_max_depth)
                path_flag = True
            elif right_path_flag:
                self.res = max(self.res, self.start_depth - depth + left_max_depth)
                path_flag = True

            return max_depth + 1, path_flag
        
        dfs(root, 0)
        return self.res
```
