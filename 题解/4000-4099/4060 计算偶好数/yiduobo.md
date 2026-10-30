---
title: "4060. 计算偶好数"
aliases: ["yiduobo的每日leetcode 4060.计算偶好数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2088027001986856710"
zhihu_id: "2088027001986856710"
zhihu_title: "yiduobo的每日leetcode 4060.计算偶好数"
question_id: "4060"
question: "计算偶好数"
problem_url: "https://leetcode.cn/problems/count-evenly-good-integers/"
created: "2026-09-28T22:17:54+08:00"
updated: "2026-09-28T22:17:54+08:00"
upvotes: 1
comments: 0
---

# 4060. 计算偶好数

> **[yiduobo的每日leetcode 4060.计算偶好数](https://zhuanlan.zhihu.com/p/2088027001986856710) · 知乎 · 2026-09-28 · 赞同 1**
> 力扣：[4060. 计算偶好数](https://leetcode.cn/problems/count-evenly-good-integers/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4060.计算偶好数

<https://leetcode.cn/problems/count-evenly-good-integers/>

题目给出两个整数l和r，满足1 \<\= l \<\= r \<\= 10^15。

若一个整数包含偶数个偶数数字，则称其为偶好数。

问l到r之间偶好数的数目。

从题目的数据规模来看，使用数位动态规划应该是可行的，不过从奇偶性出发可以得到更好的算法。

首先，对于从x \* 10到x \* 10 + 9这10个数字，其中偶好数的数量显然是5个，因为无论x中偶数数字的数量是多少个，最后这一位上的0到9刚好是5个奇数5个偶数，因此其中5个与x组合后必然具有偶数个偶数数字。

更进一步的，上面的分组可以进一步细化，即可以按照2k和2k + 1来进行划分。需要注意的是，这里必须是2k和2k + 1，因为必须要保证除个位之外的数字完全相同。例如39和40就不能分作一组，认识38和39是可以的。而对于每一组的元素，其中恰好有一个偶好数，因此在这里将l到r之间所有的元素分组就可以直接计算出偶好数的数量了。

需要特别注意的是，按照上面分组的规则，若l为奇数，那么必须单独处理l，然后从l + 1开始两个两个分组。同理，若r为偶数，那么也必须单独处理r，分组只能到r - 1为止。

最后附上python代码：

```python
class Solution(object):
    def countEvenlyGoodIntegers(self, l, r):
        """
        :type l: int
        :type r: int
        :rtype: int
        """
        
        res = 0

        if l % 2 == 1:
            x = l
            cnt = 0
            while x:
                if x % 2 == 0:
                    cnt += 1
                x //= 10
            if cnt % 2 == 0:
                res += 1
            l += 1
        
        if r % 2 == 0:
            x = r
            cnt = 0
            while x:
                if x % 2 == 0:
                    cnt += 1
                x //= 10
            if cnt % 2 == 0:
                res += 1
            r -= 1
        
        return res + (r - l + 1) // 2
```
