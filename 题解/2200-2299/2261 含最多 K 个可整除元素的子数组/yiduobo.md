---
title: "2261. 含最多K个可整除元素的子数组"
aliases: ["yiduobo的每日leetcode 2261.含最多K个可整除元素的子数组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "题单/常用数据结构", "题单/字符串", "题单/常用数据结构/六-字典树-trie", "题单/字符串/四-字符串哈希"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/548185334"
zhihu_id: "548185334"
zhihu_title: "yiduobo的每日leetcode 2261.含最多K个可整除元素的子数组"
question_id: "2261"
question: "含最多 K 个可整除元素的子数组"
problem_url: "https://leetcode.cn/problems/k-divisible-elements-subarrays/"
difficulty: "Medium"
created: "2022-07-31T13:03:36+08:00"
updated: "2022-07-31T13:03:36+08:00"
upvotes: 0
comments: 0
---

# 2261. 含最多K个可整除元素的子数组

> **[yiduobo的每日leetcode 2261.含最多K个可整除元素的子数组](https://zhuanlan.zhihu.com/p/548185334) · 知乎 · 2022-07-31 · 赞同 0**
> 力扣：[2261. 含最多 K 个可整除元素的子数组](https://leetcode.cn/problems/k-divisible-elements-subarrays/) · Medium · 灵茶山艾府：[哈希表模拟](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2261.含最多K个可整除元素的子数组

[力扣](https://leetcode.cn/problems/k-divisible-elements-subarrays/)

乍一看可以用变长的滑动窗口来解决，但是这里需要对子数组去重，所以必须要另想办法。

如果要追求最优的时间复杂度，那么就需要用到后缀数组或者其他复杂的数据结构来进行辅助，不过好在本题的数据范围并不大，因此使用暴力枚举也是可以的。

由于不同长度的子串之间是不可能出现重复的，因此可以先枚举字符串的长度l，然后检测所有长度等于l的子串是否符合条件，同时对符合条件的子串进行去重。

判断子串是否符合条件自然还是使用滑动窗口，这里已经确定了长度，所以就是常规的定长滑动窗口，统计窗口中可以被p整除的元素个数。另一方面，既然用到了定长滑动窗口，不妨顺带使用rk算法来对当前枚举的子串进行哈希从而达成去重的需求。为了防止哈希冲突，在这里可以使用两组不同的模数。

最后附上python代码：

```python
class Solution(object):
    def countDistinct(self, nums, k, p):
        """
        :type nums: List[int]
        :type k: int
        :type p: int
        :rtype: int
        """

        base = 209
        mod1 = 10 ** 9 + 7
        mod2 = 2147483647

        pow1 = pow2 = 1

        res = 0
        for l in range(1, len(nums) + 1):
            now1 = 0
            now2 = 0
            used1 = set()
            used2 = set()

            pow1 = pow1 * base % mod1
            pow2 = pow2 * base % mod2

            cnt = 0
            for index in range(l):
                if nums[index] % p == 0:
                    cnt += 1
                now1 = (now1 * base + nums[index]) % mod1
                now2 = (now2 * base + nums[index]) % mod2
            
            if cnt <= k:
                used1.add(now1)
                used2.add(now2)
                res += 1
            
            for index in range(l, len(nums)):
                now1 = (now1 * base + nums[index] - (nums[index - l] * pow1) % mod1 + mod1) % mod1
                now2 = (now2 * base + nums[index] - (nums[index - l] * pow2) % mod2 + mod2) % mod2
                if nums[index] % p == 0:
                    cnt += 1
                if nums[index - l] % p == 0:
                    cnt -= 1

                if cnt <= k and (now1 not in used1 or now2 not in used2):
                    res += 1
                    used1.add(now1)
                    used2.add(now2)
        
        return res
```
