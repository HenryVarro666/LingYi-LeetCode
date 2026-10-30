---
title: "2592. 最大化数组的伟大值"
aliases: ["yiduobo的每日leetcode 2592.最大化数组的伟大值"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/hash-table", "leetcode/sorting", "leetcode/shi-pin", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/643691475"
zhihu_id: "643691475"
zhihu_title: "yiduobo的每日leetcode 2592.最大化数组的伟大值"
question_id: "2592"
question: "最大化数组的伟大值"
problem_url: "https://leetcode.cn/problems/maximize-greatness-of-an-array/"
difficulty: "Medium"
rating: 1569
created: "2023-07-15T02:27:45+08:00"
updated: "2023-07-15T02:27:45+08:00"
upvotes: 0
comments: 0
---

# 2592. 最大化数组的伟大值

> **[yiduobo的每日leetcode 2592.最大化数组的伟大值](https://zhuanlan.zhihu.com/p/643691475) · 知乎 · 2023-07-15 · 赞同 0**
> 力扣：[2592. 最大化数组的伟大值](https://leetcode.cn/problems/maximize-greatness-of-an-array/) · Medium · 灵茶山艾府：[田忌赛马，从 O(nlogn) 到 O(n)](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2592.最大化数组的伟大值

[力扣](https://leetcode.cn/problems/maximize-greatness-of-an-array/)

看到题目脑子里浮现的一个词是田忌赛马，也就是牺牲一个最小值让其他数都能得分。不过仔细观察题目可以发现，数组是可能存在相同值的，这种情况下就需要进行一些调整了。

大体的处理方法依然是贪心，有以下两个标准：

1、尽量挑弱的对手打形成配对

2、每次配对时，都选择能刚好赢的数

根据上面两个标准，就可以将数组从小到大进行排序，接下来一趟遍历，对于当前遍历的数，使用一个变量p表示其配对的数为下标为p的数。由于遍历的数是单调不减的，因此p的位置必然是单调递增的，这样一来就可以利用这个单调性在均摊O(1)的时间内找出每个数对应的p。若某一时刻p来到了数组末尾，说明无法再形成配对，此时返回配对成功的数量，也就是当前遍历到的下标即可。

最后附上python代码：

```python
class Solution(object):
    def maximizeGreatness(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        nums.sort()
        p = 0
        for index, v in enumerate(nums):
            while p < len(nums) and nums[p] <= v:
                p += 1
            
            if p == len(nums):
                break
            
            p += 1
        
        return index
```
