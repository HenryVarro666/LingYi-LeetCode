---
title: "2464. 有效分割中的最少子数组数目"
aliases: ["yiduobo的每日leetcode 2464.有效分割中的最少子数组数目"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/632276906"
zhihu_id: "632276906"
zhihu_title: "yiduobo的每日leetcode 2464.有效分割中的最少子数组数目"
question_id: "2464"
question: "有效分割中的最少子数组数目"
problem_url: "https://leetcode.cn/problems/minimum-subarrays-in-a-valid-split/"
created: "2023-05-26T01:12:58+08:00"
updated: "2023-05-26T01:12:58+08:00"
upvotes: 0
comments: 0
---

# 2464. 有效分割中的最少子数组数目

> **[yiduobo的每日leetcode 2464.有效分割中的最少子数组数目](https://zhuanlan.zhihu.com/p/632276906) · 知乎 · 2023-05-26 · 赞同 0**
> 力扣：[2464. 有效分割中的最少子数组数目](https://leetcode.cn/problems/minimum-subarrays-in-a-valid-split/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2464.有效分割中的最少子数组数组

[力扣](https://leetcode.cn/problems/minimum-subarrays-in-a-valid-split/)

动态规划的题目。令f[i]表示以nums[i]结尾的前缀可以得到的最少划分，那么对于f[i]，不妨考虑划分出来的最后这个子数组。这个子数组的右边界显然是i，在这里就可以从0到i枚举子数组的左边界j，若nums[i]与nums[j]不互质，那么就有f[i] \= min(f[i], f[j - 1] + 1)，表示将j到i这一段划分成了最后这个子数组。

需要注意j \= 0的情况，此时不存在f[j - 1]，且一个划分显然是最小的，于是在这种情况下有f[i] \= 1。

最后附上python代码：

```python
class Solution(object):
    def validSubarraySplit(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        def gcd(x, y):
            while y:
                x, y = y, x % y
            return x

        n = len(nums)
        f = [-1] * n
        for i in range(n):
            for j in range(i + 1):
                if gcd(nums[i], nums[j]) > 1 and (j == 0 or f[j - 1] != -1):
                    if j == 0:
                        f[i] = 1
                    elif f[i] == -1 or f[i] > f[j - 1] + 1:
                        f[i] = f[j - 1] + 1
        
        return f[-1]
```
