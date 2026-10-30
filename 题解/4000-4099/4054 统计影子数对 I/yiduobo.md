---
title: "4054. 统计影子数对I"
aliases: ["yiduobo的每日leetcode 4054.统计影子数对I"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/stack", "leetcode/monotonic-stack"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2084050500434007297"
zhihu_id: "2084050500434007297"
zhihu_title: "yiduobo的每日leetcode 4054.统计影子数对I"
question_id: "4054"
question: "统计影子数对 I"
problem_url: "https://leetcode.cn/problems/count-shadow-pairs-i/"
difficulty: "Medium"
created: "2026-09-17T23:02:05+08:00"
updated: "2026-09-17T23:02:05+08:00"
upvotes: 2
comments: 0
---

# 4054. 统计影子数对I

> **[yiduobo的每日leetcode 4054.统计影子数对I](https://zhuanlan.zhihu.com/p/2084050500434007297) · 知乎 · 2026-09-17 · 赞同 2**
> 力扣：[4054. 统计影子数对 I](https://leetcode.cn/problems/count-shadow-pairs-i/) · Medium · 灵茶山艾府：[枚举右维护左 + 单调栈（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4054.统计影子数对I

<https://leetcode.cn/problems/count-shadow-pairs-i/>

题目给出一个长度为n的整数数组nums。

若一对下标(i, j)满足i \< j且nums[i] \< nums[j]，同时不存在k满足i \< k \< j且nums[k] \< nums[i] \< nums[j]，那么就称(i, j)为影子对。

问数组中影子对的总数。

题目中破坏影子对成立的nums[k]小于左边界nums[i]，那么一个自然的想法就是对于每个下标i，都找出下一个更小元素所在的下标p，那么p右侧的所有下标都无法与i形成影子对，理由是p在这里充当了k的角色。

反过来，对于i + 1到p - 1之间的元素，则都满足大于等于nums[i]，也就是说只要将其中恰好等于nums[i]的下标剔除，剩下的就是能与i形成影子对的下标，数量就是p - 1 - i - same，其中same表示i + 1到p - 1直接恰好等于nums[i]的元素数目。

巧合的是，在计算每个位置的下一个更小元素时，一般会用到单调栈，那么在i找到下一个更小元素，即i出栈之时，i + 1到p - 1之间所有恰好等于nums[i]必然是刚好在i之前依次出栈，因此在这里可以记录上一个出栈的元素pre以及相同元素连续出栈的次数cnt，那么当i出栈时，若nums[i]与pre相同，就将cnt加上1，否则将pre置为nums[i]同时将cnt置为0。这样一来，出栈时对应的cnt就是上面需要计算的same。

最后附上python代码：

```python
class Solution(object):
    def shadowPairs(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        stack = []
        res = 0
        nums.append(0)

        for index, v in enumerate(nums):
            pre = None
            cnt = 0
            while stack and nums[stack[-1]] > v:
                if pre != nums[stack[-1]]:
                    pre = nums[stack[-1]]
                    cnt = 0
                else:
                    cnt += 1
                
                res += index - stack[-1] - 1 - cnt
                stack.pop()
            
            stack.append(index)

        return res
```
