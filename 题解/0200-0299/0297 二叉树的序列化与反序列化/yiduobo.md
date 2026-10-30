---
title: "297. 二叉树的序列化与反序列化"
aliases: ["yiduobo的每日leetcode 297.二叉树的序列化与反序列化"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/157336402"
zhihu_id: "157336402"
zhihu_title: "yiduobo的每日leetcode 297.二叉树的序列化与反序列化"
question_id: "297"
question: "二叉树的序列化与反序列化"
problem_url: "https://leetcode.cn/problems/serialize-and-deserialize-binary-tree/"
created: "2020-07-06T21:18:34+08:00"
updated: "2020-07-06T21:18:34+08:00"
upvotes: 0
comments: 3
---

# 297. 二叉树的序列化与反序列化

> **[yiduobo的每日leetcode 297.二叉树的序列化与反序列化](https://zhuanlan.zhihu.com/p/157336402) · 知乎 · 2020-07-06 · 赞同 0**
> 力扣：[297. 二叉树的序列化与反序列化](https://leetcode.cn/problems/serialize-and-deserialize-binary-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

297.二叉树的序列化与反序列化<https://leetcode-cn.com/problems/serialize-and-deserialize-binary-tree/>

我是直接根据提示来做的。

构造时，就是对树进行一趟层次遍历，将所有节点保存起来，空节点则使用特殊字符储存。

复原时，同样是bfs的思路，依次将非空节点加入到队列q中，并使用两个指针l和r，q[l]指向当前处理的节点，data[r]则表示是当前节点的孩子节点的值。

当data[r]不为特殊字符时，构造值等于data[r]的节点并加入到队列q中，同时将q[l]的左孩子指向该节点。

对于data[r + 1]也使用同样的处理方法，区别仅在于此时为q[l]的右孩子。

在处理完一组q[l]以及data[r]、data[r + 1]之后，l往后移动一位，r则需要往后移动两位。

构造与复原都是一趟bfs，因此最终的时间复杂度为O(n)。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Codec:

    def serialize(self, root):
        """Encodes a tree to a single string.
        
        :type root: TreeNode
        :rtype: str
        """
        if not root:
            return None

        q = [root]
        l = 0
        r = 1
        while l < r:
            now = q[l]
            l += 1
            if now:
                q.append(now.left)
                q.append(now.right)
                r += 2
        
        q = [str(x.val) if x else 'N' for x in q]
        return ' '.join(q)

    def deserialize(self, data):
        """Decodes your encoded data to tree.
        
        :type data: str
        :rtype: TreeNode
        """
        if not data:
            return None

        data = data.split(' ')
        root = TreeNode(int(data[0]))
        q = [root]
        l = 0
        r = 1
        while l < len(q):
            now = q[l]
            l += 1
            if data[r] != 'N':
                now.left = TreeNode(int(data[r]))
                q.append(now.left)
            r += 1
            
            if data[r] != 'N':
                now.right = TreeNode(int(data[r]))
                q.append(now.right)
            r += 1
        
        return root

# Your Codec object will be instantiated and called as such:
# codec = Codec()
# codec.deserialize(codec.serialize(root))
```
