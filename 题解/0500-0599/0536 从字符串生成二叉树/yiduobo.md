---
title: "536. 从字符串生成二叉树"
aliases: ["yiduobo的每日leetcode 536.从字符串生成二叉树"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/600818260"
zhihu_id: "600818260"
zhihu_title: "yiduobo的每日leetcode 536.从字符串生成二叉树"
question_id: "536"
question: "从字符串生成二叉树"
problem_url: "https://leetcode.cn/problems/construct-binary-tree-from-string/"
created: "2023-01-25T00:21:09+08:00"
updated: "2023-01-25T00:21:09+08:00"
upvotes: 0
comments: 0
---

# 536. 从字符串生成二叉树

> **[yiduobo的每日leetcode 536.从字符串生成二叉树](https://zhuanlan.zhihu.com/p/600818260) · 知乎 · 2023-01-25 · 赞同 0**
> 力扣：[536. 从字符串生成二叉树](https://leetcode.cn/problems/construct-binary-tree-from-string/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

536.从字符串生成二叉树

[力扣](https://leetcode.cn/problems/construct-binary-tree-from-string/)

观察题目给出的字符串可以发现，除根节点外，其他所有节点值的左侧必然存在一个左括号，同时左括号也不会嵌套出现，因此可以在s的两侧额外添加一对括号来适配这个规律。

从左向右进行一趟遍历，并使用一个变量now_root记录当前描述的是哪个节点。方便起见，可以先构造一个假根节点，并将now_root初始化为这个假根节点。

接下来，对于当前遍历到的字符：

1、若其为左括号，那么后方必然紧跟着一个数字。继续向后遍历完这个数字，并将其构造成树中的节点node，而node就是now_root的某个孩子。更具体的，若now_root不存在左孩子，那么node就是now_root的左孩子，也就是now_root.left \= node。若now_root存在左孩子，那么node就是now_root的右孩子，也就是now_root.right \= node。

需要注意的是，当构造好node后，字符串中接下来描述的就是以node为根节点的子树而不是之前的now_root了，因此还需要将now_root加入到栈中，然后将now_root更新为node

2、若其为右括号，那么说明对于now_root的描述到此为止了，此时应该将栈顶元素弹出并作为新的now_root。

遍历完成后，真的根节点必然是假根节点的左孩子，因此返回假根节点的左孩子作为答案即可。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def str2tree(self, s):
        """
        :type s: str
        :rtype: TreeNode
        """

        if len(s) == 0:
            return None

        now = None
        stack = []
        now_root = None
        neg_delta = 1

        phead = TreeNode(0)
        now_root = phead
        s = '(' + s + ')'
        p = 0
        n = len(s)
        while p < n:
            if s[p] == '(':
                p += 1
                neg_delta = 1
                if s[p] == '-':
                    neg_delta = -1
                    p += 1
                now = 0
                while s[p] >= '0' and s[p] <= '9':
                    now = now * 10 + int(s[p])
                    p += 1
                
                node = TreeNode(now * neg_delta)
                if now_root.left is None:
                    now_root.left = node
                else:
                    now_root.right = node
                
                stack.append(now_root)
                now_root = node
            
            elif s[p] == ')':
                now_root = stack.pop()
                p += 1
        
        return phead.left
```
