---
title: "1628. 设计带解析函数的表达式树"
aliases: ["yiduobo的每日leetcode 1628.设计带解析函数的表达式树"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/618919041"
zhihu_id: "618919041"
zhihu_title: "yiduobo的每日leetcode 1628.设计带解析函数的表达式树"
question_id: "1628"
question: "设计带解析函数的表达式树"
problem_url: "https://leetcode.cn/problems/design-an-expression-tree-with-evaluate-function/"
created: "2023-04-02T19:22:56+08:00"
updated: "2023-04-02T19:22:56+08:00"
upvotes: 0
comments: 0
---

# 1628. 设计带解析函数的表达式树

> **[yiduobo的每日leetcode 1628.设计带解析函数的表达式树](https://zhuanlan.zhihu.com/p/618919041) · 知乎 · 2023-04-02 · 赞同 0**
> 力扣：[1628. 设计带解析函数的表达式树](https://leetcode.cn/problems/design-an-expression-tree-with-evaluate-function/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1628.设计带解析函数的表达式数

[力扣](https://leetcode.cn/problems/design-an-expression-tree-with-evaluate-function/)

由于题目中的表达式是后缀表示法，如果不考虑形成树而只需要最终的运算结果，就可以一趟遍历，对于当前遍历到的元素，若其是一个数值，就将其加入到栈中；若其是一个运算符，就从栈中取出顶部的两个数值，计算后将结果重新加入到栈中。

本题要求通过表达式构造出一棵树，那么就可以根据上面的计算过程，将所有的数值以及运算符都视为树中的节点。对于遍历到的运算符，就将参与运算的两个节点视为这个运算符节点的左右孩子，这样一来最终得到的就是表达式树的树根。

而对于表达式树，其计算方式则应该是递归求解左右子树，然后根据根节点的符号完成最终运算。

最后附上python代码：

```python
import abc 
from abc import ABCMeta, abstractmethod 
"""
This is the interface for the expression tree Node.
You should not remove it, and you can define some classes to implement it.
"""

class Node:
    __metaclass__ = ABCMeta
    # define your fields here

    def __init__(self, v):
        self.v = v
        self.left = None
        self.right = None

    @abstractmethod
    def evaluate(self):
        if self.v.isdigit():
            return int(self.v)
        
        left_res = self.left.evaluate()
        right_res = self.right.evaluate()

        if self.v == '+':
            return left_res + right_res
        elif self.v == '-':
            return left_res - right_res
        elif self.v == '*':
            return left_res * right_res
        else:
            return left_res / right_res

class TreeNode(Node):

    def __init__(self, v):
        super(TreeNode, self).__init__(v)
    
    def evaluate(self):
        return super(TreeNode, self).evaluate()

"""    
This is the TreeBuilder class.
You can treat it as the driver code that takes the postinfix input
and returns the expression tree represnting it as a Node.
"""

class TreeBuilder(object):
    def buildTree(self, postfix):
        """
        :type s: List[str]
        :rtype: int
        """

        stack = []
        for v in postfix:
            node = TreeNode(v)
            if node.v.isdigit():
                stack.append(node)
            else:
                node.right = stack.pop()
                node.left = stack.pop()
                stack.append(node)
        
        return stack[-1]

"""
Your TreeBuilder object will be instantiated and called as such:
obj = TreeBuilder();
expTree = obj.buildTree(postfix);
ans = expTree.evaluate();
"""
```
