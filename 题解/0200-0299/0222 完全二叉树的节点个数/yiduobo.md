---
title: "222. 完全二叉树的节点个数"
aliases: ["yiduobo的每日leetcode 222.完全二叉树的节点个数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/148815747"
zhihu_id: "148815747"
zhihu_title: "yiduobo的每日leetcode 222.完全二叉树的节点个数"
question_id: "222"
question: "完全二叉树的节点个数"
problem_url: "https://leetcode.cn/problems/count-complete-tree-nodes/"
created: "2020-06-17T00:08:49+08:00"
updated: "2020-06-17T00:08:49+08:00"
upvotes: 0
comments: 0
---

# 222. 完全二叉树的节点个数

> **[yiduobo的每日leetcode 222.完全二叉树的节点个数](https://zhuanlan.zhihu.com/p/148815747) · 知乎 · 2020-06-17 · 赞同 0**
> 力扣：[222. 完全二叉树的节点个数](https://leetcode.cn/problems/count-complete-tree-nodes/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

222.完全二叉树的节点个数<https://leetcode-cn.com/problems/count-complete-tree-nodes/>

一个直观的做法是直接一趟遍历，统计节点个数即可，不过这样做的时间复杂度为O(n)，还存在更好的做法。

根据完全二叉树的定义，只会有最底下那一层节点可能不是满的，不妨设树的高度为h，那么第一层有1个节点，第二层有2个节点，第三层有4个节点，依次类推，第k层有2^(k - 1)个节点。那么除了最底下那一层的所有节点个数为：

1 + 2 + 4 + ... + 2^(h - 1) \= 2^h - 1

于是可以先不断往当前节点的左子树走，借此统计出树的高度以及每一层的节点个数。此时已经知道上面这些层的节点个数为2^h - 1，那么只需要想办法得到最后一层有多少个节点就行了。一个经典的做法就是二分答案，即二分最后这一层有多少个节点。显然，最后一层的节点个数一定是在1到2^(h - 1)次方之间，那么分别以1和2^(h - 1)次方作为左右边界进行二分。

观察树中节点的编号，可以发现，在第一层进入左子树，编号减去2^(h - 1)之后，将会位于1到2^(h - 2)之间，而进入右子树则是位于2^(h - 2) + 1到2^(h - 1)之间。这里减去2^(h - 1)的原理是上面层的所有节点已经用掉了1到2^(h - 1)这些编号，于是最后一层的编号一定是从2^(h - 1) + 1开始的，于是这里可以先减去2^(h - 1)进行简化。

实际上，除了第一层之外，每一层，编号都会有区间规律，第二层的左右子树分界点是2^(h - 3)，而第k层的则是2^(h - k - 1)。于是可以根据当前二分的mid，从根节点一路下来，通过编号信息判断mid这个节点的具体位置，然后找到这个节点后判断其是否存在，若存在，那么答案就位于mid到r之间，否则位于l到mid - 1之间。

以样例来说明，最后一层的节点4、5、6，减去2^(3 - 1)，编号分别是0、1、2

这一层最多可能有2^(3 - 1) \= 4个节点，于是从1到4开始二分。实际操作中，因为编号从0开始，那么就是从0到4 - 1开始进行二分。

首先二分到编号1，那么判断1是否大于等于2^(3 - 2) \= 2，发现1小于2，那么1位于根节点的左子树。接下来判断1是否大于等于2^(3 - 3) \= 1，发现是相等的，那么1位于根节点左孩子的右孩子，即对应到图中编号5的节点。验证发现该节点存在，于是调整二分范围，l变成了2。

接下来二分到编号2，此时判断2是否大于等于2^(3 - 2) \= 2，发现是相等于，于是2位于根节点的右孩子，此时注意需要将当前编号减去2^(h - 2)，表示略过左孩子的编号。减去之后就是判断编号0在根节点右子树中的位置。接下来判断0是否大于等于2^(3 - 3) \= 1，发现0小于1，于是根节点右子树中的编号0应该位于根节点右孩子的左孩子，即对应到图中编号6的节点。验证发现该节点存在，于是调整二分范围，l变成了3。

接下来二分到编号3，此时判断3是否大于等于2^(3 - 2) \= 2，发现大于，那么3位于根节点的右孩子。此时同样要减去2^(h - 2)，此时变成了判断编号1在根节点右子树中的位置。接下来判断1是否大于等于2^(3 - 3) \= 1，发现等于，于是根节点右子树中的编号1应该位于根节点右孩子的右孩子，即图中编号3的右孩子节点，为空，于是调整二分范围，r变成了2。

此时二分结束，发现最多能找到编号为2的节点，于是最后一层一共有0、1、2三个节点，加上上面两层的2^2 - 1 \= 3各节点，最后答案就是6了。

二分的范围是1到2^h，这里的h等于logn。每次二分完之后判断的复杂度同样为h，那么最终的时间复杂度就是O(logh \* h)，即O(loglogn \* logn)

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def countNodes(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """

        if not root:
            return 0

        pow_list = [1]
        now = root
        while now.left:
            now = now.left
            pow_list.append(pow_list[-1] + pow_list[-1])

        level_cnt = pow_list[-1]

        res = 0
        l = 0
        r = level_cnt - 1
        while l <= r:
            mid = (l + r) / 2
            tmp = mid
            now = root
            for index in range(len(pow_list) - 2, -1, -1):
                if tmp >= pow_list[index]:
                    now = now.right
                    tmp -= pow_list[index]
                else:
                    now = now.left

            if now:
                res = mid
                l = mid + 1
            else:
                r = mid - 1

        return res + level_cnt
```
