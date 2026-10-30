---
title: "173. 二叉搜索树迭代器"
aliases: ["yiduobo的每日leetcode 173.二叉搜索树迭代器"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/144934893"
zhihu_id: "144934893"
zhihu_title: "yiduobo的每日leetcode 173.二叉搜索树迭代器"
question_id: "173"
question: "二叉搜索树迭代器"
problem_url: "https://leetcode.cn/problems/binary-search-tree-iterator/"
created: "2020-05-31T22:13:55+08:00"
updated: "2020-05-31T22:13:55+08:00"
upvotes: 0
comments: 4
---

# 173. 二叉搜索树迭代器

> **[yiduobo的每日leetcode 173.二叉搜索树迭代器](https://zhuanlan.zhihu.com/p/144934893) · 知乎 · 2020-05-31 · 赞同 0**
> 力扣：[173. 二叉搜索树迭代器](https://leetcode.cn/problems/binary-search-tree-iterator/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

173.二叉搜索树迭代器<https://leetcode-cn.com/problems/binary-search-tree-iterator/>

题目本质上就是要我们做一次树的前序遍历，但是如果在初始化时就完成前序遍历并储存起来的话，空间复杂度达到了O(n)，不符合题目的要求。

另一种想法是模拟前序遍历的过程，每次将当前节点入栈并往当前节点的左子树递归计算，当找不到左子树时说明到达了最左侧节点，即前序遍历的第一个节点。接下来回溯上来之后进入右子树，然后在右子树中再按同样的方法找到最左侧节点并重复上述过程即可。

我们在这里找到最左侧节点时就可以先停下来，等待next指令。遇到next指令后弹出栈顶节点，然后执行回溯操作，即在栈顶节点的右子树中寻找最左侧节点并将沿途节点入栈。由于树的高度为h，因此栈的规模也就是最多就是h，满足了空间复杂度的要求。另外每个节点只会入栈一次，出栈一次，因此时间复杂度均摊下来就是O(1)。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class BSTIterator(object):

    def __init__(self, root):
        """
        :type root: TreeNode
        """

        self.stack = []
        while root:
            self.stack.append(root)
            root = root.left

    def next(self):
        """
        @return the next smallest number
        :rtype: int
        """

        res = self.stack.pop()
        now = res.right
        while now:
            self.stack.append(now)
            now = now.left

        return res.val

    def hasNext(self):
        """
        @return whether we have a next smallest number
        :rtype: bool
        """

        if self.stack:
            return True

        return False

# Your BSTIterator object will be instantiated and called as such:
# obj = BSTIterator(root)
# param_1 = obj.next()
# param_2 = obj.hasNext()
```
