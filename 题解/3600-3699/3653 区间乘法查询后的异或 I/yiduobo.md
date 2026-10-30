---
title: "3653. 区间乘法查询后的异或I & 3655. 区间乘法查询后的异或II"
aliases: ["yiduobo的每日leetcode 3653.区间乘法查询后的异或I && 3655.区间乘法查询后的异或II", "3653. 区间乘法查询后的异或I", "3655. 区间乘法查询后的异或II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/number-theory", "leetcode/prefix-sum", "leetcode/hard", "leetcode/bao-li", "题单/常用数据结构", "题单/常用数据结构/二-差分", "题单/常用数据结构/十一-根号算法"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1948882855666115951"
zhihu_id: "1948882855666115951"
zhihu_title: "yiduobo的每日leetcode 3653.区间乘法查询后的异或I && 3655.区间乘法查询后的异或II"
question_id: ["3653", "3655"]
question: ["区间乘法查询后的异或 I", "区间乘法查询后的异或 II"]
problem_url: ["https://leetcode.cn/problems/xor-after-range-multiplication-queries-i/", "https://leetcode.cn/problems/xor-after-range-multiplication-queries-ii/"]
difficulty: ["Medium", "Hard"]
rating: 2454
created: "2025-09-13T00:49:01+08:00"
updated: "2025-09-13T00:49:04+08:00"
upvotes: 0
comments: 0
---

# 3653. 区间乘法查询后的异或I & 3655. 区间乘法查询后的异或II

> **[yiduobo的每日leetcode 3653.区间乘法查询后的异或I && 3655.区间乘法查询后的异或II](https://zhuanlan.zhihu.com/p/1948882855666115951) · 知乎 · 2025-09-13 · 赞同 0**
> 力扣：[3653. 区间乘法查询后的异或 I](https://leetcode.cn/problems/xor-after-range-multiplication-queries-i/) · Medium · 灵茶山艾府：[非暴力做法（Python/Java/C++/Go）](灵茶山艾府.md)
> 力扣：[3655. 区间乘法查询后的异或 II](https://leetcode.cn/problems/xor-after-range-multiplication-queries-ii/) · Hard · 灵茶山艾府：[根号分解算法（Python/Java/C++/Go）](../3655%20区间乘法查询后的异或%20II/灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3653.区间乘法查询后的异或I

<https://leetcode.cn/problems/xor-after-range-multiplication-queries-i/description/>

3655.区间乘法查询后的异或II

<https://leetcode.cn/problems/xor-after-range-multiplication-queries-ii/description/>

题目给出一个长度为n的整数数组nums以及一个大小为q的二维整数数组queries，其中queries\[index\] \= \[l\[index\], r\[index\], k\[index\], v\[index\]\]。

对于每个查询，需要以k[index]为步长，从l[index]遍历到r[index]，将所有遍历到的元素nums[idx]更新为nums[idx] \* v[index] % (10^9 + 7)。这里的k[index]在1到n之间，v[index]则在1到10^5之间。

问处理完所有查询后数组中所有元素的异或结果。

两题的题设一样，第二题的数据规模较大，n和q都可达10^5。

题目中虽然给出的是动态区间操作，但是需要计算的是nums的异或值，而各类区间数据结构都不太好维护异或值，需要另想办法。

对于题目中给出的查询操作，如果步长k为1，那么就相当于将区间[l, r]之间所有的元素都乘以v。对于这类问题，可以仿照静态区间加法常用的差分数组，设计一个使用乘除法的数组。具体来说，使用一个数组f记录倍率，如果要将[l, r]之间的所有元素都乘以v，那么就应该将f[l]乘以v，然后将f[r + 1]除以v。在本题中，由于需要对10^9 + 7取模，因此除以v可以改成乘以v关于10^9 + 7的逆元。

这样一来，在所有的修改完成后，只需遍历f数组，并使用一个变量v记录前缀的乘积。对于当前遍历到的f[index]，先将v与f[index]相乘，然后将nums[index]与v相乘就可以了。

而对于k > 1的情况，则可以将所有数组下标按照对k取模的结果分组。具体来说，对于查询(l, r, k, v)，修改的下标应该是l、l + k、l + 2k、...。可以发现，这些元素模k都等于l % k，那么在这里就可以用(k, l % k)作为key建立若干个上面所说的乘积数组，对于[l, r]这个区间，其在(k, l % k)这个数组中的起点为l // k，终点为(r - l % k) // k，也就是说只需要修改这个数组中的起点的值乘以v，终点下一个位置的值乘以v关于10^9 + 7的逆元就行了。

到了这里，就可以按照与k \= 1相同的处理方法，先将查询转化为对应数组下标的修改，全部处理完成后再遍历所有的数组，计算前缀乘积并修改对应下标的nums就行了。

修改完所有nums后，再一趟遍历计算异或即可。

另外值得一提的时，对于k >\= sqrt(n)的情况，如果按照上面的方式分组，需要分的组数k反而比需要修改的下标点n / k要多，因此在这些情况下，可以直接暴力修改。

最后附上python代码：

```python
class Solution(object):
    def xorAfterQueries(self, nums, queries):
        """
        :type nums: List[int]
        :type queries: List[List[int]]
        :rtype: int
        """
        
        f = {}
        n = len(nums)
        mod = 10 ** 9 + 7

        max_v = 0
        q_dict = {}
        max_r = {}
        threshold = int(n ** 0.5)
        for left, right, k, v in queries:
            if k >= threshold:
                for index in range(left, right + 1, k):
                    nums[index] *= v
                    nums[index] %= mod
            else:
                key = (k, left % k)
                if key not in q_dict:
                    q_dict[key] = []
                    max_r[key] = 0
                right = (right - left % k) // k
                left //= k
                max_r[key] = max(max_r[key], right)
                q_dict[key].append((left, right, v))
                max_v = max(max_v, v)

        fac = [1, 1]
        inv = [None, 1]
        for v in range(2, max_v + 1):
            fac.append(fac[-1] * v % mod)
            inv.append(-(mod // v) * inv[mod % v] % mod)

        now_key = None
        for key in q_dict:
            k, r = key
            f = [1] * (max_r[key] + 1)
            for left, right, v in q_dict[key]:
                f[left] *= v
                f[left] %= mod
                if right + 1 <= max_r[key]:
                    f[right + 1] *= inv[v]
                    f[right + 1] %= mod

            now = r
            v = 1
            for index in range(max_r[key] + 1):
                v *= f[index]
                v %= mod
                nums[now] *= v
                nums[now] %= mod
                now += k

        res = 0
        for v in nums:
            res ^= v
        return res
```
