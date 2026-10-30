---
title: "3729. 统计有序数组中可被K整除的子数组数量"
aliases: ["yiduobo的每日leetcode 3729.统计有序数组中可被K整除的子数组数量"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/hash-table", "leetcode/math", "leetcode/prefix-sum", "题单/常用数据结构", "题单/字符串", "题单/常用数据结构/一-前缀和", "题单/字符串/八-后缀数组/后缀自动机"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1965863159148573093"
zhihu_id: "1965863159148573093"
zhihu_title: "yiduobo的每日leetcode 3729.统计有序数组中可被K整除的子数组数量"
question_id: "3729"
question: "统计有序数组中可被 K 整除的子数组数量"
problem_url: "https://leetcode.cn/problems/count-distinct-subarrays-divisible-by-k-in-sorted-array/"
difficulty: "Hard"
rating: 2248
created: "2025-10-28T20:07:07+08:00"
updated: "2025-10-28T20:07:10+08:00"
upvotes: 4
comments: 0
---

# 3729. 统计有序数组中可被K整除的子数组数量

> **[yiduobo的每日leetcode 3729.统计有序数组中可被K整除的子数组数量](https://zhuanlan.zhihu.com/p/1965863159148573093) · 知乎 · 2025-10-28 · 赞同 4**
> 力扣：[3729. 统计有序数组中可被 K 整除的子数组数量](https://leetcode.cn/problems/count-distinct-subarrays-divisible-by-k-in-sorted-array/) · Hard · 灵茶山艾府：[前缀和与哈希表，两种写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3729.统计有序数组中可被K整除的子数组数量

[3729. 统计有序数组中可被 K 整除的子数组数量 - 力扣（LeetCode）](https://leetcode.cn/problems/count-distinct-subarrays-divisible-by-k-in-sorted-array/description/)

题目给出一个按非降序排列的整数数组nums以及一个正整数k。

若nums中某个子数组的元素和可以被k整除，那么就称其为良好子数组。

问nums中不同的良好子数组的数量。

如果不考虑不同这一条件，则可以继续沿用经典的区间和转化为前缀和之差的处理方法：记s为nums的前缀和数组，对于一个从left到right的子数组，若其中元素之和可以被k整除，即

s[right] - s[left - 1] ≡ 0 (mod k)

那么就有

s[right] ≡ s[left - 1] (mod k)

也就是说，对于每个下标right，前缀中对k取模的余数与s[right]相同的前缀数目即为以right为右边界的良好子数组数目。于是只需使用一个哈希表记录每种对k取模的结果对应的前缀数目，然后一趟遍历，先更新前缀和，然后通过哈希表更新答案，然后更新哈希表即可。

接下来需要考虑如何去重。

由于题目保证了nums是按照非降序排列的，因此重复的子数组只可能是由完全相同的元素组成，因为不同元素接壤的部分在nums中都是唯一存在的。

更进一步的，对于一个元素v，不妨设其在nums中一共出现了cnt[v]次，那么对于1到cnt[v]中的某个值num，若v \* num为k的倍数，那么所有长度为num，且全部都有v组成的子数组都是良好子数组。从这cnt[v]个v中一共可以选出cnt[v] - num + 1个子数组。但是根据题目要求，这些子数组只能被计算一次，因此最终答案应该减去减去cnt[v] - num。

基于上面的结论，就可以在使用一个哈希表cnt记录数组中每种元素出现的次数，接下来对于每种元素v，从1到cnt[v]枚举上面的num并检测v \* num是否为k的倍数，若是，则将答案减去cnt[v] - num即可。

最后附上python代码：

```python
class Solution(object):
    def numGoodSubarrays(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        s = 0
        cnt_v = {}
        cnt_s = {0: 1}
        res = 0

        for v in nums:
            s += v
            s %= k
            res += cnt_s.get(s, 0)
            cnt_s[s] = cnt_s.get(s, 0) + 1
            cnt_v[v] = cnt_v.get(v, 0) + 1
        
        for v in cnt_v:
            for num in range(1, cnt_v[v]):
                if num * v % k == 0:
                    res -= cnt_v[v] - num
        
        return res
```
