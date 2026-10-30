---
title: "3785. 避免禁用值的最小交换次数"
aliases: ["yiduobo的每日leetcode 3785.避免禁用值的最小交换次数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/hash-table", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1987011307711518167"
zhihu_id: "1987011307711518167"
zhihu_title: "yiduobo的每日leetcode 3785.避免禁用值的最小交换次数"
question_id: "3785"
question: "避免禁用值的最小交换次数"
problem_url: "https://leetcode.cn/problems/minimum-swaps-to-avoid-forbidden-values/"
difficulty: "Hard"
rating: 2052
created: "2025-12-25T02:07:57+08:00"
updated: "2025-12-25T02:08:01+08:00"
upvotes: 2
comments: 0
---

# 3785. 避免禁用值的最小交换次数

> **[yiduobo的每日leetcode 3785.避免禁用值的最小交换次数](https://zhuanlan.zhihu.com/p/1987011307711518167) · 知乎 · 2025-12-25 · 赞同 2**
> 力扣：[3785. 避免禁用值的最小交换次数](https://leetcode.cn/problems/minimum-swaps-to-avoid-forbidden-values/) · Hard · 灵茶山艾府：[结论题（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3785.避免禁用值的最小交换次数

[3785. 避免禁用值的最小交换次数 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-swaps-to-avoid-forbidden-values/description/)

题目给出两个长度为n的整数数组nums以及forbidden。

现在可以执行若干次操作，每次操作中，需要选择两个不同的下标i和j，然后交换nums[i]和nums[j]。

问至少需要多少次交换，才能使得对于每个index，nums[index]都不等于forbidden[index]。若无法满足，则返回-1。

首先考虑边界的情况。

由于交换可以任意进行，那么对于任意元素，只要其在nums中出现的次数小于等于forbidden中不等于该元素的下标的数量，那么就一定有办法可以安置这种元素。

因此可以先分别遍历nums和forbidden，记录其中每种元素出现的次数，不妨记为tot和forbid，其中tot[v]和forbid[v]分别表示v在nums中以及forbidden中出现的次数。接下来对于tot中的每种元素v，若tot[v] + forbid[v] > n，那么根据鸽笼原理，v是无法安置的，此时返回-1。

接下来考虑一般情况。

直接构造交换的方式是比较困难的，不妨从交换环路的方向进行考虑。对于一共m个需要交换的元素，若其中形成的交换环路长度分别为c[0]、c[1]、c[2]、...、c[k]，那么所需的交换次数的总数为c[0] - 1 + c[1] - 1 + ... + c[k] - 1 \= m - k。也就是说，在这里尽量让交换的组变多就可以使得交换次数尽量的少，而组变多就意味着组的大小应该控制到最小，即两两分组进行交换式最理想的情况。

不过需要注意的是，并不一定可以达成两两交换的条件，因为若其中某个元素v在非法位置上的次数，大于剩余的所有元素处于非法位置上的次数，那么就必然会剩下一些v无法配对。方便期间，在这里也可以使用一个哈希表bad记录处于非法位置上的每种元素的数量，那么这种情况就是bad的value中的最大值bad[v]，大于bad中value之和的一半。

对于这种情况，最好的处理方法就是让这个元素与其他处于合法位置上的元素进行交换。由于在最开始已经判断过了是否有解，因此在这种情况下，已经保证了合法位置上的元素数量必然是足够覆盖这些无法配对的元素的。因此在这种情况下，最终答案就是处于非法位置上元素数量的最大值。

反之，若可以成功两两配对，也就是bad的value中的最大值不超过bad中value总和的一半，那么就可以进行两两配对，因此最终答案就是bad中value之和除以2向上取整。

最后附上python代码：

```python
class Solution(object):
    def minSwaps(self, nums, forbidden):
        """
        :type nums: List[int]
        :type forbidden: List[int]
        :rtype: int
        """
        
        bad = {}
        tot = {}
        forbid = {}

        for v, f in zip(nums, forbidden):
            tot[v] = tot.get(v, 0) + 1
            forbid[f] = forbid.get(f, 0) + 1
            if v == f:
                bad[v] = bad.get(v, 0) + 1
        
        for v in tot:
            if tot[v] + forbid.get(v, 0) > len(nums):
                return -1
        
        if not bad:
            return 0
        
        return max(max(bad.values()), (sum(bad.values()) + 1) // 2)
```
