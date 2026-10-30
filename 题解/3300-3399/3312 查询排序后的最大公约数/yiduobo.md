---
title: "3312. 查询排序后的最大公约数"
aliases: ["yiduobo的每日leetcode 3312.查询排序后的最大公约数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/math", "leetcode/binary-search", "leetcode/dynamic-programming", "leetcode/number-theory", "leetcode/prefix-sum", "题单/数学算法", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1709794890"
zhihu_id: "1709794890"
zhihu_title: "yiduobo的每日leetcode 3312.查询排序后的最大公约数"
question_id: "3312"
question: "查询排序后的最大公约数"
problem_url: "https://leetcode.cn/problems/sorted-gcd-pair-queries/"
difficulty: "Hard"
rating: 2533
created: "2024-10-18T04:23:54+08:00"
updated: "2024-10-18T04:23:54+08:00"
upvotes: 1
comments: 0
---

# 3312. 查询排序后的最大公约数

> **[yiduobo的每日leetcode 3312.查询排序后的最大公约数](https://zhuanlan.zhihu.com/p/1709794890) · 知乎 · 2024-10-18 · 赞同 1**
> 力扣：[3312. 查询排序后的最大公约数](https://leetcode.cn/problems/sorted-gcd-pair-queries/) · Hard · 灵茶山艾府：[倍数容斥+前缀和+二分查找（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3312.查询排序后的最大公约数

[. - 力扣（LeetCode）](https://leetcode.cn/problems/sorted-gcd-pair-queries/description/)

题目给出一个长度为n的整数数组nums以及另一个整数数组queries。

gcdPairs表示数组nums中所有满足0 \<\= i \< j \< n的数对(nums[i], nums[j])的最大公约数按升序排列后构成的数组，现在要求对于每个询问queries[i]，找出gcdPairs中下标为queries[i]对应的元素是什么。

n的规模可达10^5，而长度为n的数组一共可以形成n \* (n - 1) // 2个数对，也就是说gcdPairs的长度非常长，不可能通过模拟将其全部计算出来。

注意到题目中元素的大小在5 \* 10^4以内，这也就意味着gcdPairs中所有的元素大小都在1到5 \* 10^4之间。由于gcdPairs是按照升序排布的，那么在这里就可以想办法计算出其中每种元素出现的次数，然后计算出次数的前缀和，这样一来就可以在这个前缀和中二分每个queries来找到对应的答案了。

现在的问题变成了如何计算每种最大公约数出现的次数。

对于数对(nums[i], nums[j])，若二者都是某个值v的倍数，那么二者的最大公约数就有可能是v。这里的有可能是因为二者的最大公约数并不是v，而是v的若干倍。例如2和4、2和6、2和8的最大公约数都是2，但是4和8的最大公约数是4。在这里需要注意的是，不能简单认为最大公约数为v的数对可以直接利用v和v自身，以及v和v的若干倍组合得到，因为也存在4和6这样的数对最大公约数为2，因此在这里就只能用最暴力的方法，即

最大公约数为v的数对，等于所有为v的倍数的数两两组合形成的数对数量，减去最大公约数为2v、3v、...、kv的数对的数量。

用更形式化的说法，令freq[x]表示在nums中x出现的次数，mul[x]表示nums中值为x的倍数的数的数量，pairs[x]表示最大公约数为x的数对的数量，那么

pairs[x] \= mul[x] \* (mul[x] - 1) // 2 - pairs[x \* 2] - pairs[x \* 3] - ... - pairs[x \* k]

另一方面，对于mul[x]，有

mul[x] \= freq[x] + freq[x \* 2] + freq[x \* 3] + ... + freq[x \* k]

可以发现，上面的过程与筛法求素数是很类似的，于是可以使用类似筛法的处理方法：

遍历所有的x，对于当前的x，以x为步长遍历x、x \* 2、... 、x \* k来更新mul[x]以及pairs[x]，这样做的时间复杂度为O(ma \* log(ma))，其中ma为nums中的最大值，在本体中就是5 \* 10^4。

另外注意到pairs这边需要减去后续的结果，因此在具体实现时应该按从大到小的顺序遍历x。

得到pairs后，一趟遍历计算前缀和s，然后对于每个询问二分其落在s的那个区间内即可。

最后附上python代码：

```python
class Solution(object):
    def gcdValues(self, nums, queries):
        """
        :type nums: List[int]
        :type queries: List[int]
        :rtype: List[int]
        """

        ma = max(nums)
        freq = [0] * (ma + 1)
        mul = [0] * (ma + 1)
        pairs = [0] * (ma + 1)

        for v in nums:
            freq[v] += 1
        
        n = len(nums)
        pairs[1] = n * (n - 1) // 2

        for v in range(ma, 1, -1):
            mul[v] = freq[v]
            for x in range(v + v, ma + 1, v):
                mul[v] += freq[x]
                pairs[v] -= pairs[x]
            
            pairs[v] += mul[v] * (mul[v] - 1) // 2
            pairs[1] -= pairs[v]

        s = [0]
        for v in range(1, ma + 1):
            s.append(s[-1] + pairs[v])
            
        res = []
        for q in queries:
            left = 1
            right = ma
            while left < right:
                mid = (left + right) // 2
                if s[mid] >= q + 1:
                    right = mid
                else:
                    left = mid + 1
            
            res.append(left)
        
        return res
```
