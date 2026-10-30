---
title: "1315. 祖父节点值为偶数的节点和"
aliases: ["yiduobo的每日leetcode 1315.祖父节点值为偶数的节点和"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/392849750"
zhihu_id: "392849750"
zhihu_title: "yiduobo的每日leetcode 1315.祖父节点值为偶数的节点和"
question_id: "1315"
question: "祖父节点值为偶数的节点和"
problem_url: "https://leetcode.cn/problems/sum-of-nodes-with-even-valued-grandparent/"
created: "2021-07-24T22:24:06+08:00"
updated: "2021-07-24T22:24:06+08:00"
upvotes: 1
comments: 0
---

# 1315. 祖父节点值为偶数的节点和

> **[yiduobo的每日leetcode 1315.祖父节点值为偶数的节点和](https://zhuanlan.zhihu.com/p/392849750) · 知乎 · 2021-07-24 · 赞同 1**
> 力扣：[1315. 祖父节点值为偶数的节点和](https://leetcode.cn/problems/sum-of-nodes-with-even-valued-grandparent/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1315.祖父节点值为偶数的节点和

[力扣](https://leetcode-cn.com/problems/sum-of-nodes-with-even-valued-grandparent/)

无论是dfs还是bfs，一般做法都只会保留上一轮的结果，因此在这里我才用的是对于当前节点，根据其父亲节点的奇偶性，来决定是否将当前节点左右孩子值加入到答案中。

直接从根节点开始进行dfs，每一轮的参数为当前节点now以及now的父亲的奇偶性flag。

当flag为true时，则将now.left和now.right的值加入到答案中。接下来，递归求解now.left以及now.right，这里也需要将now.val的奇偶性作为参数向下传递。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def sumEvenGrandparent(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """

        return self.dfs(root, False)

    def dfs(self, now, flag):
        res = 0
        if now.left:
            if flag:
                res += now.left.val
            res += self.dfs(now.left, now.val % 2 == 0)
        
        if now.right:
            if flag:
                res += now.right.val
            res += self.dfs(now.right, now.val % 2 == 0)
        
        return res
```
