---
title: "4063. 至多一次取反能被K整除的最长子数组I & 4064. 至多一次取反能被K整除的最长子数组II"
aliases: ["yiduobo的每日leetcode 4063.至多一次取反能被K整除的最长子数组I && 4064.至多一次取反能被K整除的最长子数组II", "4063. 至多一次取反能被K整除的最长子数组I", "4064. 至多一次取反能被K整除的最长子数组II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/enumeration", "leetcode/prefix-sum", "leetcode/bao-li", "leetcode/hard", "leetcode/math", "leetcode/two-pointers", "leetcode/binary-search"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2088385407603963480"
zhihu_id: "2088385407603963480"
zhihu_title: "yiduobo的每日leetcode 4063.至多一次取反能被K整除的最长子数组I && 4064.至多一次取反能被K整除的最长子数组II"
question_id: ["4063", "4064"]
question: ["至多一次取反能被 K 整除的最长子数组 I", "至多一次取反能被 K 整除的最长子数组 II"]
problem_url: ["https://leetcode.cn/problems/longest-subarray-divisible-by-k-with-at-most-one-negation-i/", "https://leetcode.cn/problems/longest-subarray-divisible-by-k-with-at-most-one-negation-ii/"]
difficulty: ["Medium", "Hard"]
created: "2026-09-29T22:37:34+08:00"
updated: "2026-09-29T22:37:34+08:00"
upvotes: 2
comments: 0
---

# 4063. 至多一次取反能被K整除的最长子数组I & 4064. 至多一次取反能被K整除的最长子数组II

> **[yiduobo的每日leetcode 4063.至多一次取反能被K整除的最长子数组I && 4064.至多一次取反能被K整除的最长子数组II](https://zhuanlan.zhihu.com/p/2088385407603963480) · 知乎 · 2026-09-29 · 赞同 2**
> 力扣：[4063. 至多一次取反能被 K 整除的最长子数组 I](https://leetcode.cn/problems/longest-subarray-divisible-by-k-with-at-most-one-negation-i/) · Medium · 灵茶山艾府：[枚举取反元素 + 优化（Python/Java/C++/Go）](../4063%20至多一次取反能被%20K%20整除的最长子数组%20I/灵茶山艾府.md)
> 力扣：[4064. 至多一次取反能被 K 整除的最长子数组 II](https://leetcode.cn/problems/longest-subarray-divisible-by-k-with-at-most-one-negation-ii/) · Hard · 灵茶山艾府：[两种方法：枚举前缀和 / 枚举取反的数（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4063.至多一次取反能被K整除的最长子数组I

<https://leetcode.cn/problems/longest-subarray-divisible-by-k-with-at-most-one-negation-i/description/>

4064.至多一次取反能被K整除的最长子数组II

<https://leetcode.cn/problems/longest-subarray-divisible-by-k-with-at-most-one-negation-ii/description/>

题目给出一个整数数组nums以及一个整数k。

若一个子数组的和能被k整除，或者在该子数组中的一个元素取反后能使得和被k整除，则称该子数组是有效的。

取反指的是将一个元素x替换为-x。

问最长有效子数组的长度。若不存在，则返回0。

两题的题设一致。第一题中nums的长度不超过1000，k的取值范围在1到10^5之间。第二题中nums的长度不超过10^5，但k的取值范围较小，在1到3000之间。

首先，由于本题中考察的是对k取模，因此为了方便起见，在这里可以先将nums中所有的元素都对k取模。

接下来，如果不考虑取反操作，那么这就是非常标准的前缀和优化区间和的问题。

一个从left到right子数组的和如果能被k整除，那么就说明到left - 1为止的前缀和与到right为止的前缀和，在模k的意义下相等。于是只需一趟遍历，计算所有前缀模k的结果。对于当前位置，若其前缀和模k的结果为s，那么当前位置左侧所有前缀和模k等于s的前缀的下一个为止都可以作为合法子数组的左边界。为了使得子数组的长度对长，在这里显然就应该选择最左侧的那个符合条件的前缀，因此在这里可以使用一个哈希表first_s记录每种前缀和模k后首次出现的下标。

另一方面，对于两个模k后结果相同的前缀和s，若前一个s能找到合法的左边界，那么后一个s使用同一个左边界必然也是合法的，同时这样形成的子数组长度必然更长。基于这个结论，对于每种不同的前缀和，都只需要考虑其最后一次出现的下标。这样一来，需要考虑的前缀和数量最多为min(n, k)种。因此，在这里使用一个哈希表last_s记录每种前缀和模k后最后一次出现的位置。

接下来考虑可以取反的情况。

不妨设取反的元素为v，那么在去掉v之后，前缀和对k取模的结果将变为(s - v) % k，而v取反后则变为(s - v \* 2) % k。换言之，在这里只需要满足first[(s - v \* 2) % k] + 1到当前下标index之间，存在至少一个v，就说明将这个v取反后可以使得这个子数组合法。更进一步的，在这里可以改成检测index左侧v最后一次出现的位置，若这个位置大于等于first[(s - v \* 2) % k] + 1，那么就说明子数组合法。

基于这一点，就可以先一趟遍历，计算前缀和哈希表first_s以及last_s，然后使用另一个哈希表last_v记录每种v最后一次出现的位置，再进行一趟遍历，一边更新last_v一边计算结果。

对于当前遍历到的index，若s\[index\]是最后一次出现，即last_s\[s\[index\]\]恰好等于index，就检测以index为右边界的所有子数组，否则直接跳过index。

若index需要检测，则只需遍历last_v中所有不同的v，检测last_v[v]是否大于first[(s[index] - v \* 2) % k]，若满足，就说明first[(s[index] - v \* 2) % k] + 1到index这一段子数组合法，使用index - first[(s[index] - v \* 2) % k]更新答案即可。由于不同的v的数量不超过min(n, k)个，而需要检测的index同样不超过min(n, k)个，因此时间复杂度不超过O(n + min(n, k)^2)，可以一次满足以上两题的数据规模。

最后附上python代码：

```python
class Solution(object):
    def longestSubarray(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        first_s = {}
        last_s = {}

        first_s[0] = -1
        last_s[0] = -1

        s = 0
        for index, v in enumerate(nums):
            v %= k
            s += v
            s %= k

            if s not in first_s:
                first_s[s] = index
            
            last_s[s] = index

        last_v = {}
        s = 0
        res = 0
        for index, v in enumerate(nums):
            v %= k
            s += v
            s %= k

            res = max(res, index - first_s[s])
            last_v[v] = index

            if last_s[s] != index:
                continue

            for rv in last_v:
                rs = (s - rv * 2) % k
                if rs in first_s and first_s[rs] < last_v[rv]:
                    res = max(res, index - first_s[rs])

        return res
```
