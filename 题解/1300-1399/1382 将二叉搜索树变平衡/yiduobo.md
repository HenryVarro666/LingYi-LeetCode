---
title: "1382. 将二叉搜索树变平衡"
aliases: ["yiduobo的每日leetcode 1382.将二叉搜索树变平衡"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/divide-and-conquer", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/402376383"
zhihu_id: "402376383"
zhihu_title: "yiduobo的每日leetcode 1382.将二叉搜索树变平衡"
question_id: "1382"
question: "将二叉搜索树变平衡"
problem_url: "https://leetcode.cn/problems/balance-a-binary-search-tree/"
difficulty: "Medium"
created: "2021-08-22T17:15:18+08:00"
updated: "2021-08-22T17:15:18+08:00"
upvotes: 1
comments: 0
---

# 1382. 将二叉搜索树变平衡

> **[yiduobo的每日leetcode 1382.将二叉搜索树变平衡](https://zhuanlan.zhihu.com/p/402376383) · 知乎 · 2021-08-22 · 赞同 1**
> 力扣：[1382. 将二叉搜索树变平衡](https://leetcode.cn/problems/balance-a-binary-search-tree/) · Medium · 灵茶山艾府：[二叉搜索树 -> 数组 -> 二叉搜索树（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1382.将二叉搜索树变平衡

<https://leetcode-cn.com/problems/balance-a-binary-search-tree/>

比较高级的做法应该是根据当前树的形态执行各种旋转操作，我在这里采用的是比较粗暴的做法。先执行一趟中序遍历，那么此时遍历结果就是按照节点值从小到大排列的。接下来我们选择正中间的节点作为新的根节点，然后使用中序遍历的前半部分递归构造左子树，后半部分则用来递归构造右子树，这样一来得到的二叉树必然是平衡的。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def balanceBST(self, root):
        """
        :type root: TreeNode
        :rtype: TreeNode
        """

        node_list = self.dfs(root)
        return self.build(node_list)

    def dfs(self, now):
        l_list = []
        r_list = []
        if now.left:
            l_list = self.dfs(now.left)
        if now.right:
            r_list = self.dfs(now.right)
        return l_list + [now] + r_list
    
    def build(self, node_list):
        mid = len(node_list) / 2
        now = node_list[mid]
        if mid > 0:
            now.left = self.build(node_list[:mid])
        else:
            now.left = None
        if mid < len(node_list) - 1:
            now.right = self.build(node_list[mid + 1:])
        else:
            now.right = None

        return now
```
