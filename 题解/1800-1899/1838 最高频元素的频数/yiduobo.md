---
title: "1838. 最高频元素的频数"
aliases: ["yiduobo的每日leetcode 1838.最高频元素的频数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/sorting", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/二-不定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/469227012"
zhihu_id: "469227012"
zhihu_title: "yiduobo的每日leetcode 1838.最高频元素的频数"
question_id: "1838"
question: "最高频元素的频数"
problem_url: "https://leetcode.cn/problems/frequency-of-the-most-frequent-element/"
difficulty: "Medium"
rating: 1876
created: "2022-02-18T23:07:34+08:00"
updated: "2022-02-18T23:07:35+08:00"
upvotes: 0
comments: 0
---

# 1838. 最高频元素的频数

> **[yiduobo的每日leetcode 1838.最高频元素的频数](https://zhuanlan.zhihu.com/p/469227012) · 知乎 · 2022-02-18 · 赞同 0**
> 力扣：[1838. 最高频元素的频数](https://leetcode.cn/problems/frequency-of-the-most-frequent-element/) · Medium · 灵茶山艾府：[排序+滑动窗口（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1838.最高频元素的频数

[力扣](https://leetcode-cn.com/problems/frequency-of-the-most-frequent-element/)

首先，由于题目只能执行加1操作，因此当选定了最终目标target后，只有小于等于target的数才有机会通过操作变为target。为了使得最后变为target的数尽量多，就应该优先小于target的数中最接近target的数变为target。为了达成这个目的，就需要对数组进行排序。

对数组排好序后，不妨设现在的最终目标target为数组中的nums[r]，那么此时就可以从r - 1开始向前遍历。对于当前遍历到的nums[l]，若满足nums[r] - nums[l] \<\= k，那么就可以将nums[l]也变为nums[r]。此时将k更新为k - (nums[r] - nums[l])，并继续向前处理nums[l- 1]。若不满足，那么说明此时的k已经不足以让l或者l之前的数变为nums[r]了。

到了这里，就已经有了一种朴素算法。首先将数组从小到大进行排序，然后枚举target的位置r。对于当前的r，从r - 1开始向左遍历，找到左边界l，将[l, r]之间的所有数都变为target。

这个朴素算法时间复杂度为O(n^2)，由于这里数组的规模并不小，因此直接枚举每个r然后计算肯定是行不通的。

不妨设将[l, r]之间的所有数变为nums[r]的总代价为p，那么就有

p \= (nums[r] - nums[r - 1]) + (nums[r] - nums[r - 2]) + ... + (nums[r] - nums[l])

另一方面，如果将[l, r - 1]之间的所有数都变为nums[r - 1]，那么此时的代价p'为

p' \= (nums[r - 1] - nums[r - 1]) + (nums[r - 1] - nums[r - 2]) + ... + (nums[r - 1] - nums[l])

对比两个式子可以发现

p' \= p - (nums[r] - nums[r - 1]) \* (r - l)

到了这里，很容易就想到使用双指针来快速求解了。

对于当已经计算出r对应的左边界l后，如果需要计算r - 1对应的左边界l'，就可以先将nums[l]到nums[r - 1]这一段先变为nums[r - 1]，此时操作的代价就是上次操作代价p[r] - (nums[r] - nums[r - 1]) \* (r - l)，也就是说对于r - 1而言，当操作到l这个位置时剩下的k'就应该等于r操作到l这个位置时剩下的k，再加上(nums[r] - nums[r - 1]) \* (r - l)，即k' \= k + (nums[r] - nums[r - 1]) \* (r - l)。由于在这里k'得到了一些补充，那么就有可能让nums[l - 1]以及更前面的数通过操作变为nums[r - 1]，因此此时还需要从l开始向左遍历，找到l'对应的位置。

重复上面的过程，直到l或r到达数组的左边界为止。

最后附上python代码：

```python
class Solution(object):
    def maxFrequency(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        nums = sorted(nums)
        r = len(nums) - 1
        l = r
        res = 1
        while l > 0 and r > 0:
            while l > 0 and nums[r] - nums[l - 1] <= k:
                k -= nums[r] - nums[l - 1]
                l -= 1

            res = max(res, r - l + 1)
            k += (r - l) * (nums[r] - nums[r - 1])
            r -= 1

        return res
```
