---
title: "3796. 找到带限制序列的最大值"
aliases: ["yiduobo的每日leetcode 3796.找到带限制序列的最大值"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1992061384440169699"
zhihu_id: "1992061384440169699"
zhihu_title: "yiduobo的每日leetcode 3796.找到带限制序列的最大值"
question_id: "3796"
question: "找到带限制序列的最大值"
problem_url: "https://leetcode.cn/problems/find-maximum-value-in-a-constrained-sequence/"
difficulty: "Medium"
rating: 1833
created: "2026-01-07T03:09:30+08:00"
updated: "2026-01-07T03:09:33+08:00"
upvotes: 1
comments: 0
---

# 3796. 找到带限制序列的最大值

> **[yiduobo的每日leetcode 3796.找到带限制序列的最大值](https://zhuanlan.zhihu.com/p/1992061384440169699) · 知乎 · 2026-01-07 · 赞同 1**
> 力扣：[3796. 找到带限制序列的最大值](https://leetcode.cn/problems/find-maximum-value-in-a-constrained-sequence/) · Medium · 灵茶山艾府：[两次扫描，传播约束（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3796.找到带限制序列的最大值

[3796. 找到带限制序列的最大值 - 力扣（LeetCode）](https://leetcode.cn/problems/find-maximum-value-in-a-constrained-sequence/)

题目给出一个整数n，一个二维整数数组restrictions，以及一个长度为n - 1的整数数组diff。现在要求构造一个长度为n的数组a，满足：

- a[0]为0
- a中的所有元素非负
- 对于0到n - 2之间的所有下标index，都有abs(a[index] - a[index + 1]) \<\= diff[index]
- 对于每个restrictions中的元素[index, maxVal]，要求a[index]必须小于等于maxVal

问在满足以上所有条件的情况下，a中的最大值最大可能是多少。

为了让a中的最大值最大，就应该让所有受restrictions限制的下标上的元素最大，因此在这里可以先想办法计算出这些位置上的元素可能达到的最大值，然后对于两个受限制位置，期间的元素应该是按照先单调递增再单调递减才能使得最大值最大，当然在这里可能只有单调递增或者单调递减其中一侧。

在这里先考虑如何计算受限位置的值。

由于题目规定了a[0] \= 0，那么对于首个受限位置(index[0]，maxVal[0])，因为diff的限制，其必然小于等于diff[0] + diff[1] + ... + diff[index - 1]。另一方面，其也必须小于等于对应的maxVal[0]，因此可以初步确定其最大值为min(sum(diff[:index]), maxVal[0])，在这里不妨记为pre_v。

接下来对于下一个受限位置(index[1], maxVal[1])，则需要分情况进行讨论。

若pre_v > maxVal\[1\]，那么index\[1\]的最大值必然可以到达maxVal\[1\]，理由是若pre_v \<\= maxVal\[1\] + sum(diff\[index\[0\]: index\[1\]\])，那么就可以通过一些减法操作让pre_v逐步下降到maxVal\[1\]；反之，也可以在上一步让pre_v的取值变小一点，刚好取到maxVal\[1\] + sum(diff\[index\[0\]: index\[1\]\])，就可以通过减法操作让pre_v下降到maxVal\[1\]。无论是哪种情况，index\[1\]的最大值都可以取到maxVal\[1\]，但是需要特别注意的是，对于后面这种情况，为了让index\[1\]的取值合法，之前的index\[0\]的取值就达不到pre_v了。更进一步的，从这里可以看出对于每个受限制的位置，其不仅受前一个受限制位置的影响，也会影响到前一个受限制位置的取值。也就是说，在这里从左到右递推之后，还需要从右向左递推，反过来进行修正。

若pre_v \<\= maxVal\[1\]，那么就需要判断pre_v + sum(diff\[index\[0\]: index\[1\]\])是否大于等于maxVal，若满足，那么index\[1\]这里可以取到maxVal，否则只能取到pre_v + sum(diff\[index\[0\]: index\[1\]\])。对于这种情况，则无需进行反向修正。但是需要注意的是，index\[1\]可能受后续元素修正，而这个修正会传播到index\[0\]，因此从右向左递推的修正是不可避免的。

按以上的做法，从左向右逐步递推，就可以初步确定每个受限制位置的最大值。这里的初步确定是因为后续还需要反向遍历进行修正。

从最后一个受限制位置开始向前遍历，若前一个受限制位置index的可能最大值v大于当前受限制位置nxt_index的可能最大值nxt_v，那么就需要将前一个位置的可能最大值修正为min(v, nxt_v + sum(diff[index: nxt_index]))，也就是前面的讨论中的前一种情况：index上的取值v太大了，导致一路递减，依然大于nxt_index上的取值nxt_v，因此只能让index上的取值v变小一点。

反向修正之后，就得到了最终构造的数组中所有受限制位置的最大值。接下来只需遍历相邻的最大值，模拟期间先递增后递减的过程，并取递增的峰值更新答案即可。

具体来说，对于一组相邻的受限制位置pre_index以及index，不妨设这两个位置可以取到的最大值分别为pre_v以及v，那么在这里就可以使用一个变量p从pre_index开始向后遍历：

1、先保证pre_v可以达到v的水平，进行第一段单调递增：

若p \< index且pre_v \< v，那么就构造一个pre_v + diff[p]加入到数组中，然后将p向后移动，此时的pre_v改为记录这个新元素pre_v + diff[p]

2、接下来对于当前的pre_v和v，期间可能还有一段单调递增的过程：

对于执行完第一段单调递增之后的p，剩下的diff之和delta为sum(diff[p: index])。

比较理想的情况是delta拆分为两个部分，前半部分单调递增，对应的是接下来数组中的元素为pre_v + diff[p]，然后是pre_v + diff[p] + diff[p + 1]，以此类推，最终在pre_v + diff[p] + diff[p + 1] + ... + diff[q]处停止，然后再单调递减回归到v。

为了确定这个q，可以从p开始向后遍历，检测pre_v + diff[p] - (delta - diff[p])是否小于等于v，若满足，将可以将pre_v + diff[p]加入到数组中，这里的小于等于是因为需要足够元素让最大值回到v。p不断向后迭代，直到不满足条件为止。

另外有两种特殊情况需要处理。

首先是p一开始就来到了index，且pre_v > v。这种情况下，必须在第一段单调递增中让pre_v的取值限制在v，也就是这种情况下，只能用v来更新答案。

另一种则是完整的diff[q]过大，但是只增加一点点则是可行的，例如pre_v \= 5，diff \= [10, 3], v \= 4，此时不能将10直接加入到pre_v中，但是可以让pre_v加上2变成7，然后7依然可以通过减3回到4。也就是说，当p \< index时，若pre_v + delta - diff[p] \<\= v，那么就可以将diff[p]中的部分拆出来加到pre_v中，此时这一段的最大值可以达到v + delta - diff[p]，应该使用这个值来更新答案。

3、最后，递减过程就没必要考虑了，因为答案不可能出现在其中。

按照以上过程逐对遍历受限制的位置并更新答案即可。另外不要忘了，在最后一个受限制位置之后，剩下的部分可以单调递增上去，也就是对于最后一个受限制位置pre_index以及对应的最大值pre_v，后续可能得到的最大值为pre_v + sum(diff[pre_index:])，需要使用这个值再更新一次答案。

最后附上python代码：

```python
class Solution(object):
    def findMaxVal(self, n, restrictions, diff):
        """
        :type n: int
        :type restrictions: List[List[int]]
        :type diff: List[int]
        :rtype: int
        """
        
        pre_index = 0
        pre_v = 0
        
        restrictions.sort()
        bound = []
        pre_index = 0
        pre_v = 0
        for index, v in restrictions:
            if pre_v > v:
                pre_v = v
            else:
                delta = sum(diff[pre_index: index])
                if pre_v + delta < v:
                    pre_v += delta
                else:
                    pre_v = v
            
            bound.append([index, pre_v])
            pre_index = index
        
        nxt_index, nxt_v = bound[-1]
        adj_bound = [(nxt_index, nxt_v)]
        for index, v in bound[-2::-1]:
            if v > nxt_v:
                delta = sum(diff[index: nxt_index])
                v = min(nxt_v + delta, v)
            adj_bound.append((index, v))
            nxt_index, nxt_v = index, v
        
        print(adj_bound)
        adj_bound.reverse()

        res = 0
        pre_index = 0
        pre_v = 0
        for index, v in adj_bound:
            p = pre_index
            while p < index and pre_v + diff[p] < v:
                pre_v += diff[p]
                p += 1

            delta = sum(diff[p: index])
            while p < index and pre_v + diff[p] - (delta - diff[p]) <= v:
                pre_v += diff[p]
                delta -= diff[p]
                p += 1

            if p < index and pre_v < delta - diff[p] + v:
                pre_v = delta - diff[p] + v
            
            res = max(res, min(pre_v, v + delta))
            pre_index, pre_v = index, v
        
        return max(res, pre_v + sum(diff[pre_index:]))
```
