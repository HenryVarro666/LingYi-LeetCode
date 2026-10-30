---
title: "101. 对称二叉树"
aliases: ["yiduobo的每日leetcode 101.对称二叉树"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/depth-first-search", "leetcode/recursion", "题单/链表-二叉树与回溯", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/链表-二叉树与回溯/二-二叉树", "题单/LeetCode-热题-100/二叉树", "题单/面试经典-150-题/二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/137722389"
zhihu_id: "137722389"
zhihu_title: "yiduobo的每日leetcode 101.对称二叉树"
question_id: "101"
question: "对称二叉树"
problem_url: "https://leetcode.cn/problems/symmetric-tree/"
difficulty: "Easy"
created: "2020-05-01T23:56:49+08:00"
updated: "2020-05-01T23:56:49+08:00"
upvotes: 0
comments: 0
---

# 101. 对称二叉树

> **[yiduobo的每日leetcode 101.对称二叉树](https://zhuanlan.zhihu.com/p/137722389) · 知乎 · 2020-05-01 · 赞同 0**
> 力扣：[101. 对称二叉树](https://leetcode.cn/problems/symmetric-tree/) · Easy · 灵茶山艾府：[【视频】如何灵活运用递归？附思考题（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

101.对称二叉树<https://leetcode-cn.com/problems/symmetric-tree/>

树操作的题目。

---

递归的做法：

对于一棵树，如果是对称的，那么沿着根节点竖着画一条线下来，可以发现左子树和右子树应该是根据这条线轴对称的。于是我们可以递归地判断，即对于两棵树a和b，如果a.val \=\= b.val，且a.left与b.right对称、a.right与b.left对称，那么就认为a和b对称。

---

迭代的做法：

可以先对树进行层次遍历，若一棵树是对称的，那么对于同一层次中遍历得到的序列，其一定是一个长度为偶数的回文序列。于是依次遍历每一层，然后判断当前层的遍历结果是否满足回文性质即可。

例如样例一中，层次遍历应该是：

[1], [2, 2], [3, 4, 4, 3]

然后依次判断每一层是否为回文即可。

我在这里并没有使用上面这种做法，而是沿用了迭代的思路，即先判断根节点，然后判断两棵树的左右子树是否对称。具体来说其实就是将递归的做法改成队列，即依次将a.left，b.right，a.right，b.left入队，然后每次取队首前两位判断val是否相等，同时将队首元素的left与right按同样的方式入队即可。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def isSymmetric(self, root):
        """
        :type root: TreeNode
        :rtype: bool
        """

        import Queue

        q = Queue.Queue()

        q.put(root)
        q.put(root)

        while not q.empty():
            node1 = q.get()
            node2 = q.get()
            if node1 is None:
                if node2 is None:
                    continue
                else:
                    return False
            else:
                if node2 is None:
                    return False
                else:
                    if node1.val != node2.val:
                        return False
                    else:
                        q.put(node1.left)
                        q.put(node2.right)
                        q.put(node1.right)
                        q.put(node2.left)
        
        return True
```
