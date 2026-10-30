---
title: "1902. 给定二叉搜索树的插入顺序求深度"
aliases: ["yiduobo的每日leetcode 1902.给定二叉搜索树的插入顺序求深度"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/622996695"
zhihu_id: "622996695"
zhihu_title: "yiduobo的每日leetcode 1902.给定二叉搜索树的插入顺序求深度"
question_id: "1902"
question: "给定二叉搜索树的插入顺序求深度"
problem_url: "https://leetcode.cn/problems/depth-of-bst-given-insertion-order/"
created: "2023-04-19T00:57:15+08:00"
updated: "2023-04-19T00:57:15+08:00"
upvotes: 0
comments: 0
---

# 1902. 给定二叉搜索树的插入顺序求深度

> **[yiduobo的每日leetcode 1902.给定二叉搜索树的插入顺序求深度](https://zhuanlan.zhihu.com/p/622996695) · 知乎 · 2023-04-19 · 赞同 0**
> 力扣：[1902. 给定二叉搜索树的插入顺序求深度](https://leetcode.cn/problems/depth-of-bst-given-insertion-order/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1902.给定二叉搜索树的插入顺序求深度

[力扣](https://leetcode.cn/problems/depth-of-bst-given-insertion-order/)

本题最直观的处理方法自然是按照插入顺序构造出完整的二叉树，但是暴力求解的算法是O(n^2)的，需要优化。

从区间分割的角度来看，本题可以认为是给出一个1到n的区间，然后遍历插入顺序。对于当前遍历到的值v，每次找出当前区间中恰好包含当前v的区间[left, right]，此时这个v就会将区间分割成[left, v - 1]以及[v + 1, right]。如果使用平衡树或者线段树来维护这些区间，就可以在O(nlogn)的时间内完成所有的区间分割，也就是得到完整的二叉搜索树。

另一个思路是从节点自身的角度出发。对于一个值v，其插入树的位置取决于已有树中所有小于v的节点中最大的那一个以及所有大于v的节点中最小的那一个中深度较深的那一个。用公式来描述，就是对于下标位置i的数值v，要求找出下标在0到i - 1之间所有满足order[j] \< v中order[j]最大的那一个，以及所有满足order[j] > v中order[j]中最小的那一个，而v就是这两个节点中较深的那个的孩子。

证明也很简单，不妨分别记下标小于i，且数值小于v中最大的节点以及大于v中最小的节点为ma和mi，那么就必然有ma \< v \< mi，同时ma到v之间，以及v到mi之间都不存在其他节点，因此ma和mi必然在同一颗树中，只能是父子或者祖孙关系。根据这个结论，v就只能放置在较深的那个节点下面，因为较浅的那个节点适合v的那一侧已经被占据了。

根据这个结论，就可以一趟遍历，对于每个v找出其对应的ma和mi，取二者深度较深的那一个作为v的父亲节点。遍历完成后，就相当于构造出了这棵树。

而对于找ma和mi这问题，乍一看依然是需要使用树结构来求解，不过注意到order中不存在相同的数值，则可以利用rank数组来辅助求解。记rank\[order\[i\]\] \= i，那么本来求解的ma是满足j \< i且order\[j\] \< order\[i\]中最大的order\[j\]，套用到rank数组里就是满足j \< i且rank\[j\] \< rank\[i\]中最大的j，也就是熟悉的左侧第一个更大的数的位置，可以利用单调栈在一趟遍历的过程中求解。而对于mi，则是满足j > i且rank\[j\] \< rank\[i\]中最小的j，可以在求解ma的过程中顺便求解。

到了这里，就可以先通过一趟遍历，利用单调栈求出order中每个数对应的ma以及mi，接下来一趟遍历，对于每个值v利用ma和mi的深度求解v的深度即可。

最后附上python代码：

```python
class Solution(object):
    def maxDepthBST(self, order):
        """
        :type order: List[int]
        :rtype: int
        """

        n = len(order)
        rank = [0] * n
        for index, v in enumerate(order):
            rank[v - 1] = index
        
        ma = [n] * n
        mi = [n] * n
        stack = []

        for index, v in enumerate(rank):
            while stack and rank[stack[-1]] > v:
                ma[rank[stack[-1]]] = v
                stack.pop()

            if stack:
                mi[v] = rank[stack[-1]]

            stack.append(index)
        
        depth = [0] * (n + 1)
        for index in range(1, n):
            depth[index] = max(depth[ma[index]], depth[mi[index]]) + 1
            
        return max(depth) + 1
```
