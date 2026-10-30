---
title: "431. 将N叉树编码为二叉树"
aliases: ["yiduobo的每日leetcode 431.将N叉树编码为二叉树"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/599561562"
zhihu_id: "599561562"
zhihu_title: "yiduobo的每日leetcode 431.将N叉树编码为二叉树"
question_id: "431"
question: "将N叉树编码为二叉树"
problem_url: "https://leetcode.cn/problems/encode-n-ary-tree-to-binary-tree/"
created: "2023-01-17T01:21:04+08:00"
updated: "2023-01-17T01:21:04+08:00"
upvotes: 0
comments: 0
---

# 431. 将N叉树编码为二叉树

> **[yiduobo的每日leetcode 431.将N叉树编码为二叉树](https://zhuanlan.zhihu.com/p/599561562) · 知乎 · 2023-01-17 · 赞同 0**
> 力扣：[431. 将N叉树编码为二叉树](https://leetcode.cn/problems/encode-n-ary-tree-to-binary-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

431.将N叉树编码为二叉树

[力扣](https://leetcode.cn/problems/encode-n-ary-tree-to-binary-tree/)

使用二叉树储存N叉树的方法应该也有不少，不过我了解到的最经典的处理方法还是孩子兄弟表示法。

具体来说，对于转化后一颗二叉树，其中某个节点node可能有两个孩子。若node有左孩子，那么node.left表示就是node在N叉树中所有孩子节点的其中一个，方便起见可以设定为children[0]。若node有右孩子，那么now.right表示的则是node在N叉树的某个兄弟节点，方便起见，在这里可以按照下标顺序，将其设定node父亲节点的children中，node的后一个节点。

对于题目描述中给出的图，如果将节点2的父亲从1改成3，就是孩子兄弟表示法的一个例子了。

接下来描述一下具体的转换过程。

首先是encode(root)。

使用root.val构造出二叉树中对应的节点res，接下来遍历root.children，并使用一个变量now记录最近处理完的孩子节点是哪一个。对于当前遍历到的孩子child，首先对其进行递归求解，得到转换后的二叉树tmp。

若此时now为空，说明当前处理的是root.children[0]。根据上面的描述，应该将其作为res的左孩子，此时应该将res.left置为tmp，然后将now置为tmp。反之，若此时now非空，那么就应该将其作为now的右孩子，此时应该将now.right置为tmp，然后将now置为tmp。

然后是decode(data)。

同样是使用data.val构造出N叉树中对应的节点root，接下来则需要想办法遍历root的孩子。根据上面的描述，root的所有孩子就应该是data.left，以及从data.left开始向下的所有右侧孩子节点，因此可以使用一个now表示当前处理的孩子节点，其初始值为data.left。接下来，若now非空，则递归求解now，得到转换后的N叉树tmp。将tmp加入到root.children中，然后将now置为now.right。不断重复此过程直到now为空。

最后附上python代码：

```python
"""
# Definition for a Node.
class Node(object):
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children
"""

"""
# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None
"""

class Codec:
    def encode(self, root):
        """Encodes an n-ary tree to a binary tree.
        :type root: Node
        :rtype: TreeNode
        """
        if not root:
            return None

        res = TreeNode(root.val)
        now = None
        for child in root.children:
            if now is None:
                res.left = self.encode(child)
                now = res.left
            else:
                now.right = self.encode(child)
                now = now.right

        return res
	
    def decode(self, data):
        """Decodes your binary tree to an n-ary tree.
        :type data: TreeNode
        :rtype: Node
        """
        if data is None:
            return None

        res = Node(data.val, [])
        now = data.left
        while now:
            res.children.append(self.decode(now))
            now = now.right
        return res
            

# Your Codec object will be instantiated and called as such:
# codec = Codec()
# codec.decode(codec.encode(root))
```
