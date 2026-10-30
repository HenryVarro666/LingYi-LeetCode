---
title: "3162. 优质数对的总数I & 3164. 优质数对的总数II"
aliases: ["yiduobo的每日leetcode 3162.优质数对的总数I && 3164.优质数对的总数II", "3162. 优质数对的总数I", "3164. 优质数对的总数II"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/hash-table", "leetcode/number-theory", "leetcode/medium", "leetcode/math", "leetcode/enumeration", "题单/数学算法", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/704771159"
zhihu_id: "704771159"
zhihu_title: "yiduobo的每日leetcode 3162.优质数对的总数I && 3164.优质数对的总数II"
question_id: ["3162", "3164"]
question: ["优质数对的总数 I", "优质数对的总数 II"]
problem_url: ["https://leetcode.cn/problems/find-the-number-of-good-pairs-i/", "https://leetcode.cn/problems/find-the-number-of-good-pairs-ii/"]
difficulty: ["Easy", "Medium"]
rating: 1777
created: "2024-06-21T23:48:29+08:00"
updated: "2024-06-21T23:48:29+08:00"
upvotes: 0
comments: 0
---

# 3162. 优质数对的总数I & 3164. 优质数对的总数II

> **[yiduobo的每日leetcode 3162.优质数对的总数I && 3164.优质数对的总数II](https://zhuanlan.zhihu.com/p/704771159) · 知乎 · 2024-06-21 · 赞同 0**
> 力扣：[3162. 优质数对的总数 I](https://leetcode.cn/problems/find-the-number-of-good-pairs-i/) · Easy · 灵茶山艾府：[非暴力做法（Python/Java/C++/Go/JS/Rust）](../3162%20优质数对的总数%20I/灵茶山艾府.md)
> 力扣：[3164. 优质数对的总数 II](https://leetcode.cn/problems/find-the-number-of-good-pairs-ii/) · Medium · 灵茶山艾府：[两种方法：枚举因子/枚举倍数（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3162.优质数对的总数I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-number-of-good-pairs-i/description/)

3164.优质数对的总数II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-number-of-good-pairs-ii/description/)

题目给出两个正整数数组num1和nums2，长度分别为n和m。另外给出一个正整数k。

对于一组nums1[i]和nums2[j]，若nums1[i]是nums2[j] \* k的倍数，那么就称(i, j)为一组优质数对。问数组中有多少组优质数对。

两题的题设一致，第二题的数据规模较大。其中n和m可达10^5，数组中的最大值可达10^6。

由于对于数值相同的nums1[i]以及nums1[i']，又或者nums2[j]以及nums2[j']，其可以构成的优质数对的数目是一致的，因此在这里就可以先用哈希表freq1和freq2分别统计nums1和nums2中每种数值出现的次数。

接下来对于freq2中的某个出现了f次的数值v，先将其乘以k，那么若nums1中存在某个数等于其倍数x，即v、v \* 2、v \* 3、...，二者就可以形成优质数对，可以形成的数对数目则为f \* freq1[x]。

不妨设num1中的最大值为ma，那么对于v而言，需要考虑的就是v、v \* 2、v \* 3、...、ma // v \* v这一共ma // v个数。当v \= 1时，需要考虑ma // 1个数，当v \= 2时，需要考虑ma // 2个数，以此类推。在极限情况下，即k \= 1同时nums2由1、2、3、...、m构成时，需要考虑的的数的个数就是

ma // 1 + ma // 2 + ... + ma // m

这个式子的时间复杂度是ma \* log(m)，在本题的数据规模下是完全够用的。于是只需遍历freq2中的每个数v以及出现的次数f，接下来将v乘以k，然后从新的v开始到nums1中的最大值ma结束，以v为步长进行遍历。对于当前遍历到的数值x，将freq1[x] \* f累加到答案中即可。

最后附上python代码：

```python
class Solution(object):
    def numberOfPairs(self, nums1, nums2, k):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :type k: int
        :rtype: int
        """

        ma = max(nums1)

        freq1 = Counter(nums1)
        freq2 = Counter(nums2)
        res = 0
        for v, f in freq2.items():
            v *= k
            for x in range(v, ma + 1, v):
                res += freq1[x] * f
        
        return res
```
