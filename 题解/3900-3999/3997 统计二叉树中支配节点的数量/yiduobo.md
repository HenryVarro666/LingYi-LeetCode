---
title: "3997. 统计二叉树中支配节点的数量"
aliases: ["yiduobo的每日leetcode 3997.统计二叉树中支配节点的数量"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/recursion", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2063374405825254804"
zhihu_id: "2063374405825254804"
zhihu_title: "yiduobo的每日leetcode 3997.统计二叉树中支配节点的数量"
question_id: "3997"
question: "统计二叉树中支配节点的数量"
problem_url: "https://leetcode.cn/problems/count-dominant-nodes-in-a-binary-tree/"
difficulty: "Medium"
rating: 1427
created: "2026-07-22T21:31:49+08:00"
updated: "2026-07-22T21:31:50+08:00"
upvotes: 1
comments: 0
---

# 3997. 统计二叉树中支配节点的数量

> **[yiduobo的每日leetcode 3997.统计二叉树中支配节点的数量](https://zhuanlan.zhihu.com/p/2063374405825254804) · 知乎 · 2026-07-22 · 赞同 1**
> 力扣：[3997. 统计二叉树中支配节点的数量](https://leetcode.cn/problems/count-dominant-nodes-in-a-binary-tree/) · Medium · 灵茶山艾府：[自底向上 DFS（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3997.统计二叉树中支配节点的数量

<https://leetcode.cn/problems/count-dominant-nodes-in-a-binary-tree/description/>

题目给出一颗完全二叉树的根节点root。

若某个节点x的值等于以x为根的子数中所有节点的最大值，那么就称x为支配节点。

问数中支配节点的数量。

题目中关于支配节点的定义设计到子树中所有节点的最大值，那么一个自然的想法就是自顶向下递归求解。

具体来说，对于当前处理的节点now：

1、若now有左孩子，则递归求解now.left，记录两个返回值left_res以及left_v，分别表示以now.left为根节点的子数中支配节点的数量，以及这颗子树中所有节点的最大值。若now没有左孩子，则设置left_res和left_v为0

2、对于now的右孩子按相同的方法处理，得到right_res以及right_v

3、此时就可以初始化以now为根节点的子数中的支配节点数目res \= left_res + right_res。接下来，若now的值大于等于max(left_v, right_v)，说明now也是支配节点，此时就应该返回res + 1以及now的值，反之，则应该返回res以及max(left_v, right_v)

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def countDominantNodes(self, root):
        """
        :type root: Optional[TreeNode]
        :rtype: int
        """
        

        def dfs(now):
            if now.left:
                left_res, left_v = dfs(now.left)
            else:
                left_res, left_v = 0, 0
            
            if now.right:
                right_res, right_v = dfs(now.right)
            else:
                right_res, right_v = 0, 0

            res = left_res + right_res
            ma = max(left_v, right_v)
            if now.val >= ma:
                return res + 1, now.val
            else:
                return res, ma
        
        return dfs(root)[0]
```
