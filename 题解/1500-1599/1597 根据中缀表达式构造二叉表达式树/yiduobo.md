---
title: "1597. 根据中缀表达式构造二叉表达式树"
aliases: ["yiduobo的每日leetcode 1597.根据中缀表达式构造二叉表达式树"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/618625481"
zhihu_id: "618625481"
zhihu_title: "yiduobo的每日leetcode 1597.根据中缀表达式构造二叉表达式树"
question_id: "1597"
question: "根据中缀表达式构造二叉表达式树"
problem_url: "https://leetcode.cn/problems/build-binary-expression-tree-from-infix-expression/"
created: "2023-03-31T23:13:44+08:00"
updated: "2023-03-31T23:13:44+08:00"
upvotes: 1
comments: 0
---

# 1597. 根据中缀表达式构造二叉表达式树

> **[yiduobo的每日leetcode 1597.根据中缀表达式构造二叉表达式树](https://zhuanlan.zhihu.com/p/618625481) · 知乎 · 2023-03-31 · 赞同 1**
> 力扣：[1597. 根据中缀表达式构造二叉表达式树](https://leetcode.cn/problems/build-binary-expression-tree-from-infix-expression/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1597.根据中缀表达式构造二叉表示式树

[力扣](https://leetcode.cn/problems/build-binary-expression-tree-from-infix-expression/)

对于题目中给出的表达式，如果其部分前缀可以进行计算，那么就可以将其做成一颗树，使用树的根节点来代替这部分前缀参与后续的运算，因此本题就可以按照之前772题的处理方式来处理这个表达式。

[yiduobo：yiduobo的每日leetcode 772.基本计算器III](https://zhuanlan.zhihu.com/p/606392458)

不同之处在于772题需要计算出具体结果，而本题则需要将运算结果做成树的节点。

最后附上python代码：

```python
# Definition for a binary tree node.
# class Node(object):
#     def __init__(self, val=" ", left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def expTree(self, s):
        """
        :type s: str
        :rtype: Node
        """

        node_stack = []
        op_stack = []
        n = len(s)
        p = 0

        def calc():
            y, x = node_stack.pop(), node_stack.pop()
            op = op_stack.pop()

            node = Node(op)
            node.left = x
            node.right = y
            node_stack.append(node)

        while p < n:
            if '0' <= s[p] <= '9':
                start = p
                while p < n and '0' <= s[p] <= '9':
                    p += 1
                
                node = Node(s[start : p])
                node_stack.append(node)

            elif s[p] == '+' or s[p] == '-':
                while op_stack and op_stack[-1] != '(' and op_stack[-1] != ')':
                    calc()
                
                op_stack.append(s[p])
                p += 1
            
            elif s[p] == '*' or s[p] == '/':
                while op_stack and (op_stack[-1] == '*' or op_stack[-1] == '/'):
                    calc()
                
                op_stack.append(s[p])
                p += 1
            
            elif s[p] == '(':
                op_stack.append(s[p])
                p += 1
            else:
                while op_stack[-1] != '(':
                    calc()

                op_stack.pop()
                p += 1

        while op_stack:
            calc()

        return node_stack[-1]
```
