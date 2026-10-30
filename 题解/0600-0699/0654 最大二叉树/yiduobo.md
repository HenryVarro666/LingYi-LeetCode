---
title: "654. 最大二叉树"
aliases: ["yiduobo的每日leetcode 654.最大二叉树"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/279435477"
zhihu_id: "279435477"
zhihu_title: "yiduobo的每日leetcode 654.最大二叉树"
question_id: "654"
question: "最大二叉树"
problem_url: "https://leetcode.cn/problems/maximum-binary-tree/"
created: "2020-11-08T17:52:42+08:00"
updated: "2020-11-08T17:52:42+08:00"
upvotes: 1
comments: 0
---

# 654. 最大二叉树

> **[yiduobo的每日leetcode 654.最大二叉树](https://zhuanlan.zhihu.com/p/279435477) · 知乎 · 2020-11-08 · 赞同 1**
> 力扣：[654. 最大二叉树](https://leetcode.cn/problems/maximum-binary-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

654.最大二叉树

[力扣](https://leetcode-cn.com/problems/maximum-binary-tree/)

一个直观的想法就是每次从当前区间选择最大值作为根节点，然后通过这个最大值划分左右子树之后递归求解。使用朴素算法这里的时间复杂度位O(n^2)，当然也可以使用线段树之类的东西将求区间最大值的时间复杂度优化到logn，最后达成O(nlogn)的时间复杂度。

不过在这里，利用根节点是最大值以及划分左右子树这个性质，我们可以得到更好的做法。

对于数组中的某个值nums[index]，若其不是根节点，那么其父亲节点的值必然是离index最近的，且值大于nums[index]的某个数。这里的最近指的是数组下标上的最近。

证明也很简单，不妨设nums[p] > nums[q] > nums[r]，p \< q \< r。若此时r的父亲节点是p，那么说明从p + 1到r这一段里面最大的数是nums[r]，但此时nums[q]是大于nums[r]的，产生矛盾。

数组的方向反过来也成立，设nums[p] > nums[q] > nums[r]，且p > q > r，若此时r的父亲节点是p，那么说明从r到p - 1这一段里面最大的数是nums[r]，同样与nums[q]产生矛盾。

当然，对于index而言，其左侧和右侧可能都存在离index最近且值大于nums[index]的数，此时我们应当选择较小的那一个作为index的父亲，证明如下：

设nums[r] > nums[p] > nums[q]，且p \< q \< r，同时p到q之间以及q到r之间不存在其他大于nums[q]的数。由于p到r - 1这一段里面的数都小于nums[r]，因此这些数必然都是nums[r]左子树中的节点。此时若nums[q]的父亲是nums[r]，表示这颗子树中的最大值是nums[q]，与nums[p]产生矛盾了。

有了上面这两个结论，我们就可以对于每个数nums[index]，找到其左侧和右侧离得最近，且大于nums[index]的数。若左侧的较小，那么将nums[index]设为左侧数的右孩子，否则将nums[index]设为右侧数的左孩子。

为了高效获得两侧离得最近的较大值，我们可以使用一个单调栈来进行处理。具体来说就是一趟扫描，对于当前的nums[index]：

1、若栈为空，说明该元素左侧没有更大的元素，但还需要找到右侧比该元素更大的数，因此将其压入栈中即可。

2、若其小于栈顶元素，说明其左侧离得最近，且大于nums[index]的数就是栈顶元素，但此时栈中所有元素包括nums[index]都还没有找到右侧离得最近且较大的数，因此此时应该将nums[index]压入栈中。

3、若其大于栈顶元素，那么此时栈顶元素就已经找齐了左右两侧离得最近且较大的数，将其从栈中弹出并与新的栈顶元素或者当前的nums[index]建立父子关系。接下来继续考察nums[index]与新的栈顶元素的关系，直到出现情况1或者情况2。

当一趟扫描之后，栈中必然还存在一些元素无法找到右侧的更大值，此时从栈顶元素开始，将其作为上一个元素的右子树即可。最后出栈的元素左右两侧都没有更大值，为最后的根节点。

由于每个元素最多进出栈一次，因此最终的时间复杂度为O(n)。

最后附上代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def constructMaximumBinaryTree(self, nums):
        """
        :type nums: List[int]
        :rtype: TreeNode
        """

        stack = []
        left = {}
        right = {}
        for num in nums:
            now = TreeNode(num)
            while stack and stack[-1].val < num:
                tmp = stack.pop()
                if stack and stack[-1].val < num:
                    stack[-1].right = tmp
                else:
                    now.left = tmp
            
            stack.append(now)

        if stack:
            now = stack.pop()
            while stack:
                stack[-1].right = now
                now = stack.pop()

        return now
```
