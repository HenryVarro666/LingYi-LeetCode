---
title: "1485. 克隆含随机指针的二叉树"
aliases: ["yiduobo的每日leetcode 1485.克隆含随机指针的二叉树"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/616819305"
zhihu_id: "616819305"
zhihu_title: "yiduobo的每日leetcode 1485.克隆含随机指针的二叉树"
question_id: "1485"
question: "克隆含随机指针的二叉树"
problem_url: "https://leetcode.cn/problems/clone-binary-tree-with-random-pointer/"
created: "2023-03-24T23:16:57+08:00"
updated: "2023-03-24T23:16:57+08:00"
upvotes: 0
comments: 0
---

# 1485. 克隆含随机指针的二叉树

> **[yiduobo的每日leetcode 1485.克隆含随机指针的二叉树](https://zhuanlan.zhihu.com/p/616819305) · 知乎 · 2023-03-24 · 赞同 0**
> 力扣：[1485. 克隆含随机指针的二叉树](https://leetcode.cn/problems/clone-binary-tree-with-random-pointer/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1485.克隆含随机指针的二叉树

[力扣](https://leetcode.cn/problems/clone-binary-tree-with-random-pointer/)

对于这类克隆数据结构的问题，一种常见的处理方法是利用哈希表建立原节点到克隆节点的映射，然后遍历原数据结构，在过程中就可以利用原数据结构节点间的关系以及哈希表建立起克隆节点间的关系。另一方面，对于本题中的random指针，同样可以按照上面的方法，将每个节点对应的克隆节点的random指向该节点指向的random的克隆节点，也就是当node1->random为node2时，需要将node1的克隆节点的random指向node2的克隆节点。

在具体实现上，我在这里采用的是从根节点开始向下进行bfs，建立克隆节点以及其中的原始父子关系。接下来再遍历所有节点建立random关系。

最后附上python代码：

```python
# Definition for Node.
# class Node(object):
#     def __init__(self, val=0, left=None, right=None, random=None):
#         self.val = val
#         self.left = left
#         self.right = right
#         self.random = random

class Solution(object):
    def copyRandomBinaryTree(self, root):
        """
        :type root: Node
        :rtype: NodeCopy
        """

        if not root:
            return None

        mapping = {}
        q = [root]
        mapping[root] = NodeCopy(root.val)

        head, tail = 0, 1
        while head < tail:
            now = q[head]
            head += 1
            if now.left:
                q.append(now.left)
                tail += 1
                mapping[now.left] = NodeCopy(now.left.val)
                mapping[now].left = mapping[now.left]
            
            if now.right:
                q.append(now.right)
                tail += 1
                mapping[now.right] = NodeCopy(now.right.val)
                mapping[now].right = mapping[now.right]

        for node in mapping:
            if node.random:
                mapping[node].random = mapping[node.random]

        return mapping[root]
```
