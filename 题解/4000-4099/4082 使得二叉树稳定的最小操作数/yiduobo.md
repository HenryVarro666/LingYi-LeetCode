---
title: "4082. 使得二叉树稳定的最小操作数"
aliases: ["yiduobo的每日leetcode 4802.使得二叉树稳定的最小操作数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2094977040101401910"
zhihu_id: "2094977040101401910"
zhihu_title: "yiduobo的每日leetcode 4802.使得二叉树稳定的最小操作数"
question_id: "4082"
question: "使得二叉树稳定的最小操作数"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-stabilize-a-binary-tree/"
title_number_fixed: ["4802→4082"]
created: "2026-10-18T03:24:34+08:00"
updated: "2026-10-18T03:24:34+08:00"
upvotes: 0
comments: 0
---

# 4082. 使得二叉树稳定的最小操作数

> **[yiduobo的每日leetcode 4802.使得二叉树稳定的最小操作数](https://zhuanlan.zhihu.com/p/2094977040101401910) · 知乎 · 2026-10-18 · 赞同 0**
> 力扣：[4082. 使得二叉树稳定的最小操作数](https://leetcode.cn/problems/minimum-operations-to-stabilize-a-binary-tree/)
> 原文标题里的题号写作 4802，这里改成 4082：力扣还没有 4802 题，作者按题号顺序写，前一篇是 4081，后一篇是 4083，所以是 4082

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4802.minimum-operations-to-stabilize-a-binary-tree

<https://leetcode.cn/problems/minimum-operations-to-stabilize-a-binary-tree/description/>

题目给出一颗二叉树的树根，树中每个节点都有一个权重值val。

对于一颗二叉树，若其中每一组父子节点对之间的权重值val之差不超过1，那么就称这颗二叉树是稳定的。

现在可以执行若干次操作，每次操作中，都可以将树中某个节点的值加上1或者减去1，问最少需要多少次操作才能使得树稳定。

树中节点数量不超过50000，权重的取值范围在-10^5到10^5之间。

现在的常规困难题都已经到lcp的难度。本题需要用到凸优化维护斜率的技巧，以及左偏树合并堆的操作，有兴趣的同学可以先参考之前的lcp59，是同一类型的问题。

[yiduobo的每日leetcode LCP59.搭桥过河](https://zhuanlan.zhihu.com/p/578857297)

对于本题，如果仅有一个节点那么就是非常容易的，显然让这个节点保持原状就好了。如果用函数来表示这个代价，那么就有

$f_{}(x) = \begin{cases} -x + val, & x < val \\ 0,      & x = val \\ x - val,  & x > val \end{cases}$ 接下来考虑这个父子之差至多为1会为取值带来了什么影响。

以第一个样例举例，根节点5的左孩子值为8，那么在不考虑5的前提下，左孩子取值为8是最合适的。从这个8出发，如果往上推一层的话，可以发现此时根节点的取值在7到9之间时，左孩子都可以取到最优值8。更进一步的，如果根节点的取值x小于7，那么左孩子的取值就应该取x + 1，反之若根节点的取值x大于9，那么左孩子的取值则应该取x - 1。

具体来说，一开始，左子树对应的函数如下

$$f_{\mathrm{left}}(x) = \begin{cases} -x + 8, & x < 8 \\ 0,      & x = 8 \\ x - 8,  & x > 8 \end{cases}$$

但是从根节点的视角出发，左子树对应的函数变成了这样

$f_{\mathrm{left\_for\_father}}(x) = \begin{cases} -x + 7, & x < 7 \\ 0,      & 7 <= x <= 9 \\ x - 9,  & x > 9 \end{cases}$相当于分段函数的分段点以最小值为基准，从中间向两侧外扩了1。

同样的，对于右子树，其原始的函数以及从根节点来看的函数分别为

$f_{\mathrm{right}}(x) = \begin{cases} -x + 3, & x < 3 \\ 0,      & x = 3 \\ x - 3,  & x > 3 \end{cases}$ 以及

$f_{\mathrm{right\_for\_father}}(x) = \begin{cases} -x + 2, & x < 2 \\ 0,      & 2 <= x <= 4 \\ x - 4,  & x > 4 \end{cases}$此时，从根节点的视角来看，目标就是选择一个最优的x，使得f_left_for_father(x) + f_right_for_father(x) + |x - 5|最小。其中|x - 5|也可以写成这种形式

$f_{\mathrm{ori\_root}}(x) = \begin{cases} -x + 5, & x < 5 \\ 0,      & x = 5 \\ x - 5,  & x > 5 \end{cases}$对于这个问题，最直观的做法自然是将这三者合并，然后找出最优值。在这里先尝试手动合并，看看会发生什么。

首先对于right_for_father的部分，其中x \< 2以及2 \<\= x \<\= 4这两段都满足x \< 7，因此这两段需要叠加left_for_father中x \< 7对应的-x + 7，因此得到了

$f_{\mathrm{merge}}(x) = \begin{cases} -2x + 9, & x < 2 \\ -x + 7,      & 2 <= x <= 4 \end{cases}$而对于4 \< x \< 7这一段，命中的是left_for_father中的x \< 7对应的-x + 7，以及right_for_father中的x > 4对应的x - 4，可以发现这里的x抵消了，剩下了7 - 4 \= 3这一常数项，即

$$f_{\mathrm{merge}}(x) = \begin{cases} 3, & 4 < x < 7 \\ \end{cases}$$

最后，对于7 \<\= x \<\= 9以及x > 9，这两段都满足x > 4，因此这两段需要叠加right_for_father中的x > 4对应的x - 4，因此得到了

$f_{\mathrm{merge}}(x) = \begin{cases} x - 4, & 7 <= x <= 9 \\ 2x - 13,      & 9 < x \end{cases}$全部综合起来，就是

$$f_{\mathrm{merge}}(x) = \begin{cases} -2x + 9, & x < 2 \\ -x + 7, & 2 <= x <= 4 \\ 3,      & 4 < x < 7 \\ x - 4, & 7 <= x <= 9 \\ 2x - 13,  & x > 9 \end{cases}$$

接下来还需要叠加f_ori_root，不过得到的是：

$$f_{\mathrm{final}}(x) = \begin{cases} -3x + 14, & x < 2 \\ -2x + 12, & 2 <= x <= 4\\ -x + 8, & 4 < x < 5 \\ 3, & x = 5 \\ x - 2, & 5 < x < 7 \\ 2x - 9, & 7 <= x <= 9 \\ 3x - 18, & x > 9 \end{cases}$$

因此，最终答案就是根节点取5时对应f_final(5) \= 3。

观察上面的形式可以发现：

1、每次合并后，分段函数的所有分割点原样保留

2、每次合并后，x的斜率依然是连续的，是一个从大到小，到0，再到大的过程，而这些斜率对应的分割点是单调递增的。这正是绝对值函数合并的特点

那么对于本题，实际上就是一个自底向上，不断将左右孩子的分段函数分割点向外扩展1，合并后再与自身的绝对值函数合并的过程。根据上面总结出来的性质，在这里就需要做的就是：

- 根据x斜率的正负记录这些分割点。需要注意，这里利用了分割点单调递增的特点。只需要区分出在哪一侧，就可以通过这一侧的需来还原出每一段的斜率和截距，而不需要再记录具体的斜率和截距了。
- 高效将分割点向外扩展1，即上面提到的父节点视角下的子树对应的函数，有1的容错，所以可以从最小值开始向两侧将分割点扩展1。
- 高效合并子树的分割点以及自身的绝对值函数(绝对值函数也可以写成分割点的形式)。注意这里的合并需要保证序的正确，尤其是一个函数的正斜率分割点在另一个函数的负斜率左侧时，二者合并将使得斜率抵消，同时抬升最小值，这也是答案的来源。除此之外，还需要手动纠正这个逆序

综合上面这节点要求，在这里使用左偏树是比较合适的。

左偏树是一种特殊的堆，其除了常规的堆的大小性质之外，还额外维护一个dist值。约定空节点的dist值为0，而其他节点的dist值则表示其在树中与最近的空节点距离。而对于左偏树的改造，其需要满足左孩子的dist大于等于右孩子的dist，这也是左偏树名称的由来，大部分节点集中在左侧，而右侧链上的节点数量不超过logn。

这样做的好处就是，在执行合并时，假设合并的是x和y，那么就可以先判断谁是新的根节点，然后将新根节点的右孩子，与另一方进行递归合并。由于右链长度的限制，这里合并的时间复杂度就是O(logn + logm)，其中n和m是这两个左偏树的大小。

对于本题，使用两棵左偏树来分别维护每个分段函数负斜率的分割点以及正斜率的分割点，这样一来就可以解决掉合并以及纠正逆序。对于纠正逆序，则需要利用对顶堆的经典操作：令负斜率的堆为大顶堆，正斜率的堆为小顶堆，那么两个堆的堆顶如果产生了逆序，交换二者，重复此过程直到没有逆序为止。在这里交换堆顶的过程则可以视为将堆顶弹出，然后合并原始的左右孩子，再合并对方的原始堆顶。

而对于向外扩展1的操作，则可以利用树的性质，通过经典的懒更新策略来完成。每次扩展时，令负斜率堆的根节点对应的标记减去1，正斜率堆的根节点对应的标记加上1，当合并操作发生时，再更新当前节点值并下放标记即可。

还是以样例来举例。首先，左孩子对应的两个堆为[8], [8]，右孩子对应的则是[3], [3]。接下来回到根节点，首先对这几个堆进行向外扩展，此时左孩子对应的两个堆为[7], [9]，右孩子对应的则是[2], [4]。

接下来执行合并操作。一开始是负斜率和负斜率合并，正斜率和正斜率合并，得到了[7, 2], [4, 9]。在这里可以发现，7和4出现了逆序，此时需要交换二者，并将答案加上7 - 4 \= 3，得到了[4, 2]，[7, 9]。最后，将5分别加入这两个堆，得到了[5, 4, 2]以及[5, 7, 9]，发现没有逆序，无需后续的操作了。

到了这里，就得到了所有分割点，刚好对应上面计算的分段函数，同时最优值应该取两个堆堆顶间的值，在这里只能取5，得到的答案就是前面通过累加7 - 4计算出来的3。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def stabilizeBinaryTree(self, root):
        """
        :type root: Optional[TreeNode]
        :rtype: int
        """
        
        left = [0]
        right = [0]
        dist = [0]
        val = [0]
        delta = [0]
        global res
        res = 0

        def new_ist(v):
            left.append(0)
            right.append(0)
            dist.append(1)
            val.append(v)
            delta.append(0)
            return len(left) - 1

        def merge(x, y, sign):
            if not x or not y:
                return x | y
            
            if delta[x]:
                val[x] += delta[x]
                delta[left[x]] += delta[x]
                delta[right[x]] += delta[x]
                delta[x] = 0
            
            if delta[y]:
                val[y] += delta[y]
                delta[left[y]] += delta[y]
                delta[right[y]] += delta[y]
                delta[y] = 0
            
            if val[x] * sign > val[y] * sign:
                x, y = y, x
            
            right[x] = merge(right[x], y, sign)
            if dist[left[x]] < dist[right[x]]:
                left[x], right[x] = right[x], left[x]
            
            dist[x] = dist[right[x]] + 1
            return x

        def dfs(now):
            if now.left:
                left_neg, left_pos = dfs(now.left)
                delta[left_neg] -= 1
                delta[left_pos] += 1
            else:
                left_neg, left_pos = 0, 0
            
            if now.right:
                right_neg, right_pos = dfs(now.right)
                delta[right_neg] -= 1
                delta[right_pos] += 1
            else:
                right_neg, right_pos = 0, 0
            
            neg = merge(left_neg, right_neg, -1)
            pos = merge(left_pos, right_pos, 1)
            

            root_neg = new_ist(now.val)
            root_pos = new_ist(now.val)

            neg = merge(neg, root_neg, -1)
            pos = merge(pos, root_pos, 1)

            global res
            while neg and pos and val[neg] + delta[neg] > val[pos] + delta[pos]:
                ori_neg = neg
                neg = merge(left[neg], right[neg], -1)
                left[ori_neg] = 0
                right[ori_neg] = 0

                ori_pos = pos
                pos = merge(left[pos], right[pos], 1)
                left[ori_pos] = 0
                right[ori_pos] = 0

            
                neg = merge(neg, ori_pos, -1)
                pos = merge(pos, ori_neg, 1)
                res += val[ori_neg] - val[ori_pos]

            return neg, pos

        dfs(root)
        return res
```
