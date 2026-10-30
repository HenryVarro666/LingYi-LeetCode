---
title: "606. 根据二叉树创建字符串"
aliases: ["yiduobo的每日leetcode 606.根据二叉树创建字符串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/268909343"
zhihu_id: "268909343"
zhihu_title: "yiduobo的每日leetcode 606.根据二叉树创建字符串"
question_id: "606"
question: "根据二叉树创建字符串"
problem_url: "https://leetcode.cn/problems/construct-string-from-binary-tree/"
created: "2020-10-26T22:30:48+08:00"
updated: "2020-10-26T22:30:48+08:00"
upvotes: 0
comments: 0
---

# 606. 根据二叉树创建字符串

> **[yiduobo的每日leetcode 606.根据二叉树创建字符串](https://zhuanlan.zhihu.com/p/268909343) · 知乎 · 2020-10-26 · 赞同 0**
> 力扣：[606. 根据二叉树创建字符串](https://leetcode.cn/problems/construct-string-from-binary-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

606.根据二叉树创建字符串<https://leetcode-cn.com/problems/construct-string-from-binary-tree/>

比较基础的题目，直接按题目要求进行前序遍历。若当前节点有左子树或者右子树，那么就递归处理然后用括号将其括起来。需要注意当只有右子树时，也需要为左子树预留空的括号。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def tree2str(self, t):
        """
        :type t: TreeNode
        :rtype: str
        """

        return self.dfs(t)
    
    def dfs(self, now):
        if not now:
            return ''

        ret = str(now.val)
        if now.left:
            ret += '(' + self.dfs(now.left) + ')'
            if now.right:
                ret += '(' + self.dfs(now.right) + ')'
        elif now.right:
            ret += '()'
            ret += '(' + self.dfs(now.right) + ')'
        
        return ret
```
