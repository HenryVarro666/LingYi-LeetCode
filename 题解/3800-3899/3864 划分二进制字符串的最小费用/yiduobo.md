---
title: "3864. 划分二进制字符串的最小费用"
aliases: ["yiduobo的每日leetcode 3864.划分二进制字符串的最小费用"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/divide-and-conquer", "leetcode/prefix-sum", "leetcode/simulation", "leetcode/bao-li", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/五-其他递归/分治"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2014140249865986764"
zhihu_id: "2014140249865986764"
zhihu_title: "yiduobo的每日leetcode 3864.划分二进制字符串的最小费用"
question_id: "3864"
question: "划分二进制字符串的最小费用"
problem_url: "https://leetcode.cn/problems/minimum-cost-to-partition-a-binary-string/"
difficulty: "Hard"
rating: 2032
created: "2026-03-11T23:59:53+08:00"
updated: "2026-03-11T23:59:57+08:00"
upvotes: 1
comments: 0
---

# 3864. 划分二进制字符串的最小费用

> **[yiduobo的每日leetcode 3864.划分二进制字符串的最小费用](https://zhuanlan.zhihu.com/p/2014140249865986764) · 知乎 · 2026-03-11 · 赞同 1**
> 力扣：[3864. 划分二进制字符串的最小费用](https://leetcode.cn/problems/minimum-cost-to-partition-a-binary-string/) · Hard · 灵茶山艾府：[暴力分治即可，时间复杂度 O(n)（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3864.划分二进制字符串的最小费用

<https://leetcode.cn/problems/minimum-cost-to-partition-a-binary-string/description/>

题目给出一个二进制字符串s，以及两个整数encCost以及flatCost。

对于每个下标index，若s[index]为'1'，那么第index个元素就是敏感的，否则是不敏感的。

现在要求为s进行分段操作。起始状态下，整个字符串是一个单一的分段。

对于一个长度为L，且包含X个敏感元素的分段：

- 若X为0，那么其费用就是flatCost
- 若X > 0，那么其费用为L \* X \* encCost

若一个分段的长度为偶数，则还可以对其进行进一步的拆分，将其拆分为两个长度相等的连续分段，此时的费用则改为计算两个分段的费用之和。

问如何进行分段操作，才能使得费用最小。

题目中对于分段的计算与线段树计算区间值的方式是非常类似的，在这里可以选择自顶向下或者自底向上进行求解，我在这里选择的是后者。

具体来说，对于长度为偶数的段，可以将其划分为长度折半的两段，那么经历有限次的划分，必然可以让子段的长度变为奇数，此时无法继续向下划分。也就是说，这个奇数长度是最小的计算单元，可以在初始状态下，不断对s的长度n除以2来计算得到，不妨记为min_length。

接下来，就可以想象自底向上构造一颗线段树的过程。

首先最底层是若干个长度为min_length的子段，分别覆盖了[0, min_length - 1], [min_length, min_length \* 2 - 1], ...这些区间。这些区间对应的费用可以通过题目中描述的方式进行计算。

接下来往上一层，是若干个长度为min_length \* 2的子段。方便起见，在这里记part_length \= min_length \* 2，那么这一层的区间就覆盖了[0, part_length - 1], [part_length, min_length \* 2 - 1]，...这些区间。对于这些区间的费用，可以不进行划分，也就是通过题目中描述的方式进行计算，也可以进行划分，也就是上一轮计算得到的两个折半子区间的结果之和。

不断倍增子段的长度并重复上面的计算过程，直到区间长度等于n为止，此时唯一一个区间对应的费用即为最终答案。总的计算次数为1 + 2 + 4 + ... + 2^k，其中k为n中2的因子数量，因此上述计算的次数是O(n)量级的。

另外需要注意的是，在计算过程中涉及到了区间内1的数量，直接遍历计算的话时间复杂度为O(nlogn)，不过在这里也可以可以通过左右子区间中1的数量之和得到当前区间中1的数量，而对于最小的计算单元这一层，则可以通过一趟遍历得到，因此在优化后时间复杂度还是O(n)。

最后附上python代码：

```python
class Solution(object):
    def minCost(self, s, encCost, flatCost):
        """
        :type s: str
        :type encCost: int
        :type flatCost: int
        :rtype: int
        """
        
        n = len(s)
        
        min_length = n
        while min_length % 2 == 0:
            min_length //= 2
        
        f = [0] * n
        one = [0] * n
        for index in range(0, n, min_length):
            for c in s[index: index + min_length]:
                one[index] += int(c)

            if one[index] == 0:
                f[index] = flatCost
            else:
                f[index] = min_length * one[index] * encCost
        
        part_length = min_length + min_length
        while part_length <= n:
            for index in range(0, n, part_length):
                f[index] += f[index + part_length // 2]
                one[index] += one[index + part_length // 2]
                if one[index] == 0:
                    v = flatCost
                else:
                    v = part_length * one[index] * encCost
                
                f[index] = min(f[index], v)

            part_length += part_length

        return f[0]
```
