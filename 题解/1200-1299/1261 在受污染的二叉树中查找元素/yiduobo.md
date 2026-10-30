---
title: "1261. 在受污染的二叉树中查找元素"
aliases: ["yiduobo的每日leetcode 1261.在受污染的二叉树中查找元素"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/depth-first-search", "leetcode/hash-table", "题单/链表-二叉树与回溯", "题单/位运算", "题单/链表-二叉树与回溯/二-二叉树", "题单/位运算/九-其他"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/386432798"
zhihu_id: "386432798"
zhihu_title: "yiduobo的每日leetcode 1261.在受污染的二叉树中查找元素"
question_id: "1261"
question: "在受污染的二叉树中查找元素"
problem_url: "https://leetcode.cn/problems/find-elements-in-a-contaminated-binary-tree/"
difficulty: "Medium"
rating: 1440
created: "2021-07-05T01:58:37+08:00"
updated: "2021-07-05T01:58:37+08:00"
upvotes: 0
comments: 0
---

# 1261. 在受污染的二叉树中查找元素

> **[yiduobo的每日leetcode 1261.在受污染的二叉树中查找元素](https://zhuanlan.zhihu.com/p/386432798) · 知乎 · 2021-07-05 · 赞同 0**
> 力扣：[1261. 在受污染的二叉树中查找元素](https://leetcode.cn/problems/find-elements-in-a-contaminated-binary-tree/) · Medium · 灵茶山艾府：[两种方法：哈希表/位运算（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1261.在受污染的二叉树中查找元素

[力扣](https://leetcode-cn.com/problems/find-elements-in-a-contaminated-binary-tree/)

注意到二叉树中每个节点的值都与其父节点有关，因此我们可以使用层序遍历先将整棵树还原出来，并使用一个set记录所有出现过的节点值，然后对于每次询问只需在set中查找即可。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class FindElements(object):

    def __init__(self, root):
        """
        :type root: TreeNode
        """
        self.num_set = set([0])
        root.val = 0
        q = [root]
        l = 0
        r = 1
        while l < r:
            now = q[l]
            l += 1
            if now.left:
                now.left.val = now.val * 2 + 1
                self.num_set.add(now.left.val)
                q.append(now.left)
                r += 1
            if now.right:
                now.right.val = now.val * 2 + 2
                self.num_set.add(now.right.val)
                q.append(now.right)
                r += 1

    def find(self, target):
        """
        :type target: int
        :rtype: bool
        """
        return target in self.num_set

# Your FindElements object will be instantiated and called as such:
# obj = FindElements(root)
# param_1 = obj.find(target)
```
