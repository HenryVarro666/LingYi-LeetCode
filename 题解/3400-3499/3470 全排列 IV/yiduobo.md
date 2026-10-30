---
title: "3470. 全排列IV"
aliases: ["yiduobo的每日leetcode 3470.全排列IV"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/math", "leetcode/combinatorics", "题单/数学算法", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1896335945567037349"
zhihu_id: "1896335945567037349"
zhihu_title: "yiduobo的每日leetcode 3470.全排列IV"
question_id: "3470"
question: "全排列 IV"
problem_url: "https://leetcode.cn/problems/permutations-iv/"
difficulty: "Hard"
rating: 2474
created: "2025-04-18T00:23:31+08:00"
updated: "2025-04-18T00:23:31+08:00"
upvotes: 0
comments: 0
---

# 3470. 全排列IV

> **[yiduobo的每日leetcode 3470.全排列IV](https://zhuanlan.zhihu.com/p/1896335945567037349) · 知乎 · 2025-04-18 · 赞同 0**
> 力扣：[3470. 全排列 IV](https://leetcode.cn/problems/permutations-iv/) · Hard · 灵茶山艾府：[从左往右构造（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3470.全排列IV

[3470. 全排列 IV - 力扣（LeetCode）](https://leetcode.cn/problems/permutations-iv/description/)

题目给出两个整数n和k，另外定义一个交替排列为前n个正整数形成的，且任意两个相邻元素不同奇偶的排列。现在要求找出字典序第k小的交替排列，若不存在，则返回空数组。

对于这类计算排列第k大的问题，一种常见的处理方法是利用康拓展开，具体做法可以理解成从高位到低位逐位进行填充，对于当前填充的位，在剩余的元素中从小到大枚举填充的元素，并计算剩余元素可以形成的所有排列的总数。若这个排列数大于等于k，说明当前为就应该填充当前枚举到的元素，此时应该继续向后填充；反之，说明当前填充的元素过小，需要尝试下一个元素，同时将k减去之前计算出的排列数。

对于没有其他限制条件的全排列而言，由于剩余元素互不相同，实际上可以等价为计算若干个不同元素形成的排列总数，显然这个排列总数就是这些元素数量的阶乘，可以提前预处理得到。这样一来，就可以在O(n^2)的时间内完成上述的填充过程。

对于本题，由于存在相邻位数不能同奇偶这一限制，在计算剩余元素可以形成的有效排列时的计算方法略有不同。具体来说，对于常规全排列的计算，由于最高位可以任意填充元素，因此最终填充方案是阶乘，而对于本题，由于奇偶性的限制，因此在确定了最高位填充奇数时，每一位可用元素的数目只有剩下元素数量的一半向上取整。这里特别强调确定了最高位填充奇数的理由是对于长度为偶数的交替排列而言，其最高位既可以是奇数也可以是偶数，而对于长度为奇数的交替排列而言，其最高位只能是奇数。

计算得到填充方案数之后，就可以按照最开始所说的方法，从最高位开始向后逐位填充。在这里需要注意的是，当n为奇数时，最高位只能填充奇数，因此在枚举最高位时需要从1到n以步长为2进行枚举，反之当n为偶数时，则应该枚举1到n之间的所有数作为最高位。

在确定了最高位后，对于后续位的填充，则需要根据前一位的奇偶性来确定当前为可以填充哪些元素。

最后附上python代码：

```python
class Solution(object):
    def permute(self, n, k):
        """
        :type n: int
        :type k: int
        :rtype: List[int]
        """
        
        f = [1]
        for index in range(1, n + 1):
            f.append(f[-1] * ((index + 1) // 2))

        if n % 2 == 0:
            if f[-1] * 2 < k:
                return []
            step = 1
        else:
            if f[-1] < k:
                return []
            step = 2
        
        choose = None
        res = []
        used = [False] * (n + 1)
        for x in range(1, n + 1, step):
            if k > f[n - 1]:
                k -= f[n - 1]
            else:
                choose = x
                break
            
        res.append(choose)
        used[choose] = True

        for r in range(2, n):
            if res[-1] % 2 == 0:
                start = 1
            else:
                start = 2
            choose = None
            for x in range(start, n + 1, 2):
                if not used[x]:
                    if k > f[n - r]:
                        k -= f[n - r]
                    else:
                        choose = x
                        break
            
            res.append(choose)
            used[choose] = True
        
        for x in range(1, n + 1):
            if not used[x]:
                res.append(x)
                break
        
        return res
```
