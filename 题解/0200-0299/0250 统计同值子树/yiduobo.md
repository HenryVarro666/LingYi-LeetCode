---
title: "250. 统计同值子树"
aliases: ["yiduobo的每日leetcode 250.统计同值子树"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/592448251"
zhihu_id: "592448251"
zhihu_title: "yiduobo的每日leetcode 250.统计同值子树"
question_id: "250"
question: "统计同值子树"
problem_url: "https://leetcode.cn/problems/count-univalue-subtrees/"
created: "2022-12-17T04:50:24+08:00"
updated: "2022-12-17T04:50:24+08:00"
upvotes: 0
comments: 0
---

# 250. 统计同值子树

> **[yiduobo的每日leetcode 250.统计同值子树](https://zhuanlan.zhihu.com/p/592448251) · 知乎 · 2022-12-17 · 赞同 0**
> 力扣：[250. 统计同值子树](https://leetcode.cn/problems/count-univalue-subtrees/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

250.统计同值子树

[力扣](https://leetcode.cn/problems/count-univalue-subtrees/)

对于以节点now为根节点的子树来说，如果其所有节点是同值的，那么其左右子树必然也是同值的，且这棵树根节点的值now.val必然等于now.left.val以及now.right.val，于是可以从root开始向下dfs。对于当前处理的子树now，先递归求解now.left和now.right，并使用两个变量left_flag和right_flag分别记录左右子树是否为同值子树。若now.val与now.left.val和now.right.val相等，且left_flag和right_flag均为真，那么说明以now为根节点的子树就是同值子树，此时更新答案然后返回true，否则返回false。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def countUnivalSubtrees(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """

        if not root:
            return 0

        global res
        res = 0

        def dfs(now):
            left_flag = right_flag = True
            if now.left:
                left_flag = dfs(now.left)
            if now.right:
                right_flag = dfs(now.right)

            if now.left and (now.val != now.left.val or not left_flag):
                return False
            if now.right and (now.val != now.right.val or not right_flag):
                return False
            
            global res
            res += 1
            return True
        
        dfs(root)
        return res
```
