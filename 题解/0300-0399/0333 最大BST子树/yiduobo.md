---
title: "333. 最大BST子树"
aliases: ["yiduobo的每日leetcode 333.最大BST子树"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/596644611"
zhihu_id: "596644611"
zhihu_title: "yiduobo的每日leetcode 333.最大BST子树"
question_id: "333"
question: "最大BST子树"
problem_url: "https://leetcode.cn/problems/largest-bst-subtree/"
created: "2023-01-04T23:24:28+08:00"
updated: "2023-01-04T23:24:55+08:00"
upvotes: 0
comments: 0
---

# 333. 最大BST子树

> **[yiduobo的每日leetcode 333.最大BST子树](https://zhuanlan.zhihu.com/p/596644611) · 知乎 · 2023-01-04 · 赞同 0**
> 力扣：[333. 最大BST子树](https://leetcode.cn/problems/largest-bst-subtree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

333.最大BST子树

[力扣](https://leetcode.cn/problems/largest-bst-subtree/)

题目要求找出节点数最多的bst子树，对于一颗以节点now为根节点的子树，如果其为bst，那么就需要满足：

1、如果now有左孩子，那么以now.left为根节点的子树也是bst，同时子树中最大的节点值要小于now.val

2、如果now有右孩子，那么以now.right为根节点的子树也是bst，同时子树中最小的节点值要大于now.val

根据以上两点，就可以设计一种递归算法。每次递归求解某棵子树的以下信息：

1、是否为bst

2、子树中最大的节点值

3、子树中最小的节点值

4、子树中节点的总数

那么对于以now为根节点的子树，优先递归求解now.left和now.right，得到左右子树的以上信息。那么：

1、若以now.left为根节点的子树或这以now.right为根节点的子树不是bst，那么以now为根节点的子树也不是bst。此时另外三个值就无关紧要了，直接返回False, 0, 0, 0

2、若now.left中的最大值大于等于now.val，或者now.right中的最小值小于等于now.val，那么以now为根节点的子树不是bst，此时同样返回False, 0, 0, 0

3、否则以now为根节点的子树就是bst。此时需要求解其他三个值。

子树的最小值就是左子树now.left中的最小节点值。需要注意的是，若now.left为空，那么now的最小值就是now.val自身。

同样的，子树的最大值就是右子树now.right中的最大节点值。若now.right为空，那么now的最大值就是now.val自身。

子树中的节点总数则可以通过左子树的节点总数，加上右子树的节点总数，再加上1得到。这里的1表示now自身这个节点。

此时应该使用子树中的节点总数来更新最终答案，同时返回True以及上述三个值

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def largestBSTSubtree(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """

        global res
        res = 0

        def dfs(now):
            global res

            if not now.left:
                if not now.right:
                    res = max(res, 1)
                    return True, now.val, now.val, 1
                else:
                    right_flag, right_mi, right_ma, right_size = dfs(now.right)
                    if right_flag and right_mi > now.val:
                        res = max(res, right_size + 1)
                        return True, now.val, right_ma, right_size + 1
                    else:
                        return False, 0, 0, 0

            elif not now.right:
                left_flag, left_mi, left_ma, left_size = dfs(now.left)
                if left_flag and left_ma < now.val:
                    res = max(res, left_size + 1)
                    return True, left_mi, now.val, left_size + 1
                else:
                    return False, 0, 0, 0
            
            else:
                left_flag, left_mi, left_ma, left_size = dfs(now.left)
                right_flag, right_mi, right_ma, right_size = dfs(now.right)
                if left_flag and right_flag and left_ma < now.val < right_mi:
                    res = max(res, left_size + right_size + 1)
                    return True, left_mi, right_ma, left_size + right_size + 1
                else:
                    return False, 0, 0, 0

        if root:
            dfs(root)
        return res
```
