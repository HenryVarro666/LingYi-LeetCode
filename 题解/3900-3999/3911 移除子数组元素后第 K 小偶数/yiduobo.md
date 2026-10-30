---
title: "3911. 移除子数组元素后第K小偶数"
aliases: ["yiduobo的每日leetcode 3911.移除子数组元素后第K小偶数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/binary-search", "题单/二分算法", "题单/二分算法/四-其他"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2032595777688712893"
zhihu_id: "2032595777688712893"
zhihu_title: "yiduobo的每日leetcode 3911.移除子数组元素后第K小偶数"
question_id: "3911"
question: "移除子数组元素后第 K 小偶数"
problem_url: "https://leetcode.cn/problems/k-th-smallest-remaining-even-integer-in-subarray-queries/"
difficulty: "Hard"
rating: 2156
created: "2026-04-28T23:20:35+08:00"
updated: "2026-04-28T23:20:35+08:00"
upvotes: 2
comments: 0
---

# 3911. 移除子数组元素后第K小偶数

> **[yiduobo的每日leetcode 3911.移除子数组元素后第K小偶数](https://zhuanlan.zhihu.com/p/2032595777688712893) · 知乎 · 2026-04-28 · 赞同 2**
> 力扣：[3911. 移除子数组元素后第 K 小偶数](https://leetcode.cn/problems/k-th-smallest-remaining-even-integer-in-subarray-queries/) · Hard · 灵茶山艾府：[两种方法：二分套二分 / 二分（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3911.移除子数组元素后第K小偶数

<https://leetcode.cn/problems/k-th-smallest-remaining-even-integer-in-subarray-queries/description/>

题目给出一个长度不超过10^5的数组nums，其中的元素是严格递增的。

另外给出一个二维整数数组queries，其中queries\[index\] \= \[l\[index\], r\[index\], k\[index\]\]。

对于每个查询\[l\[index\], r\[index\], k\[index\]\]，需要从无限长的正偶数序列中移除掉nums\[l\[index\]...r\[index\]\]中出现过的偶数，然后找出剩余序列中第k\[index\]个整数是什么。这里的k\[index\]不超过10^9。

更具体的，就是从序列2, 4, 6, 8, 10, ...这个序列中，移除掉出现在nums\[l\[index\]\]到nums\[r\[index\]\]之间这一段中的元素，然后问剩下的序列中第k\[index\]个整数是什么。

要求返回一个整数数组ans，其中ans[index]是第index个查询的结果。

首先可以明确的是，对于一组询问[l, r, k]，其最终答案必然处于2到2 \* (k + e)之间，这里的e表示nums[l]到nums[r]之间偶数的数量。而k越大，答案也就越大，因此在这里可以通过二分来确定这次询问的答案。

对于当前二分到的m，其对应的正偶数就是v \= m \* 2，现在还需要知道从2到v的偶数序列中，有多少个元素因为出现在nums[l]到nums[r]中而需要被移除掉。

注意到题目中的nums也是单调递增的，因此在这里就可以在nums中再次进行二分v，得出nums[l]到nums[r]之间有多少个元素小于等于v。

更进一步的，其中所有小于等于v的偶数，都会从2, 4, 6, ..., v这个正偶数序列中移除掉。不妨记移除掉的元素数目为removed，那么2, 4, 6, ..., v这个正偶数序列中剩下的元素数量就是m - removed。若这个值小于k，说明v还不够大，需要调整外层二分的下界为m + 1，否则调整上界为m。

而对于removed的计算，则可以先对nums进行一趟遍历，使用一个前缀数组even记录每个前缀中偶数元素的数量。方便起见，默认even[0]为0，而even[index]记录的是nums[0]到nums[index - 1]中偶数元素的数量。对于某个v，若nums[l]到nums[r]中小于等于v的最大的元素为nums[left]，那么就说明其中有even[left + 1] - even[l]个小于等于v的偶数，即上面需要计算的removed。

最后附上python代码：

```python
class Solution(object):
    def kthRemainingInteger(self, nums, queries):
        """
        :type nums: List[int]
        :type queries: List[List[int]]
        :rtype: List[int]
        """
        
        even = [0]
        for v in nums:
            even.append(even[-1])
            if v % 2 == 0:
                even[-1] += 1

        res = []
        for l, r, k in queries:
            lo = k
            hi = k + even[r + 1] - even[l]

            while lo < hi:
                m = (lo + hi) // 2

                v = m * 2

                if v < nums[l]:
                    removed = 0
                else:
                    left, right = l, r
                    while left < right:
                        mid = (left + right + 1) // 2
                        if v < nums[mid]:
                            right = mid - 1
                        else:
                            left = mid

                    removed = even[left + 1] - even[l]

                if m - removed < k:
                    lo = m + 1
                else:
                    hi = m

            res.append(lo * 2)
        
        return res
```
