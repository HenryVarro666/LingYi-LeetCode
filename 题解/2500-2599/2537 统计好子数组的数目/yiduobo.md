---
title: "2537. 统计好子数组的数目"
aliases: ["yiduobo的每日leetcode 2537.统计好子数组的数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/二-不定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/637375402"
zhihu_id: "637375402"
zhihu_title: "yiduobo的每日leetcode 2537.统计好子数组的数目"
question_id: "2537"
question: "统计好子数组的数目"
problem_url: "https://leetcode.cn/problems/count-the-number-of-good-subarrays/"
difficulty: "Medium"
rating: 1892
created: "2023-06-17T16:45:49+08:00"
updated: "2023-06-17T16:45:49+08:00"
upvotes: 0
comments: 0
---

# 2537. 统计好子数组的数目

> **[yiduobo的每日leetcode 2537.统计好子数组的数目](https://zhuanlan.zhihu.com/p/637375402) · 知乎 · 2023-06-17 · 赞同 0**
> 力扣：[2537. 统计好子数组的数目](https://leetcode.cn/problems/count-the-number-of-good-subarrays/) · Medium · 灵茶山艾府：[「越长越合法」型滑动窗口（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2537.统计好子数组的数目

[力扣](https://leetcode.cn/problems/count-the-number-of-good-subarrays/)

对于数组中的任意位置left，不妨设right为最小的，且满足子数组[left, right)为好子数组的下标，那么对于所有以left为左边界的子数组，只要其右边界大于等于right - 1，这就是一个好子数组，也就是可以提供n - right + 1个好子数组。那么现在的问题就是对于每个left，如何找出对应的最小的right。

可以发现，随着left的向右移动，right也必然是跟着向右移动的，因此在这里可以利用变长滑动窗口来找出每个left对应的right。具体来说，可以使用哈希表cnt记录窗口中每种数字出现的次数，同时使用一个变量now记录子数组中值相等的下标对。对于新加入到窗口中的数字nums\[right\]，其在先前的窗口中出现了cnt\[nums\[right\]\]次，就可以提供cnt\[nums\[right\]\] \* (cnt\[nums\[right\]\] - 1) / 2组下标对。此时这个次数变成了cnt\[nums\[right\]\] + 1，那么其可以提供的下标对就变成了(cnt\[nums\[right\]\] + 1) \* cnt\[nums\[right\]\] / 2组，相比之前多出了cnt\[nums\[right\]\]组，此时只需将now加上cnt\[nums\[right\]\]，然后将cnt\[nums\[right\]\]加上1，最后将右边界right向后移动。重复此过程直到right来到数组末尾或者now大于等于k为止。

而对于left的向右移动，其能形成的下标对则从cnt\[nums\[left\]\] \* (cnt\[nums\[left\]\] - 1) / 2变成了(cnt\[nums\[left\]\] - 1) \* (cnt\[nums\[left\]\] - 2) / 2，减少了cnt\[nums\[left\]\] - 1组相同的下标对。此时将now减去cnt\[nums\[left\]\] - 1，然后将cnt\[nums\[left\]\]减去1即可。

最后附上python代码：

```python
class Solution(object):
    def countGood(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        n = len(nums)
        right = 0
        now = 0
        res = 0
        cnt = {}
        for left in range(n):
            while right < n and now < k:
                freq = cnt.get(nums[right], 0)
                now += freq
                cnt[nums[right]] = freq + 1
                right += 1

            if now < k:
                break
            
            res += n - right + 1

            now -= (cnt[nums[left]] - 1)
            cnt[nums[left]] -= 1
        
        return res
```
