---
title: "272. 最接近的二叉搜索树值II"
aliases: ["yiduobo的每日leetcode 272.最接近的二叉搜索树值II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/594293845"
zhihu_id: "594293845"
zhihu_title: "yiduobo的每日leetcode 272.最接近的二叉搜索树值II"
question_id: "272"
question: "最接近的二叉搜索树值II"
problem_url: "https://leetcode.cn/problems/closest-binary-search-tree-value-ii/"
created: "2022-12-26T00:58:03+08:00"
updated: "2022-12-26T00:58:03+08:00"
upvotes: 2
comments: 0
---

# 272. 最接近的二叉搜索树值II

> **[yiduobo的每日leetcode 272.最接近的二叉搜索树值II](https://zhuanlan.zhihu.com/p/594293845) · 知乎 · 2022-12-26 · 赞同 2**
> 力扣：[272. 最接近的二叉搜索树值II](https://leetcode.cn/problems/closest-binary-search-tree-value-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

272.最接近的二叉搜索树值II

[力扣](https://leetcode.cn/problems/closest-binary-search-tree-value-ii/)

之前270题的强化版，本题要求找出最近target的k个值。最直观的想法就是先执行一次中序遍历，然后利用排序或者快速选择找出最接近target的top k个值，不过在这里还存在更好的做法。

直接套用270题的做法，从根节点向下寻找最接近target的节点值，并将遍历到的值记录下来。可以发现，随着深度的加深，所有小于target的值都是单调递增的，而所有大于target的值都是单调递减的，因此可以使用两个栈mi和ma分别储存在查找过程中遇到的比target小以及比target大的数。

接下来，最接近target数应该是mi栈顶和ma栈顶这二者中里target更近的那一个。另外，在确定了这个最接近的数之后，则需要将下一个最接近的数加入到对应的栈顶。

具体来说，当mi的栈顶最接近target时，需要将小于mi栈顶的最大值加入到mi中，也就是以mi左孩子为根节点的子树的最右侧的节点。从mi左孩子往这个节点遍历时，需要将路径上的节点也加入到mi中。

需要注意的是，有一种可能的情况是当前mi栈顶元素并没有左孩子，那么此时无需执行其他额外操作，因为mi新的栈顶元素就是要找的小于原mi栈顶的最大值。

同样的，当ma的栈顶最接近target时，则需要将大于ma栈顶的最小值加入到ma中，也就是以ma右孩子为根节点的子树的最左侧的节点。从ma右孩子往这个节点遍历时，同样需要将路径上的节点加入到ma中。

重复上面的过程一共k轮，就可以找出最接近target的k个值了。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def closestKValues(self, root, target, k):
        """
        :type root: TreeNode
        :type target: float
        :type k: int
        :rtype: List[int]
        """

        mi = []
        ma = []
        now = root
        res = []

        while now:
            if now.val > target:
                ma.append(now)
                now = now.left
            else:
                mi.append(now)
                now = now.right
        
        while k > 0:
            choose_mi = False

            if not mi:
                if not ma:
                    break
                else:
                    choose_mi = False
            elif not ma:
                choose_mi = True
            elif abs(ma[-1].val - target) < abs(mi[-1].val - target):
                choose_mi = False
            else:
                choose_mi = True
            
            if choose_mi:
                res.append(mi[-1].val)
                now = mi[-1].left
                mi.pop()
                while now:
                    mi.append(now)
                    now = now.right
            
            else:
                res.append(ma[-1].val)
                now = ma[-1].right
                ma.pop()
                while now:
                    ma.append(now)
                    now = now.left
            
            k -= 1
        
        return res
```
