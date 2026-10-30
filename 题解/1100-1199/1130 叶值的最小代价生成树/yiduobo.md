---
title: "1130. 叶值的最小代价生成树"
aliases: ["yiduobo的每日leetcode 1130.叶值的最小代价生成树"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/376515509"
zhihu_id: "376515509"
zhihu_title: "yiduobo的每日leetcode 1130.叶值的最小代价生成树"
question_id: "1130"
question: "叶值的最小代价生成树"
problem_url: "https://leetcode.cn/problems/minimum-cost-tree-from-leaf-values/"
created: "2021-05-30T19:38:47+08:00"
updated: "2021-05-30T19:38:47+08:00"
upvotes: 0
comments: 0
---

# 1130. 叶值的最小代价生成树

> **[yiduobo的每日leetcode 1130.叶值的最小代价生成树](https://zhuanlan.zhihu.com/p/376515509) · 知乎 · 2021-05-30 · 赞同 0**
> 力扣：[1130. 叶值的最小代价生成树](https://leetcode.cn/problems/minimum-cost-tree-from-leaf-values/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1130.叶值的最小代价生成树

[力扣](https://leetcode-cn.com/problems/minimum-cost-tree-from-leaf-values/)

动态规划的算法是很容想到了。令f[l][r]表示arr[l : r + 1]这个子数组所形成的最小代价生成树，那么我们可以枚举分割点p，其中arr[l : p]为左子树，arr[p : r + 1]为右子树，那么就有

f[l][r] \= min(f[l][p - 1] + f[p][r] + max(arr[l : p]) \* max(arr[p : r + 1]))

我们可以提前预处理好max相关的东西，那么最终就可以在O(n^2)的时间复杂度内求出最终结果。

除此之外，还可以将问题转化成给出一个数组，每次选择两个相邻的数相乘，将乘积累加到答案之后去除较小的那个数。重复这个过程直到数组中只剩下一个数。

对于这个问题，我们不妨考虑这种情况。在某一时刻存在一个i，满足

arr[i - 1] > arr[i] \<\= arr[i + 1]

那么对于arr[i]而言，无论后续如何操作，其只会进行一次乘法操作然后就会被去除掉。那么此时对于arr[i]而言：

1、可以首先处理arr[0]到arr[i - 1]中的合并，得到某个arr[j]再与arr[i]进行合并。这种情况下必然有arr[j] >\= arr[i - 1]，那么相对地，如果我们先将min(arr[i - 1], arr[i + 1])与arr[i]进行合并，再处理arr[0]到arr[i - 1]中的合并，其代价显然是更小的。

2、可以首先处理arr[i + 1]到arr[-1]中的合并，得到某个arr[k]再与arr[i]进行合并。这种情况下必然有arr[k] >\= arr[i + 1]，那么相对地，如果我们先将min(arr[i - 1], arr[i + 1])与arr[i]进行合并，再处理arr[i + 1]到arr[-1]中的合并，其代价显然是更小的。

综合起来，说明此时我们就应当直接合并掉arr[i]以及min(arr[i - 1], arr[i + 1])。

对于arr[i - 1] > arr[i]这种结构，我们可以使用单调栈来进行储存。方便起见，我们可以先在栈中设置边界值16，这样做的目的是方便处理i\=0时没有arr[i - 1]的情况。此时的16必然是大于等于arr[i]的，且其必然小于arr[i + 1]，因此不会影响到最终结果。

那么现在的做法就是一趟扫描，对于当前的arr[index]，若其大于等于栈顶元素stack[-1]，那么说明此时的栈顶arr[-1]就形成了stack[-2] > stack[-1] \<\= arr[index]，因此我们应当合并stack[-1]以及min(stack[-2], arr[index])，然后将stack[-1]弹出。重复此过程直到arr[index]小于栈顶元素stack[-1]为止。此时将arr[index]压入栈中然后继续向后扫描即可。

扫描完毕后，栈中可以还有没有合并的元素。由于栈是单调递减的，因此应该逐个合并stack[-1]以及stack[-2]，然后将stack[-1]弹出，直到栈中只剩下两个元素，即初始的16以及另一个元素为止。

最后附上python代码：

```python
class Solution(object):
    def mctFromLeafValues(self, arr):
        """
        :type arr: List[int]
        :rtype: int
        """

        stack = [16]
        res = 0
        for num in arr:
            while num >= stack[-1]:
                res += stack[-1] * min(num, stack[-2])
                stack.pop()
            stack.append(num)
        
        while len(stack) > 2:
            res += stack[-1] * stack[-2]
            stack.pop()
        
        return res
```
