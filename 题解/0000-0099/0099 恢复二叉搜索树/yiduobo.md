---
title: "99. 恢复二叉搜索树"
aliases: ["yiduobo的每日leetcode 99.恢复二叉搜索树"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/137573147"
zhihu_id: "137573147"
zhihu_title: "yiduobo的每日leetcode 99.恢复二叉搜索树"
question_id: "99"
question: "恢复二叉搜索树"
problem_url: "https://leetcode.cn/problems/recover-binary-search-tree/"
created: "2020-04-30T23:19:28+08:00"
updated: "2020-04-30T23:19:28+08:00"
upvotes: 0
comments: 0
---

# 99. 恢复二叉搜索树

> **[yiduobo的每日leetcode 99.恢复二叉搜索树](https://zhuanlan.zhihu.com/p/137573147) · 知乎 · 2020-04-30 · 赞同 0**
> 力扣：[99. 恢复二叉搜索树](https://leetcode.cn/problems/recover-binary-search-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

99.恢复二叉搜索树<https://leetcode-cn.com/problems/recover-binary-search-tree/>

很有意思的题目，涉及到有序数组的知识以及树的操作。

首先可以明确的是，一颗正常的二叉搜索树的中序遍历，得到的一定是一个单调递增的数组。题目中，树中有两个节点被错误的交换了，那么说明这个单调递增的数组中有两个数进行了互换。那么现在的问题就是，如何找到这两个数。

对于一个单调递增的数组，其满足：

a[0] \< ... \< a[m - 1] \< a[m] \< a[m + 1] \< ... \< a[n - 1] \< a[n] \< a[n + 1] \< ... \< a[-1]

在交换了a[m]与a[n]之后，这个单调递增的关系中就出现了两处逆序的地方，具体为：

a[0] \< ... \< a[m - 1] \< a[n]，**a[n] > a[m + 1]**

a[m + 1] \< ... \< a[n - 1]

**a[n - 1] > a[m]**，a[m] \< a[n + 1] \< ... \< a[-1]

于是，可以通过一次扫描，记录下两次逆序的位置，就能确定具体的m和n是多少了。

需要特别注意的是，还有一种特殊情况，就是m与n相邻。此时交换a[m]与a[n]之后只会出现一处逆序的位置。于是，在扫描过程中，当出现第一次逆序时，我们记录下逆序的两个位置。若还存在第二次逆序，那么将第一次逆序记录的靠后的位置替换成第二次逆序靠后的位置即可。

至此，问题已经有了一种解法。首先对二叉树进行中序遍历，然后对于中序遍历得到的数组，一趟扫描找出其中逆序的位置，就能得到最终的答案了。

题目在这里要求常数空间的做法，于是我们可以继续沿用之前利用左子树最右节点的做法（传送门在这里[yiduobo：yiduobo的每日leetcode 94.二叉树的中序遍历](https://zhuanlan.zhihu.com/p/137080593)），同时在遍历过程中记录住上一个遍历的节点，然后判断当前节点与上一个节点是否逆序来找出最终的答案。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def recoverTree(self, root):
        """
        :type root: TreeNode
        :rtype: None Do not return anything, modify root in-place instead.
        """

        first = None
        second = None
        last = None
        now = root

        while now:
            if now.left:
                rightest = now.left
                while rightest.right and rightest.right != now:
                    rightest = rightest.right
                
                if rightest.right is None:
                    rightest.right = now
                    now = now.left
                else:
                    rightest.right = None
                    if last and last.val > now.val:
                        second = now
                        if first is None:
                            first = last
                    last = now
                    now = now.right
            else:
                if last and last.val > now.val:
                    second = now
                    if first is None:
                        first = last
                last = now
                now = now.right

        tmp = first.val
        first.val = second.val
        second.val = tmp

        return root
```
