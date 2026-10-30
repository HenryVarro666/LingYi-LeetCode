---
title: "776. 拆分二叉搜索树"
aliases: ["yiduobo的每日leetcode 776.拆分二叉搜索树"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/606725915"
zhihu_id: "606725915"
zhihu_title: "yiduobo的每日leetcode 776.拆分二叉搜索树"
question_id: "776"
question: "拆分二叉搜索树"
problem_url: "https://leetcode.cn/problems/split-bst/"
created: "2023-02-16T03:20:08+08:00"
updated: "2023-02-16T03:20:08+08:00"
upvotes: 0
comments: 0
---

# 776. 拆分二叉搜索树

> **[yiduobo的每日leetcode 776.拆分二叉搜索树](https://zhuanlan.zhihu.com/p/606725915) · 知乎 · 2023-02-16 · 赞同 0**
> 力扣：[776. 拆分二叉搜索树](https://leetcode.cn/problems/split-bst/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

776.拆分二叉搜索树

[力扣](https://leetcode.cn/problems/split-bst/)

题目要求尽量保留原树的结构，那么节点now而言，若target位于其左子树中，那么应当将now.left先进行切分，然后将切分得到的右半部分作为新的now.left；同样的，若target位于其右子树中，那么应当将now.right先进行切分，然后将切分得到的左半部分作为新的now.right。

根据这个结论，就可以从根节点向下开始递归求解。对于当前处理的节点now：

1、若now为空，那么自然没有什么切分一说，直接返回两个空即可。这种情况将会在树中不存在target这个节点时出现

2、若now.val \= target，说明now就是要找的节点。此时树中值大于target的节点都位于now.right中，因此在这种情况下应该返回的就是now与now.right，同时还需要将now与now.right断开，也就是置now.right为空

3、若now.val > target，说明target位于now的左子树中。此时需要递归求解now.left得到划分出来的左右部分l与r，然后将得到的右半部分，也就是r置为新的now.left，而对于now而言，其最终的划分结果就是l与now

4、若now.val \< target，说明target位于now的右子树中。此时与情况3对称，递归求解now.right得到划分结果l和r后，将now.right置为l，然后返回now与r

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def splitBST(self, root, target):
        """
        :type root: TreeNode
        :type target: int
        :rtype: List[TreeNode]
        """

        def dfs(now):
            if now is None:
                left = None
                right = None
            elif now.val == target:
                left = now
                right = now.right
                now.right = None
            elif now.val > target:
                left, right = dfs(now.left)
                now.left = right
                right = now
            else:
                left, right = dfs(now.right)
                now.right = left
                left = now
            
            return [left, right]

        return dfs(root)
```
