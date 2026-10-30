---
title: "220. 存在重复元素 III"
aliases: ["yiduobo的每日leetcode 220.存在重复元素 III"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/148546491"
zhihu_id: "148546491"
zhihu_title: "yiduobo的每日leetcode 220.存在重复元素 III"
question_id: "220"
question: "存在重复元素 III"
problem_url: "https://leetcode.cn/problems/contains-duplicate-iii/"
created: "2020-06-15T22:15:27+08:00"
updated: "2020-06-15T22:15:27+08:00"
upvotes: 2
comments: 2
---

# 220. 存在重复元素 III

> **[yiduobo的每日leetcode 220.存在重复元素 III](https://zhuanlan.zhihu.com/p/148546491) · 知乎 · 2020-06-15 · 赞同 2**
> 力扣：[220. 存在重复元素 III](https://leetcode.cn/problems/contains-duplicate-iii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

220.存在重复元素 III <https://leetcode-cn.com/problems/contains-duplicate-iii/>

上一题的加强版，这里不再是需要两个数完全相等，而是差值可以在t之内。大体做法还是一直，用一个dict维护某个数上一次出现的位置，然后从左往右扫描判断当前数nums[index]差值在-t到t之间，即nums[index] - t到nums[index] + t之间的数上一次出现的位置是否与index在k之内。不过这样做的复杂度是O(nt)的，效率略低。

一个自然的想法是能否不判断nums[index] - t到nums[index] + t之间的每个数，而是运用某种性质优化这个判断的时间呢？受164题最大间隔的启发，在这里也可以使用分桶的做法。

对于两个a和b，其mod (t + 1)的余数显然是落在0到t之间的。二者余数的差一定是小于等于t的。换言之，如果a整除(t + 1)等于b整除(t + 1)，那么a和b之间的差一定小于等于t。

于是现在的做法就变成了，对于nums[index]除以(t + 1)进行分桶，若计算得到的桶编号x中已经有了数字，说明x桶中的数字与nums[index]差值在t之内。由于现在记录的是区间信息而不是具体的数，因此这里需要利用滑动窗口的方法，将已经超出左边界index - k的数从桶中移除，否则可能对后续的判断产生干扰。运用滑动窗口后，就不再需要判断nums[index]与桶中的数下标差值是否在k之内，而只需要判断二者本身的差值是否在t之内即可。

另外，除了判断nums[index]与x桶中数的差值之外，也可能会出现a和b差值在t之内，但是恰好被分在相邻两个桶中的情况，例如2和6相差4，但是在按5分桶时二者被分到了不同的桶中。于是在这里还需要对比nums[index]与x - 1号桶以及x + 1号桶中的数。

最后附上python代码：

```python
class Solution(object):
    def containsNearbyAlmostDuplicate(self, nums, k, t):
        """
        :type nums: List[int]
        :type k: int
        :type t: int
        :rtype: bool
        """

        if k < 0 or t < 0:
            return False

        pos_dict = {}

        for index, num in enumerate(nums):
            pos = num / (t + 1)

            if pos in pos_dict:
                return True
            if pos - 1 in pos_dict and num - pos_dict[pos - 1] <= t:
                return True
            if pos + 1 in pos_dict and pos_dict[pos + 1] - num <= t:
                return True

            pos_dict[pos] = num

            if index >= k:
                pos_dict.pop(nums[index - k] / (t + 1))

        return False
```
