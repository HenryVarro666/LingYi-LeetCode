---
title: "1612. 检查两颗二叉树表达式是否等价"
aliases: ["yiduobo的每日leetcode 1612.检查两颗二叉树表达式是否等价"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/618814569"
zhihu_id: "618814569"
zhihu_title: "yiduobo的每日leetcode 1612.检查两颗二叉树表达式是否等价"
question_id: "1612"
question: "检查两颗二叉树表达式是否等价"
problem_url: "https://leetcode.cn/problems/check-if-two-expression-trees-are-equivalent/"
created: "2023-04-02T01:40:42+08:00"
updated: "2023-04-02T01:40:42+08:00"
upvotes: 0
comments: 0
---

# 1612. 检查两颗二叉树表达式是否等价

> **[yiduobo的每日leetcode 1612.检查两颗二叉树表达式是否等价](https://zhuanlan.zhihu.com/p/618814569) · 知乎 · 2023-04-02 · 赞同 0**
> 力扣：[1612. 检查两颗二叉树表达式是否等价](https://leetcode.cn/problems/check-if-two-expression-trees-are-equivalent/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1612.检查两颗二叉树表达式是否等价

[力扣](https://leetcode.cn/problems/check-if-two-expression-trees-are-equivalent/)

题目的树中只存在加法操作，换言之树中每个叶子节点的值都将被累加到最终结果中，于是可以分别遍历这两棵树，使用哈希表统计每个变量被累加的次数。得到哈希表后，只需对比这两个哈希表是否相同即可。

最后附上python代码：

```python
# Definition for a binary tree node.
# class Node(object):
#     def __init__(self, val=" ", left=None, right=None):
#         self.val = val
#         self.left = None
#         self.right = None
class Solution(object):
    def checkEquivalence(self, root1, root2):
        """
        :type root1: Node
        :type root2: Node
        :rtype: bool
        """

        cnt = {}
        head, tail = 0, 1

        q = [root1]
        while head < tail:
            now = q[head]
            head += 1
            if now.val == '+':
                q.append(now.left)
                q.append(now.right)
                tail += 2
            else:
                cnt[now.val] = cnt.get(now.val, 0) + 1

        head, tail = 0, 1
        q = [root2]
        while head < tail:
            now = q[head]
            head += 1
            if now.val == '+':
                q.append(now.left)
                q.append(now.right)
                tail += 2
            elif cnt.get(now.val, 0) == 0:
                return False
            else:
                cnt[now.val] -= 1

        for v in cnt.values():
            if v > 0:
                return False
        
        return True
```
