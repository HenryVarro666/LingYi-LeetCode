---
title: "3153. 所有数对中数位不同之和"
aliases: ["yiduobo的每日leetcode 3153.所有数对中数位不同之和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/brainteaser", "leetcode/math", "题单/位运算", "题单/位运算/四-拆位-/-贡献法"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/703956112"
zhihu_id: "703956112"
zhihu_title: "yiduobo的每日leetcode 3153.所有数对中数位不同之和"
question_id: "3153"
question: "所有数对中数位差之和"
problem_url: "https://leetcode.cn/problems/sum-of-digit-differences-of-all-pairs/"
difficulty: "Medium"
rating: 1645
created: "2024-06-18T01:26:27+08:00"
updated: "2024-06-18T01:26:27+08:00"
upvotes: 1
comments: 0
---

# 3153. 所有数对中数位不同之和

> **[yiduobo的每日leetcode 3153.所有数对中数位不同之和](https://zhuanlan.zhihu.com/p/703956112) · 知乎 · 2024-06-18 · 赞同 1**
> 力扣：[3153. 所有数对中数位差之和](https://leetcode.cn/problems/sum-of-digit-differences-of-all-pairs/) · Medium · 灵茶山艾府：[拆位法+枚举右维护左（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3153.所有数对中数位不同之和

[. - 力扣（LeetCode）](https://leetcode.cn/problems/sum-of-digit-differences-of-all-pairs/description/)

题目给出一个由正整数组成的数组nums，其中元素的数位长度都相同。两个整数的数位不同指的是两个整数相同位置上不同数字的数目，问nums中的所有整数对的数位不同之和。

由于题目中的数位不同只考虑整数对间的相同位置，那么在这里就可以将所有数位分开进行讨论。

对于其中某一位，若这一位上数字d一共出现了k次，那么其他的n - k个数字都可以与d形成一组不同的数位，一共就可以形成k \* (n - k)组不同的数位。更进一步的，由于d的取值范围只能在0到9之间，那么完全可以枚举d，计算当前数位的不同数对，将所有数位的不同数对数累加起来即为最终答案。

根据上面的结论，就可以先枚举nums中的每个元素，将其逐位分离，同时使用哈希表freq统计每个数位上每种数字出现的次数，其中freq[p][x]表示在p这一位上数字x出现的次数。统计完成后，再枚举哈希表中的每个数位index，对于当前的index，再从0到9枚举数字d，将freq[index][d] \* (n - freq[index][d])累加到答案中。

需要特别注意的是，上面的计算方法对于每一组数对都计算了两次，所以最终答案还需要除以2。

最后附上python代码：

```python
class Solution(object):
    def sumDigitDifferences(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        res = 0
        freq = [[0] * 10 for _ in range(9)]
        for v in nums:
            p = 0
            while v:
                freq[p][v % 10] += 1
                p += 1
                v //= 10

        for index in range(9):
            for d in range(10):
                res += freq[index][d] * (len(nums) - freq[index][d])
        
        return res // 2
```
