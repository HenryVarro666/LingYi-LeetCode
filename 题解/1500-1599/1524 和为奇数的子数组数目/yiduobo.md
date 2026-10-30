---
title: "1524. 和为奇数的子数组数目"
aliases: ["yiduobo的每日leetcode 1524.和为奇数的子数组数目"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/422189583"
zhihu_id: "422189583"
zhihu_title: "yiduobo的每日leetcode 1524.和为奇数的子数组数目"
question_id: "1524"
question: "和为奇数的子数组数目"
problem_url: "https://leetcode.cn/problems/number-of-sub-arrays-with-odd-sum/"
created: "2021-10-16T16:08:40+08:00"
updated: "2021-10-16T16:08:40+08:00"
upvotes: 0
comments: 0
---

# 1524. 和为奇数的子数组数目

> **[yiduobo的每日leetcode 1524.和为奇数的子数组数目](https://zhuanlan.zhihu.com/p/422189583) · 知乎 · 2021-10-16 · 赞同 0**
> 力扣：[1524. 和为奇数的子数组数目](https://leetcode.cn/problems/number-of-sub-arrays-with-odd-sum/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1524.和为奇数的子数组数目

[力扣](https://leetcode-cn.com/problems/number-of-sub-arrays-with-odd-sum/)

对于这类子数组和相关的问题，经典的做法就是利用前缀和。

对于数组中的某个位置index，设其对应的前缀和为s[index]，那么对于s[index]而言，若s[index]为奇数，那么在index之前有多少个偶数的前缀和，那么就可以形成多少个和为奇数的子数组。同样的，若s[index]为偶数，那么在index之前有多少个奇数的前缀和，就可以形成多少个和为奇数的子数组。

另外还需要特别注意，若当前前缀和为奇数，那么直接将这个前缀和拎出来也是一种合法答案，因此此时还需要将答案额外加上1。

最后附上python代码：

```python
class Solution(object):
    def numOfSubarrays(self, arr):
        """
        :type arr: List[int]
        :rtype: int
        """

        now = 0
        odd = even= 0
        res = 0
        mod = 10 ** 9 + 7
        for num in arr:
            now += num
            if now & 1:
                res += even + 1
                odd += 1
            else:
                res += odd
                even += 1
            if res >= mod:
                res -= mod
        
        return res
```
