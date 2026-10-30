---
title: "449. 序列化和反序列化二叉搜索树"
aliases: ["yiduobo的每日leetcode 449.序列化和反序列化二叉搜索树"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/211243639"
zhihu_id: "211243639"
zhihu_title: "yiduobo的每日leetcode 449.序列化和反序列化二叉搜索树"
question_id: "449"
question: "序列化和反序列化二叉搜索树"
problem_url: "https://leetcode.cn/problems/serialize-and-deserialize-bst/"
created: "2020-09-01T23:20:08+08:00"
updated: "2020-09-01T23:20:08+08:00"
upvotes: 0
comments: 0
---

# 449. 序列化和反序列化二叉搜索树

> **[yiduobo的每日leetcode 449.序列化和反序列化二叉搜索树](https://zhuanlan.zhihu.com/p/211243639) · 知乎 · 2020-09-01 · 赞同 0**
> 力扣：[449. 序列化和反序列化二叉搜索树](https://leetcode.cn/problems/serialize-and-deserialize-bst/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

449.序列化和反序列化二叉搜索树<https://leetcode-cn.com/problems/serialize-and-deserialize-bst/>

注意到这里给出的是二叉搜索树，那么有一个隐藏条件就是这棵树的中序遍历必然是单调递增的。于是我们通过一遍dfs求出这棵树的先序遍历之后，通过这个先序遍历以及隐藏的中序遍历就能还原出整棵树了。

具体来说依然是按照先序遍历逐个确定节点，而对于每个节点，设置一个上界与一个下界，若当前先序遍历位置上的值val在上界与下界之间，才生成对应的节点。初始上界与下界分别为-maxint与maxint，那么在确定根节点root之后，递归生成根节点的左子树与右子树，那么此时左子树的上界以及右子树的下界就应该变成root.val，表示root.left.val不能大于root.val，且root.right.val不能小于root.val。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Codec:

    def dfs(self, now):
        if not now:
            return []
        return [now.val] + self.dfs(now.left) + self.dfs(now.right)

    def serialize(self, root):
        """Encodes a tree to a single string.
        
        :type root: TreeNode
        :rtype: str
        """
        
        return ' '.join([str(x) for x in self.dfs(root)])

    def build(self, data, now, min_num, max_num):
        if now == len(data):
            return None, 0
        val = int(data[now])
        if val < min_num or val > max_num:
            return None, 0
        node = TreeNode(val)
        left, left_offset = self.build(data, now + 1, min_num, val)
        right, right_offset = self.build(data, now + left_offset + 1, val, max_num)
        node.left = left
        node.right = right
        return node, left_offset + right_offset + 1

    def deserialize(self, data):
        """Decodes your encoded data to tree.
        
        :type data: str
        :rtype: TreeNode
        """

        if not data:
            return None

        return self.build(data.split(' '), 0, -2147483648, 2147483647)[0]

# Your Codec object will be instantiated and called as such:
# codec = Codec()
# codec.deserialize(codec.serialize(root))
```
