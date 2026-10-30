---
title: "164. 最大间距"
aliases: ["yiduobo的每日leetcode 164.最大间距"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/array", "leetcode/math"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/144070490"
zhihu_id: "144070490"
zhihu_title: "yiduobo的每日leetcode 164.最大间距"
question_id: "164"
question: "最大间距"
problem_url: "https://leetcode.cn/problems/maximum-gap/"
difficulty: "Medium"
created: "2020-05-27T22:48:55+08:00"
updated: "2020-05-27T22:48:55+08:00"
upvotes: 1
comments: 0
---

# 164. 最大间距

> **[yiduobo的每日leetcode 164.最大间距](https://zhuanlan.zhihu.com/p/144070490) · 知乎 · 2020-05-27 · 赞同 1**
> 力扣：[164. 最大间距](https://leetcode.cn/problems/maximum-gap/) · Medium · 灵茶山艾府：[详细解释 O(n) 分桶法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

164.最大间距<https://leetcode-cn.com/problems/maximum-gap/>

鸽笼原理加上桶排序的题目。

首先，对于长度为n的数组nums，若其中最大的数为max_num，最小的数为min_num，那么其最大间隔一定是大于等于(max_num - min_num + 1)/(n - 1)的。

证明也很简单，极端情况下，两两之间的间隔全部相等，设这个间隔为max_gap，那么

min_num + max_gap \* (n - 1) \= max_num

将式子变一下形即可得到

max_gap \= (max_num - min_num + 1)/(n - 1)

此时最大间隔等于(max_num - min_num + 1)/(n - 1)

其他情况下，设最大间隔为max_gap，那么

min_num + max_gap \* (n - 1) - k \= max_num

这里的k表示其他间隔不足max_gap的间隔补充道max_gap需要的值，那么同样是变形之后可以得到

max_gap \= (max_num - min_num + 1)/(n - 1) + k/(n - 1)

此时最大间隔大于(max_num - min_num + 1)/(n - 1)

于是，可以将所有数按照(max_num - min_num + 1)/(n - 1)间隔，分到若干个桶里。由于最大间隔一定会大于等于桶的容量(max_num - min_num + 1)/(n - 1)，那么若两个数位于同一个桶中，那么其间隔一定是小于(max_num - min_num + 1)/(n - 1)的，因此不可能是最终的答案，于是答案一定桶与桶之间相邻两个数的间隔，那么就一定是前一个桶的最大值与后一个桶的最小值，因为只有这样才能保证两个数相邻。那么就可以在将数分到桶的过程中维护住每个桶中的最大值与最小值，之后扫描每个桶，对比相邻两个桶的最大值与最小值之间的差值即可找到最终的答案。

实际操作中，由于max_num - min_num + 1不一定能被n - 1整除，那么经典的除法向上取整操作，即对于a/b，可以变成(a - 1) / b + 1来实现，于是在这里就变成了

(max_num - min_num) / (n - 1) + 1

最后附上python代码，其中gap表示这个桶宽，part表示当前这个数应该放在哪个桶里面：

```python
class Solution(object):
    def maximumGap(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        if len(nums) < 2:
            return 0

        min_num = min(nums)
        max_num = max(nums)

        part_dict = {}
        gap = (max_num - min_num) / (len(nums) - 1) + 1

        for num in nums:
            part = (num - min_num + 1) / gap
            if part not in part_dict:
                part_dict[part] = [num, num]
            else:
                part_min, part_max = part_dict[part]
                part_min = min(part_min, num)
                part_max = max(part_max, num)
                part_dict[part] = [part_min, part_max]

        now = None
        res = 0
        for part in range(0, len(nums)):
            if part in part_dict:
                if now is not None:
                    res = max(res, part_dict[part][0] - now)

                now = part_dict[part][1]

        return res
```
