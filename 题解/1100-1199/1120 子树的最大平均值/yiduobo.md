---
title: "1120. 子树的最大平均值"
aliases: ["yiduobo的每日leetcode 1120.子树的最大平均值"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/609952384"
zhihu_id: "609952384"
zhihu_title: "yiduobo的每日leetcode 1120.子树的最大平均值"
question_id: "1120"
question: "子树的最大平均值"
problem_url: "https://leetcode.cn/problems/maximum-average-subtree/"
created: "2023-02-27T22:27:30+08:00"
updated: "2023-02-27T22:27:30+08:00"
upvotes: 0
comments: 0
---

# 1120. 子树的最大平均值

> **[yiduobo的每日leetcode 1120.子树的最大平均值](https://zhuanlan.zhihu.com/p/609952384) · 知乎 · 2023-02-27 · 赞同 0**
> 力扣：[1120. 子树的最大平均值](https://leetcode.cn/problems/maximum-average-subtree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1120.子树的最大平均值

[力扣](https://leetcode.cn/problems/maximum-average-subtree/)

题目中关于子树的定义比较特殊，包含了一整颗子树中的所有节点，那么在这里对于平均值的计算就可以通过子树中所有节点的节点值之和除以节点数量来得到。对于这两个值，则都可以通过递归得到。具体来说，子树中所有节点值之和等于根节点的值加上左右子树中所有节点值之和，而子树中的节点数量则等于左右子树的节点数量之和再加上一。

根据这个结论，就得到了一种递归的算法。从根节点开始向下递归求解，对于当前处理的节点now：

1、初始化以now为根节点的子树中的节点值s为now.val，节点数量cnt为1

2、若now存在左孩子，那么递归求解now.left，得到以now.left为根节点的子树中的节点值之和left_s以及节点数量left_cnt，并使用这两个值分别更新s以及cnt

3、与情况2类似，若now存在右孩子，那么递归求解now.right，并根据返回结果更新s以及cnt

4、使用s / cnt得到平均值并更新答案，然后返回s以及cnt供now的父节点使用

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def maximumAverageSubtree(self, root):
        """
        :type root: TreeNode
        :rtype: float
        """

        global res
        res = 0

        def dfs(now):
            s = now.val
            cnt = 1

            if now.left:
                left_s, left_cnt = dfs(now.left)
                s += left_s
                cnt += left_cnt
            
            if now.right:
                right_s, right_cnt = dfs(now.right)
                s += right_s
                cnt += right_cnt
            
            global res
            res = max(res, s * 1.0 / cnt)
            return s, cnt

        dfs(root)
        return res
```
