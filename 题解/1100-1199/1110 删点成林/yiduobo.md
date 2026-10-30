---
title: "1110. 删点成林"
aliases: ["yiduobo的每日leetcode 1110.删点成林"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/recursion", "leetcode/hash-table", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/374942361"
zhihu_id: "374942361"
zhihu_title: "yiduobo的每日leetcode 1110.删点成林"
question_id: "1110"
question: "删点成林"
problem_url: "https://leetcode.cn/problems/delete-nodes-and-return-forest/"
difficulty: "Medium"
rating: 1511
created: "2021-05-24T22:43:21+08:00"
updated: "2021-05-24T22:43:21+08:00"
upvotes: 0
comments: 0
---

# 1110. 删点成林

> **[yiduobo的每日leetcode 1110.删点成林](https://zhuanlan.zhihu.com/p/374942361) · 知乎 · 2021-05-24 · 赞同 0**
> 力扣：[1110. 删点成林](https://leetcode.cn/problems/delete-nodes-and-return-forest/) · Medium · 灵茶山艾府：[简洁写法！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1110.删点成林

[力扣](https://leetcode-cn.com/problems/delete-nodes-and-return-forest/)

我们先来看看森林里面的树的特点。首先，树的根节点必然不能是to_delete当中的点。接下来，树的根节点要么是整棵树的根节点，要么其父亲节点被删除了。

那么我们可以从根节点开始向下进行dfs，并携带一个标记new_root_flag表示当前节点是否需要作为森林中的树的根节点。那么对于当前节点now：

1、若now.val出现在to_delete当中，那么说明now需要被删除，使用一个表示del_flag记录下来。

2、若now有左孩子，那么递归计算now.left，此时now.left配套的new_root_flag就是del_flag。递归计算完毕后，若now.left需要被移除，那么置now.left为空。

3、若now有右孩子，按情况2的做法如法炮制。

4、最后，若del_flag为假，且new_root_flag为真，那么now就是森林中的树的根节点，需要将now加入到答案当中。

处理完毕now之后，还需要返回del_flag，用来给now的父亲节点判断是否需要置now这一侧的孩子为空。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def delNodes(self, root, to_delete):
        """
        :type root: TreeNode
        :type to_delete: List[int]
        :rtype: List[TreeNode]
        """

        del_set = set(to_delete)
        self.res = []
        self.dfs(root, del_set, True)
        return self.res

    def dfs(self, now, del_set, new_root_flag):
        if now.val in del_set:
            del_flag = True
        else:
            del_flag = False

        if now.left and self.dfs(now.left, del_set, del_flag):
            now.left = None
        if now.right and self.dfs(now.right, del_set, del_flag):
            now.right = None
        
        if not del_flag and new_root_flag:
            self.res.append(now)
        
        return del_flag
```
