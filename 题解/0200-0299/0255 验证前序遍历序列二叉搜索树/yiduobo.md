---
title: "255. 验证前序遍历序列二叉搜索树"
aliases: ["yiduobo的每日leetcode 255.验证前序遍历序列二叉搜索树"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/593020005"
zhihu_id: "593020005"
zhihu_title: "yiduobo的每日leetcode 255.验证前序遍历序列二叉搜索树"
question_id: "255"
question: "验证前序遍历序列二叉搜索树"
problem_url: "https://leetcode.cn/problems/verify-preorder-sequence-in-binary-search-tree/"
created: "2022-12-20T01:06:22+08:00"
updated: "2022-12-20T01:06:22+08:00"
upvotes: 0
comments: 0
---

# 255. 验证前序遍历序列二叉搜索树

> **[yiduobo的每日leetcode 255.验证前序遍历序列二叉搜索树](https://zhuanlan.zhihu.com/p/593020005) · 知乎 · 2022-12-20 · 赞同 0**
> 力扣：[255. 验证前序遍历序列二叉搜索树](https://leetcode.cn/problems/verify-preorder-sequence-in-binary-search-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

255.验证前序遍历二叉搜索树

[力扣](https://leetcode.cn/problems/verify-preorder-sequence-in-binary-search-tree/)

首先，前序遍历的第一个值显然是数的根节点的值。如果这是一棵二叉搜索树，那么前序遍历的构成必然是根-所有值小于根节点值的节点形成的左子树的前序遍历-所有值大于根节点值的节点形成的右子树的前序遍历。因此如果存在左子树，那么其左子树根节点的值就是前序遍历中的第二个值，而右子树相对复杂一点，如果存在右子树，那么其右子树根节点的值就是前序遍历中从左向右第一个大于根节点值的值。

根据这个结论，就可以通过前序遍历确认当前数左右子树根节点对应的下标，从而将前序遍历拆解成三个部分，此时就可以检测这种划分是否符合要求，然后再递归求解左右子树。通过上面这种方法找出来的左子树中，每个节点值都是小于根节点值的，无需进行额外的检测。而对于右子树，则要求其中的最小值必须大于根节点的值。

到了这一步，就需要实现两个操作：

1、找出前序遍历中每个数下一个更大的数的位置

2、找出前序遍历中任意区间中的最小值

对于问题1，是经典的单调栈问题，具体可以参考496题。

[yiduobo：yiduobo的每日leetcode 496.下一个更大元素I](https://zhuanlan.zhihu.com/p/257283167)

对于问题2，常规做法可能需要使用线段数，实现的复杂就比较高了，可以想想有没有存在可以优化的地方。

题目中主要的检测出现在检测所有存在右子树的节点，其右子树中是否存在比该节点值更小的节点，也就是对于节点now，如果now.right不为空，那么以now.right为根节点的子树中是否存在比now更小的节点。在这里如果now.right自身也存在右子树，那么now.right必须先经受其自身的右子树，也就是以now.right.right为根节点的子树的考验。而一旦now.right通过了考验，那么now实际上就只需要考虑now.right的左子树中是否存在某个节点的值小于now的值，因为now.right的右子树中的值都大于now.right的值，因此必然大于now的值。

更进一步的，实际上now需要考虑的就是所有在now.right到now.right.right之间，所有向左走的节点的值是否小于now的值，而其他节点的值会有各自子树的根节点帮now处理掉，而这一过程恰好可以融合到单调栈求解下一个更大值的操作中。具体来说，就是当一轮弹栈操作完成后，被弹出栈的最后一个节点必然是所有值小于当前节点的节点中值最小，也是辈分最高的那一个。只要满足了这个节点，其他被弹出节点关于向左走的节点的值的检测也顺带就完成了，因此不妨将其记为root_val，接下来只需判断接下来遍历到的节点值是否都大于root_val，直到出现某个不符合条件的节点，或者root_val因为碰到上面提到的待检测右子树的迭代而同步产生迭代为止。

具体实现上的代码非常简洁，但是要理清楚root_val的取值方法，以及确定这种做法能涵盖所有情况则需要花一番功夫。

最后附上python代码：

```python
class Solution(object):
    def verifyPreorder(self, preorder):
        """
        :type preorder: List[int]
        :rtype: bool
        """

        root_val = -1
        stack = []
        for v in preorder:
            if root_val > v:
                return False
            
            while stack and stack[-1] < v:
                root_val = stack[-1]
                stack.pop()

            stack.append(v)
        
        return True
```
