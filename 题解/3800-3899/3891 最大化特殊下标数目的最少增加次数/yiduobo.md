---
title: "3891. 最大化特殊下标数目的最少增加次数"
aliases: ["yiduobo的每日leetcode 3891.最大化特殊下标数目的最少增加次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/enumeration", "题单/动态规划", "题单/动态规划/六-状态机-DP", "题单/动态规划/专题-前后缀分解"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2024595498951033503"
zhihu_id: "2024595498951033503"
zhihu_title: "yiduobo的每日leetcode 3891.最大化特殊下标数目的最少增加次数"
question_id: "3891"
question: "最大化特殊下标数目的最少增加次数"
problem_url: "https://leetcode.cn/problems/minimum-increase-to-maximize-special-indices/"
difficulty: "Medium"
rating: 1953
created: "2026-04-07T22:34:31+08:00"
updated: "2026-04-07T22:34:35+08:00"
upvotes: 0
comments: 0
---

# 3891. 最大化特殊下标数目的最少增加次数

> **[yiduobo的每日leetcode 3891.最大化特殊下标数目的最少增加次数](https://zhuanlan.zhihu.com/p/2024595498951033503) · 知乎 · 2026-04-07 · 赞同 0**
> 力扣：[3891. 最大化特殊下标数目的最少增加次数](https://leetcode.cn/problems/minimum-increase-to-maximize-special-indices/) · Medium · 灵茶山艾府：[前后缀分解（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3891.最大化特殊下标数目的最少增加次数

<https://leetcode.cn/problems/minimum-increase-to-maximize-special-indices/description/>

题目给出一个长度为n的整数数组nums。

对于其中某个满足0 \< index \< n - 1的下标index，若其对应的元素大于两侧相邻的元素，即nums[index] > nums[index - 1]，同时nums[index] > nums[index + 1]，那么就称index是特殊的。

现在可以执行操作，选择任意下标index，并将nums[index]增加1。

现在要求通过操作使得nums中特殊下标的数量尽量多，问至少需要多少次操作，才能使得nums中特殊下标的数量达到最大。

特殊下标对应的元素必须大于两侧相邻元素的特性，意味着特殊下标不能出现在数组的两侧，同时两个特殊下标也不可能连续出现。为了使得特殊下标的数量尽量多，那么就应该尽量让特殊下标间隔出现，在这里就需要分奇偶来进行讨论：

1、若n为奇数，那么在这里就必须将所有的奇数下标都变为特殊下标，这样才能使得特殊下标的数量尽量多。又由于题目中只提供+1操作，因此在这里就不应该动偶数下下标的元素，只需将所有奇数下标对应的元素增加到刚好大于两侧相邻元素的较大值就行了。

更具体的，对于nums[index]，其两侧元素的较大值为max(nums[index - 1], nums[index + 1])，那么nums[index]的最小目标值就是max(nums[index - 1], nums[index + 1]) + 1，因此需要的操作次数就是max(max(nums[index - 1], nums[index + 1]) + 1 - nums[index], 0)

基于上面的结论，只需一趟遍历，计算处理所有奇数下标所需的操作总和即可。

2、若n为偶数，那么相比上面这种情况多出了一个位置的空闲，也就是说最终答案必然是修改前缀的奇数下标以及后缀的偶数下标，当然这个前缀或者后缀可以为空。

例如一个长度为8的数组，可以修改的前缀奇数下标为[1, 3, 5]，而可以修改的偶数后缀下标为[2, 4, 6]，那么一共可以形成四组配对，分别为

- 前缀为空，后缀为[2, 4, 6]
- 前缀为[1]，后缀为[4, 6]
- 前缀为[1, 3]，后缀为[6]
- 前缀为[1, 3, 5]，后缀为空

于是可以正反两趟遍历，计算操作前缀奇数下标所需的最小操作次数以及操作后缀偶数下标所需的最小操作次数，操作次数的计算方法与上面相同。接下来只需枚举修改的前缀奇数下标的数量，然后计算出对应的偶数后缀下标的数量，再使用操作代价之和更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def minIncrease(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        n = len(nums)

        if n % 2 == 1:
            res = 0
            for index in range(1, n - 1, 2):
                res += max(max(nums[index - 1], nums[index + 1]) + 1 - nums[index], 0)
            return res
        
        left = [0]
        for index in range(1, n - 1, 2):
            v = max(max(nums[index - 1], nums[index + 1]) + 1 - nums[index], 0)
            left.append(left[-1] + v)
        
        right = [0]
        for index in range(n - 2, 0, -2):
            v = max(max(nums[index - 1], nums[index + 1]) + 1 - nums[index], 0)
            right.append(right[-1] + v)
        
        res = None
        for cnt in range(n // 2):
            cost = left[cnt] + right[n // 2 - 1 - cnt]
            if res is None or res > cost:
                res = cost
        return res
```
