---
title: "968. 监控二叉树"
aliases: ["yiduobo的每日leetcode 968.监控二叉树"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/depth-first-search", "leetcode/dynamic-programming", "题单/链表-二叉树与回溯", "题单/动态规划", "题单/链表-二叉树与回溯/二-二叉树", "题单/动态规划/十二-树形-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/361995242"
zhihu_id: "361995242"
zhihu_title: "yiduobo的每日leetcode 968.监控二叉树"
question_id: "968"
question: "监控二叉树"
problem_url: "https://leetcode.cn/problems/binary-tree-cameras/"
difficulty: "Hard"
rating: 2124
created: "2021-04-02T23:42:05+08:00"
updated: "2021-04-02T23:42:05+08:00"
upvotes: 0
comments: 0
---

# 968. 监控二叉树

> **[yiduobo的每日leetcode 968.监控二叉树](https://zhuanlan.zhihu.com/p/361995242) · 知乎 · 2021-04-02 · 赞同 0**
> 力扣：[968. 监控二叉树](https://leetcode.cn/problems/binary-tree-cameras/) · Hard · 灵茶山艾府：[【视频】一个思路解决两种变形：一般树 / 点权树（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

968.监控二叉树

[力扣](https://leetcode-cn.com/problems/binary-tree-cameras/)

拿到题目的第一反应就是动态规划问题，不过这里的情况比较复杂，因为这里的孩子节点可以监控到父亲节点，那么在设置状态的时候必须涵盖父亲节点的状态，于是简单来说可以分成四类情况：

1、父亲节点有摄像头，当前节点也有摄像头

2、父亲节点没有摄像头，当前节点有摄像头

3、父亲节点有摄像头，当前节点没有摄像头

4、父亲节点没有摄像头，当前节点也没有摄像头

对于情况1和2而言，由于当前节点无法影响到之前的决策，因此可以归为一类，就是当前节点有摄像头。对于情况3而言，当前节点已经被父亲节点监控住了，但是对于情况4而言，需要孩子节点来监控当前节点，这两种情况需要进行区分。

于是对于一个节点，我们需要分三种情况讨论，分别设为own，fa，child，表示通过自己的摄像头监控、通过父亲节点的摄像头监控、通过孩子的摄像头监控。那么对于当前节点now：

1、首先若存在左右孩子，优先递归求解左右孩子的，得到left_own、left_fa、left_child以及right_own、right_fa、right_child

2、接下来考察now的own、fa以及child如何求解。对于now，有以下几种情况：

2-1)对于没有左右孩子的情况，当前节点的own显然为1，fa显然为0，child在这里没有意义，可以先设置为maxint

2-2)对于只有左孩子的情况：

2-2.1）own：当前节点设置了1个摄像头，其左孩子可以设置或者不设置摄像头，分别对应了left_own和left_fa，因此就有own \= 1 + min(left_own, left_fa)

2-2.2）fa：当前节点不设置摄像头，其左孩子可以设置或者不设置摄像头，分别对应了left_own和left_child，因此就有fa \= min(left_own, left_child)

2-2.3）child：当前节点不设置摄像头，其左孩子必须设置摄像头，对应的是left_own，因此就有child \= left_own

2-3)对于只有右孩子的情况：

与上面完全对称，于是有

own \= 1 + min(right_own, right_fa)

fa \= min(right_own, right_child)

child \= right_own

2-4)对于同时有左孩子和右孩子的情况：

2-4.1）own：当前节点设置了1个摄像头，其左右孩子都可以设置或者不设置摄像头，分别对应了left_own、left_fa以及right_own、right_fa，那么就有

own \= 1 + min(left_own, left_fa) + min(right_own, right_fa)

2-4.2）fa：当前节点不设置摄像头，其左右孩子都可以设置或者不设置摄像头，分别对应了left_own、left_child以及right_own,、right_child，那么就有

fa \= min(left_own, left_child) + min(right_own, right_child)

2-4.3）child：当前节点不设置摄像头，其左右孩子中至少有一方需要设置摄像头，那么分别有两个孩子都设置、左孩子设置且右孩子不设置、右孩子设置且左孩子不设置这三种情况，分别对应的是left_own + right_own、left_own + right_child、right_own + left_child，那么就有

child \= min(left_own + right_own, left_own + right_child, right_own + left_child)

从root开始进行动态规划，完成后得到的own和child中的较小值就是答案。

这种做法只需一趟dfs，应该是比较好的做法了。不过感觉这类问题也许可以通过重新选根利用树分治来解决，当然我现在已经不会这一套东西了。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def minCameraCover(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """
        
        own, fa, child = self.dfs(root)
        return min(own, child)

    def dfs(self, now):
        if now.left:
            left_own, left_fa, left_child = self.dfs(now.left)
        if now.right:
            right_own, right_fa, right_child = self.dfs(now.right)
        
        if not now.left:
            if not now.right:
                own = 1
                fa = 0
                child = 1001
            else:
                own = 1 + min(right_own, right_fa)
                fa = min(right_own, right_child)
                child = right_own
        elif not now.right:
            own = 1 + min(left_own, left_fa)
            fa = min(left_own, left_child)
            child = left_own
        else:
            own = 1 + min(left_own, left_fa) + min(right_own, right_fa)
            fa = min(left_own, left_child) + min(right_own, right_child)
            child = min(left_own + right_own, left_own + right_child, right_own + left_child)

        return own, fa, child
```
